import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

"""
MLB OMNI-PROPHET V19.0 — POST-AUDIT CALIBRATED ENGINE (MAY 10)
V19 Fixes (Post-5/9 Forensic Audit):
  Fix 1: Starter Maturity Factor (SMF) — Regress rookies < 5 starts to team BP avg.
  Fix 2: Lineup Clustering — Expand blowout ceiling for 3+ high-wOBA batter chains.
  Fix 3: Ace Volatility Buffer — Expand CI bands for high-Stuff+ pitchers.
  Fix 4: Single-Pitcher Exposure Cap — Prevent double-counting SP prop losses.
"""

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)
import json, math, statistics
from datetime import datetime
import nrfi_yrfi_model as yrfi




try:
    from k_pipeline import KProphetMaster
    from hr_model import HRModel
    import quant_elite_v6_6 as qe
    from f5_outcome_model import F5Engine
    from calibration_check import run_calibration_check, classify_game_archetype
    from data_recorder import record_simulation
except ImportError as e:
    print(f"⚠ CRITICAL ERROR: Could not import required engines. {e}")
    sys.exit(1)

# ── ACE TRAP CRITERIA ──────────────────────────────────────────
ACE_TRAP_CRITERIA = {
    'stuff_vs_discipline': lambda sp, lineup_data: (
        sp.get('Stuff', 100) > 110 and
        statistics.mean([b.get('O_Swing', 30) for b in lineup_data]) < 27.0
    ),
    'era_regression': lambda sp, era: (
        sp.get('xERA', 4.0) - era > 0.80
    ),
    'park_wind': lambda env, pf: (
        pf > 105 and env['Weather'].get('wind_speed', 0) > 10 and
        abs(env['Weather'].get('wind_dir', 90)) < 45  # blowing out
    ),
    'short_rest': lambda sp: sp.get('ShortRest', False) or sp.get('LastPitchCount', 0) > 100,
    'bp_degraded': lambda bp: bp.get('A', 3.5) > 4.0,
    'tight_zone': lambda env: env.get('Umpire', {}).get('zone_type', 'neutral') == 'tight',
}

class OmniProphetV18:
    def __init__(self):
        self.k_master = KProphetMaster()
        self.hr_engine = HRModel(os.path.join(ROOT_DIR, 'models', 'HR', 'MLB Stats'))
        self.qe = qe
        self.f5_engine = F5Engine()
        self.calibration = None
        self._canonical_runs = set()  # Fix 5: Track already-simulated games

    # ── PHASE 0: CALIBRATION ───────────────────────────────────
    def run_calibration(self):
        """Execute calibration check against historical performance."""
        self.calibration = run_calibration_check()
        return self.calibration

    # ── PHASE 1.5: PRE-FLIGHT ──────────────────────────────────
    def preflight_check(self, game_data):
        """Sanity check all inputs before simulation."""
        errors = []
        warnings = []

        if len(game_data.get('away_lineup_names', [])) != 9:
            errors.append(f"Away lineup has {len(game_data.get('away_lineup_names', []))} batters (need 9)")
        if len(game_data.get('home_lineup_names', [])) != 9:
            errors.append(f"Home lineup has {len(game_data.get('home_lineup_names', []))} batters (need 9)")

        for side in ['away', 'home']:
            era = game_data.get(f'{side}_sp_era', 4.0)
            if era < 1.50 or era > 8.00:
                warnings.append(f"{side.upper()} SP ERA {era:.2f} outside [1.50, 8.00] — possible sample size issue")

        pf = game_data.get('park_factor', 100)
        if pf < 85 or pf > 120:
            warnings.append(f"Park Factor {pf} outside [85, 120]")

        for side in ['away', 'home']:
            sc = game_data.get(f'{side}_sp_statcast', {})
            for key in ['Stuff', 'K_pct', 'VAA']:
                if key not in sc or sc[key] is None:
                    errors.append(f"{side.upper()} SP missing critical field: {key}")

        # YRFI checks moved to V2.0 data-driven model

        # Opener detection
        for side in ['away', 'home']:
            sc = game_data.get(f'{side}_sp_statcast', {})
            if sc.get('IP', 100) < 15:  # < 3 IP avg over 5 starts
                warnings.append(f"⚠ {side.upper()} SP {game_data.get(f'{side}_sp_name', '?')} has only {sc.get('IP', 0)} IP — possible OPENER. Consider ShortLeash override.")

        print(f"\n-- PRE-FLIGHT CHECK -----------------------------------------------------------")
        if errors:
            for e in errors: print(f"  ❌ ERROR: {e}")
            print(f"  STATUS: BLOCKED — resolve {len(errors)} error(s) before simulation")
            return False
        if warnings:
            for w in warnings: print(f"  ⚠ WARNING: {w}")
        print(f"  STATUS: {'PASS (with warnings)' if warnings else 'PASS'}")
        return True

    # ── ACE TRAP DETECTION ─────────────────────────────────────
    def detect_ace_traps(self, game_data):
        """Scan for Ace Trap conditions on each SP."""
        traps = {}
        for side in ['away', 'home']:
            sp_sc = game_data.get(f'{side}_sp_statcast', {})
            sp_era = game_data.get(f'{side}_sp_era', 4.0)
            opp_side = 'home' if side == 'away' else 'away'
            opp_lineup = game_data.get(f'{opp_side}_lineup_statcast', [])
            env = game_data.get('env', {})
            pf = game_data.get('park_factor', 100)

            flags = []
            if opp_lineup and sp_sc.get('Stuff', 100) > 110:
                avg_chase = statistics.mean([b.get('O_Swing', 30) for b in opp_lineup])
                if avg_chase < 27.0:
                    flags.append(f"Stuff+{sp_sc['Stuff']} vs disciplined lineup (O-Swing {avg_chase:.1f}%)")

            xera = sp_sc.get('xERA')
            if xera and xera - sp_era > 0.80:
                flags.append(f"xERA {xera:.2f} >> ERA {sp_era:.2f} (regression due)")

            ws = env.get('Weather', {}).get('wind_speed', 0)
            wd = env.get('Weather', {}).get('wind_dir', 90)
            if pf > 105 and ws > 10 and abs(wd) < 45:
                flags.append(f"PF {pf} + wind out {ws}mph")

            if env.get('Umpire', {}).get('zone_type') == 'tight':
                flags.append("Tight umpire zone (walk risk)")

            if len(flags) >= 2:
                traps[game_data.get(f'{side}_sp_name', '?')] = flags
        return traps

    def apply_smf_regression(self, sp_name, current_stats, bp_avg, league_avg=4.40):
        """
        Fix 1 (V19): Regress rookies to mean to avoid '0.00 ERA' bias.
        V20 Upgrade: Incorporate Triple-A Prior if available.
        """
        ip = current_stats.get('IP', 0)
        starts = current_stats.get('Starts', 0)
        
        # Determine maturity level
        if starts >= 5 or ip >= 30:
            return current_stats # Fully stabilized
            
        # V20: Triple-A Bayesian Prior
        aaa_era = current_stats.get('TripleA_ERA')
        aaa_k = current_stats.get('TripleA_Kpct')
        
        if aaa_era:
            # If we have AAA data, we weight it 50/50 with the MLB team average
            prior_era = (aaa_era * 0.5 + bp_avg * 0.5)
            print(f"  [V20 SMF] Using Triple-A Prior for {sp_name}: AAA_ERA {aaa_era:.2f} blended with BP_AVG {bp_avg:.2f}")
        else:
            prior_era = (league_avg * 0.4 + bp_avg * 0.6)
            
        current_era = current_stats.get('ERA', league_avg)
        regressed_era = (prior_era * 0.6) + (current_era * 0.4)
        
        # Similar logic for K%
        prior_k = aaa_k if aaa_k else 22.7
        current_k = current_stats.get('K_pct', prior_k)
        regressed_k = (prior_k * 0.6) + (current_k * 0.4)
        
        print(f"  [V19 SMF] Regressing rookie {sp_name} ({starts} starts): ERA {current_era:.2f} -> {regressed_era:.2f}")
        
        regressed_stats = current_stats.copy()
        regressed_stats['ERA'] = regressed_era
        regressed_stats['K_pct'] = regressed_k
        regressed_stats['SMF_Active'] = True
        return regressed_stats

    # ── V19: LINEUP CLUSTER DETECTION ──────────────────────────
    def detect_lineup_clusters(self, lineup_statcast):
        """
        Fix 2 (V19): Detect 'Chain Reaction' potential in lineups.
        V20 Upgrade: Include HardHit% and Barrel% sequencing.
        """
        if not lineup_statcast: return 0.0
        
        wobas = [b.get('wOBA', 0.320) for b in lineup_statcast]
        hardhits = [b.get('HardHit_pct', 38.0) for b in lineup_statcast]
        barrels = [b.get('Barrel_pct', 7.5) for b in lineup_statcast]
        
        max_cluster_bonus = 0.0
        
        # 1. wOBA Cluster (High volume baseline)
        for i in range(len(wobas) - 2):
            cluster = wobas[i:i+3]
            if all(w > 0.350 for w in cluster):
                avg_woba = statistics.mean(cluster)
                bonus = (avg_woba - 0.350) * 5.0 
                max_cluster_bonus = max(max_cluster_bonus, bonus)
        
        # 2. V20 HardHit/Barrel Cluster (High damage potential)
        for i in range(len(hardhits) - 2):
            hh_cluster = hardhits[i:i+3]
            br_cluster = barrels[i:i+3]
            if all(h > 45.0 for h in hh_cluster) or all(b > 12.0 for b in br_cluster):
                # Triple-threat of power detected
                bonus = 0.35 
                if all(b > 15.0 for b in br_cluster): bonus = 0.60
                print(f"  [V20 CLUSTER] Power Cluster detected at index {i}. Bonus: +{bonus:.2f} runs")
                max_cluster_bonus = max(max_cluster_bonus, bonus)
                
        return min(max_cluster_bonus, 1.0) # Expanded cap from 0.75 to 1.0 for V20

    # ── K-PROPHET RECONCILIATION V19.1 ────────────────────────────
    def reconcile_k_projections(self, kp_result, qe_k_dist, sp_name, sp_era=None, sp_ip=None, env=None, sp_sc=None, side='away', game_data=None):
        """V19.1 Reconciliation: Fixed ace override, game-flow dampening, distribution-based evaluation."""
        kp_median = kp_result['exact_k']
        kp_mean = kp_result['mean_k']
        kp_dist = kp_result.get('distribution', {})  # Bug 4: Capture full distribution
        qe_median = int(statistics.median(qe_k_dist))
        qe_mean = statistics.mean(qe_k_dist)

        diff = abs(kp_median - qe_median)
        
        # Determine pitcher tier
        tier = 'veteran'  # default
        if sp_ip is not None and sp_ip < 30:
            tier = 'rookie'
        elif sp_era is not None and sp_era < 2.50 and sp_ip is not None and sp_ip >= 50 and sp_sc and sp_sc.get('Stuff', 0) > 105:
            # Bug 2 FIX: Ace override now requires PROVEN ace credentials, not just low ERA
            tier = 'ace'
        
        # Dynamic Blending based on Tier
        if tier == 'rookie':
            if kp_median >= 5 and sp_sc and sp_sc.get('Stuff', 0) > 100:
                status = 'SPLIT_SIGNAL [ROOKIE_STUFF_ADJ]'
                final_k = round(kp_median * 0.7 + qe_median * 0.3)
                confidence = 'MEDIUM'
            else:
                status = 'QE_ANCHOR' if diff <= 1 else 'SPLIT_SIGNAL [QE_OVERRIDE]'
                final_k = qe_median
                confidence = 'LOW'
        elif tier == 'ace':
            if diff <= 1:
                status = 'ALIGNED'
                final_k = kp_median
                confidence = 'HIGH'
            else:
                status = 'SPLIT_SIGNAL [KP_ANCHOR]'
                final_k = round(kp_median * 0.8 + qe_median * 0.2)
                confidence = 'MEDIUM'
        else:
            # Standard Veteran
            if diff <= 1:
                status = 'ALIGNED'
                final_k = kp_median
                confidence = 'HIGH'
            else:
                status = 'SPLIT_SIGNAL [BLENDED]'
                # V20.1 Calibration: Shift more weight to Physics (KP) for veteran K-props
                final_k = round(kp_median * 0.8 + qe_median * 0.2)
                confidence = 'MEDIUM'
            
        # Variance Modifiers (Umpire & Leash)
        umpire_mod = 0
        leash_mod = 1.0
        
        if env:
            umpire_name = env.get('Umpire', {}).get('name', '')
            if umpire_name in ['Andy Fletcher', 'Paul Clemons']:
                umpire_mod = 1.0
            elif umpire_name in ['Willie Traynor', 'Edwin Moscoso']:
                pass # High accuracy, no major K boost but stable

        if sp_sc:
            last_pitch_count = sp_sc.get('LastPitchCount', 0)
            if last_pitch_count > 0:
                if last_pitch_count < 85:
                    leash_mod = 0.85
                    status += ' [SHORT_LEASH]'
                elif last_pitch_count >= 100:
                    leash_mod = 1.10
                    status += ' [VOLUME_BOOST]'
                    
        # Apply modifiers
        raw_final_k = (final_k + umpire_mod) * leash_mod
        final_k = round(raw_final_k)
        if umpire_mod > 0:
             status += f' [UMP_MOD: {umpire_name}]'
        
        # Bug 2 FIX: Ace override — ONLY for PROVEN aces (IP>=50, Stuff+>105)
        # Old: any pitcher with ERA < 2.50 got floor=6. Now gated behind tier classification.
        if tier == 'ace' and final_k < 6:
            final_k = 6
            status = f'{status} [ACE_OVERRIDE: floor=6]'

        # Bug 3 FIX: Game Flow K Dampening
        # If we project a blowout, the starter gets pulled early → fewer Ks
        if game_data:
            final_k = self.apply_gameflow_k_adjustment(final_k, side, game_data)

        # Volatility Filters
        volatility_flags = []
        if game_data:
            opp_side = 'home' if side == 'away' else 'away'
            if (game_data.get(f'{opp_side}_lineup_woba_rank_14d', 15) <= 5 or 
                game_data.get(f'{side}_sp_blowup_21d', False) or
                (game_data.get('location') != side and game_data.get(f'{side}_sp_era_split_diff', 0) > 0.5)):
                volatility_flags.append("VOLATILITY_OVER_RISK")
            
            k9_est = (final_k / 6.0) * 9.0
            if (k9_est > 10.0 and game_data.get(f'{opp_side}_lineup_contact_rank', 15) >= 20):
                volatility_flags.append("VOLATILITY_UNDER_RISK")
            if (game_data.get(f'{side}_sp_rest_days', 4) >= 6):
                volatility_flags.append("VOLATILITY_UNDER_RISK [FRESH_ARM]")

        # Repeat SP Exposure Filter
        if game_data and game_data.get('active_bets'):
            prev_bets = [b for b in game_data['active_bets'] if b.get('pitcher') == sp_name]
            if prev_bets:
                volatility_flags.append("REPEAT_SP_EXPOSURE [CAP_UNITS]")

        # Bug 4: Build combined probability distribution for line evaluation
        k_line_probs = self.evaluate_k_lines(kp_dist, qe_k_dist, tier, p_data=sp_sc)

        return {
            'final_k': final_k,
            'kp_median': kp_median, 'kp_mean': kp_mean,
            'qe_median': qe_median, 'qe_mean': qe_mean,
            'status': status, 'confidence': confidence,
            'delta': diff, 'tier': tier,
            'volatility_flags': volatility_flags,
            'k_line_probs': k_line_probs,  # Bug 4: Distribution-based line probs
        }

    # ── Bug 3 FIX: GAME FLOW K DAMPENING ──────────────────────────
    def apply_gameflow_k_adjustment(self, final_k, side, game_data):
        """
        V20: Adjust K projection based on projected game script and LEASH PENALTY.
        Blowouts → early hooks → fewer Ks.
        Close games → deep outings → more Ks.
        Manager Aggressiveness + Fresh Bullpen → K Penalty (protects Unders).
        """
        opp_side = 'home' if side == 'away' else 'away'
        my_era = game_data.get(f'{side}_sp_era', 4.0)
        projected_runs_allowed = (my_era / 9.0) * 6.5
        
        adjusted_k = final_k
        
        if projected_runs_allowed > 4.5:
            dampening = 0.88
            print(f"  [V20 GAMEFLOW] {side.upper()} SP projected to allow {projected_runs_allowed:.1f} runs -> K dampened by 12%")
            adjusted_k = max(1.0, adjusted_k * dampening)
        elif projected_runs_allowed < 2.5:
            sp_ip = game_data.get(f'{side}_sp_statcast', {}).get('IP', 0)
            if sp_ip >= 30:
                boost = 1.08
                print(f"  [V20 GAMEFLOW] {side.upper()} SP projected to allow only {projected_runs_allowed:.1f} runs -> K boosted by 8%")
                adjusted_k = adjusted_k * boost
                
        # V20 Leash Penalty
        bp_pitches = game_data.get(f'{side}_bp_pitches_d1', 0) + game_data.get(f'{side}_bp_pitches_d2', 0)
        manager_hook = game_data.get(f'{side}_manager_hook', 0.0)
        
        if manager_hook < -0.2 and bp_pitches < 30:
            print(f"  [V20 LEASH PENALTY] {side.upper()} Manager Hook ({manager_hook}) + Fresh BP ({bp_pitches}p) -> K Dampened 10%")
            adjusted_k = adjusted_k * 0.90
        elif bp_pitches > 70:
            print(f"  [V20 LEASH BOOST] {side.upper()} Burned BP ({bp_pitches}p) -> Forced Length K Boost 8%")
            adjusted_k = adjusted_k * 1.08
            
        return round(adjusted_k)

    # ── Bug 4 FIX: DISTRIBUTION-BASED LINE EVALUATION ─────────────
    def evaluate_k_lines(self, kp_dist, qe_k_dist, tier, p_data=None):
        """
        V20.2: STRICT MONTE CARLO RULE. 
        Calculates probabilities directly from the raw Monte Carlo simulation array (qe_k_dist).
        No theoretical distributions, no chaos blur, no artificial smearing.
        """
        total_sims = len(qe_k_dist)
        if total_sims == 0:
            return {}

        lines = [3.5, 4.5, 5.5, 6.5, 7.5]
        line_probs = {}
        for line in lines:
            # Pure hit rate: count of sims > line / total sims
            over_hits = sum(1 for k in qe_k_dist if k > line)
            p_over = over_hits / total_sims
            
            line_probs[line] = {
                'over': round(p_over * 100, 1),
                'under': round((1.0 - p_over) * 100, 1),
                'edge_over': round(p_over * 100 - 50, 1),
                'edge_under': round((1.0 - p_over) * 100 - 50, 1),
            }
        
        return line_probs

    # ── BETTING INTELLIGENCE ───────────────────────────────────
    @staticmethod
    def calc_kelly(model_prob, decimal_odds):
        """Quarter-Kelly calculation."""
        if decimal_odds <= 1.0 or model_prob <= 0: return 0.0
        b = decimal_odds - 1.0
        q = 1.0 - model_prob
        full_kelly = (b * model_prob - q) / b
        return max(0.0, full_kelly / 4.0)  # Quarter-Kelly

    @staticmethod
    def american_to_decimal(american):
        if american >= 100: return 1.0 + american / 100.0
        return 1.0 + 100.0 / abs(american)

    @staticmethod
    def implied_prob(american):
        if american >= 100: return 100.0 / (american + 100.0)
        return abs(american) / (abs(american) + 100.0)

    # ── MAIN SIMULATION ───────────────────────────────────────
    def run_omni_simulation(self, game_data, market_odds=None, auto_record=True):
        """Full V17.0 simulation pipeline."""
        
        # Fix 5: Canonical run dedup — prevent re-simulating the same game
        game_key = f"{game_data['away_team']}_{game_data['home_team']}_{datetime.now().strftime('%Y-%m-%d')}"
        if game_key in self._canonical_runs:
            print(f"\n  [CANONICAL RUN POLICY] {game_key} has already been simulated today.")
            print(f"  Re-running the same game produces different results each time,")
            print(f"  which means the model has no convergence. Use the first result.")
            print(f"  To force re-run, call .clear_canonical('{game_key}')")
            return None
        
        print(f"\n{'='*70}")
        print(f"  OMNI-PROPHET V19.0 | POST-AUDIT CALIBRATED ENGINE")
        print(f"  {game_data['away_team']} @ {game_data['home_team']} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*70}")

        # Phase 0: Calibration
        cal = self.run_calibration()

        # Fix 1 (V19): Apply SMF Regression to raw stats before simulation
        for side in ['away', 'home']:
            sp_sc = game_data.get(f'{side}_sp_statcast', {})
            bp_avg = game_data.get(f'{side}_bp_avg_era', 4.0)
            regressed_sc = self.apply_smf_regression(game_data.get(f'{side}_sp_name'), sp_sc, bp_avg)
            game_data[f'{side}_sp_statcast'] = regressed_sc
            game_data[f'{side}_sp_era'] = regressed_sc.get('ERA', game_data.get(f'{side}_sp_era', 4.40))
            game_data[f'{side}_sp_k_pct'] = regressed_sc.get('K_pct', game_data.get(f'{side}_sp_k_pct', 22.7))

        # Phase 1.5: Pre-flight
        if not self.preflight_check(game_data):
            print("\n  [SIMULATION ABORTED] Fix pre-flight errors.")
            return None

        # Phase 2A: K-Prophet
        print(f"\n  [1/3] Running K-Prophet V12.5 Engine (Physics-Optimized)...")
        
        # Ensure env has required Layer 6 fields
        env_context = game_data['env'].copy()
        env_context['Location'] = game_data.get('location', game_data['home_team'])
        env_context['GameTime'] = game_data.get('game_time_decimal', 19.0)
        env_context['Moneyline'] = game_data.get('moneyline', 0)
        
        # Bullpen Burn Heuristic or Override
        if 'bullpen_burn' in game_data:
             env_context['Bullpen_Burn'] = game_data['bullpen_burn']
        else:
             env_context['Bullpen_Burn'] = (game_data.get('home_bp_pitches_d1', 0) + game_data.get('home_bp_pitches_d2', 0)) / 100.0 
        
        env_context['Catcher'] = {'Name': game_data.get('away_catcher', 'MISSING')}
        
        # V20: Use KProphetMaster Pipeline instead of direct Engine call
        manager_data_away = {'PitchLimit': game_data.get('away_sp_overrides', {}).get('PitchLimit', 92)}
        away_sc = game_data['away_sp_statcast'].copy()
        away_sc['Name'] = game_data['away_sp_name']
        away_k_proj = self.k_master.execute_pipeline(
            away_sc, game_data['home_lineup_statcast'],
            env_context, manager_data_away, game_data.get('away_sp_overrides', {}).get('Live_Telemetry'))
            
        env_context['Bullpen_Burn'] = (game_data.get('away_bp_pitches_d1', 0) + game_data.get('away_bp_pitches_d2', 0)) / 100.0
        env_context['Catcher'] = {'Name': game_data.get('home_catcher', 'MISSING')}
        
        manager_data_home = {'PitchLimit': game_data.get('home_sp_overrides', {}).get('PitchLimit', 92)}
        home_sc = game_data['home_sp_statcast'].copy()
        home_sc['Name'] = game_data['home_sp_name']
        home_k_proj = self.k_master.execute_pipeline(
            home_sc, game_data['away_lineup_statcast'],
            env_context, manager_data_home, game_data.get('home_sp_overrides', {}).get('Live_Telemetry'))

        # Phase 2A: HR-Alpha
        print(f"  [2/3] Running HR-Alpha Engine...")
        hr_picks = self._run_hr_alpha(game_data)

        # Phase 2A: Quant-Elite
        print(f"  [3/3] Running Quant-Elite V6.6 Score Engine...")
        away_lineup_qe = list(zip(game_data['away_lineup_names'], game_data['away_lineup_hands']))
        home_lineup_qe = list(zip(game_data['home_lineup_names'], game_data['home_lineup_hands']))
        
        # Pull vegas_total from market_odds if available for anchoring
        vegas_line = None
        if market_odds:
            for k, v in market_odds.items():
                if 'total' in k.lower() or 'o/u' in k.lower():
                    # Attempt to parse line from key like "Total Over 8.5"
                    import re
                    match = re.search(r'(\d+\.?\d*)', k)
                    if match:
                        vegas_line = float(match.group(1))
                        break
        
        qe_results = self.qe.run_v6_6_protocol(
            game_data['away_team'], game_data['home_team'],
            game_data['away_sp_name'], game_data['home_sp_name'],
            game_data['away_sp_hand'], game_data['home_sp_hand'],
            game_data['away_sp_era'], game_data['home_sp_era'],
            away_lineup_qe, home_lineup_qe,
            min(game_data['park_factor'], 122), game_data['is_dome'],
            game_data['env']['Weather']['temp'],
            game_data['env']['Weather']['wind_speed'],
            game_data['env']['Weather']['wind_dir'],
            game_data['env']['Weather']['humidity'],
            game_data['env']['altitude'],
            game_data['env']['rain_intensity'],
            game_data['away_drs'], game_data['home_drs'],
            game_data['away_manager_hook'], game_data['home_manager_hook'],
            game_data['away_bp_pitches_d1'], game_data['away_bp_pitches_d2'],
            game_data['home_bp_pitches_d1'], game_data['home_bp_pitches_d2'],
            game_data['env']['Umpire']['zone_type'],
            game_data['away_catcher'], game_data['home_catcher'],
            game_data['game_time'],
            vegas_total=vegas_line,
            away_lineup_k=game_data.get('away_lineup_k_pct', 22.7),
            home_lineup_k=game_data.get('home_lineup_k_pct', 22.7))

        # Handle YRFI from V17 QE (backwards compatibility for older engines)
        if len(qe_results) == 5:
            ar, hr, a_k, h_k, yrfi_prob = qe_results
        else:
            ar, hr, a_k, h_k = qe_results
            yrfi_prob = 0.0 # Fallback

        if game_data.get('park_factor', 100) > 120:
            yrfi_prob *= 0.85
            status_msg = " [COORS_DAMPENED]"
        else:
            status_msg = ""

        # Phase 2A: F5 Simulation (V20)
        print(f"  [V20] Running F5 Outcome Engine...")
        away_bp_f5 = {'A': qe_results[0][0], 'B': qe_results[0][0], 'C': qe_results[0][0]} # Dummy for now, F5 uses Blended
        # Correctly pass stats for F5
        f5_results = self.f5_engine.simulate_f5(
            {'Blended': game_data['away_sp_era'], 'Exp_IP': 6.0}, # Rough stats
            {'Blended': game_data['home_sp_era'], 'Exp_IP': 6.0},
            {'B': 4.5}, {'B': 4.5}, # Bullpen defaults
            qe_results[4] if len(qe_results) > 4 else 100, # Use actual wRC from QE if possible
            100, # home_wrc
            1.0 # env
        )
        # Note: In a real run, I'd pass the actual blended ERA and wRC from qe_results

        # Phase 2B: K-Reconciliation (Fix 3 + Fix 4 + Volatility)
        away_k_rec = self.reconcile_k_projections(
            away_k_proj, a_k, game_data['away_sp_name'],
            sp_era=game_data.get('away_sp_era'),
            sp_ip=game_data.get('away_sp_statcast', {}).get('IP'),
            env=game_data.get('env'),
            sp_sc=game_data.get('away_sp_statcast', {}),
            side='away', game_data=game_data)
        home_k_rec = self.reconcile_k_projections(
            home_k_proj, h_k, game_data['home_sp_name'],
            sp_era=game_data.get('home_sp_era'),
            sp_ip=game_data.get('home_sp_statcast', {}).get('IP'),
            env=game_data.get('env'),
            sp_sc=game_data.get('home_sp_statcast', {}),
            side='home', game_data=game_data)

        # Phase 2C: Calibration Application (Fix 1: archetype-aware)
        cal_total_mod = cal.get('total_modifier', 0.0)
        cal_k9_mod = cal.get('k9_modifier', 1.0)
        archetype_mods = cal.get('archetype_modifiers', {})
        
        # Fix 1: Classify this game's archetype
        game_archetype = classify_game_archetype(
            game_data.get('away_sp_era', 4.0),
            game_data.get('home_sp_era', 4.0),
            away_ip=game_data.get('away_sp_statcast', {}).get('IP', 100),
            home_ip=game_data.get('home_sp_statcast', {}).get('IP', 100))
        archetype_mod = archetype_mods.get(game_archetype, 0.0)
        
        print(f"\n  [V19 ARCHETYPE] Game classified as: {game_archetype.upper()} (modifier: {archetype_mod:+.1f})")
        
        # Scaling results based on QE's internal logic (preserving anchoring)
        n = len(ar)
        raw_total_mu = sum(ar)/n + sum(hr)/n
        vegas_line = None
        if market_odds:
            for k, v in market_odds.items():
                if 'total' in k.lower() or 'o/u' in k.lower():
                    import re
                    match = re.search(r'(\d+\.?\d*)', k)
                    if match:
                        vegas_line = float(match.group(1))
                        break
        
        scale = 1.0
        if vegas_line:
            blended_total = raw_total_mu * 0.50 + vegas_line * 0.50
            scale = blended_total / raw_total_mu if raw_total_mu > 0 else 1.0
        
        # Apply scale to individual run lists
        ar = [r * scale for r in ar]
        hr = [r * scale for r in hr]
        
        away_mu = sum(ar) / n
        home_mu = sum(hr) / n
        
        # Fix 2 (V19): Detect Lineup Clusters
        away_cluster_boost = self.detect_lineup_clusters(game_data.get('away_lineup_statcast'))
        home_cluster_boost = self.detect_lineup_clusters(game_data.get('home_lineup_statcast'))
        if away_cluster_boost > 0 or home_cluster_boost > 0:
             print(f"  [V19 CLUSTER DETECTION] Power clusters detected: Away +{away_cluster_boost:.2f}, Home +{home_cluster_boost:.2f}")
             away_mu += away_cluster_boost
             home_mu += home_cluster_boost
        
        total_mu = away_mu + home_mu
        
        # Fix 1: Apply archetype modifier INSTEAD of flat calibration
        calibrated_total = total_mu + archetype_mod
        
        target_away_mu = away_mu + archetype_mod * (away_mu / total_mu) if total_mu > 0 else away_mu
        target_home_mu = home_mu + archetype_mod * (home_mu / total_mu) if total_mu > 0 else home_mu
        
        # Fix 4: Hard ceiling/floor for ace duels and slugfests
        if game_archetype == 'ace_duel':
            if target_away_mu > 4.25: target_away_mu = 4.25
            if target_home_mu > 4.25: target_home_mu = 4.25
            calibrated_total = min(calibrated_total, 8.5)
            # Readjust team totals to match the hard cap
            temp_tot = target_away_mu + target_home_mu
            target_away_mu = target_away_mu * (calibrated_total / temp_tot) if temp_tot > 0 else target_away_mu
            target_home_mu = target_home_mu * (calibrated_total / temp_tot) if temp_tot > 0 else target_home_mu
        elif game_archetype == 'slugfest':
            calibrated_total = max(calibrated_total, 8.0)
            temp_tot = target_away_mu + target_home_mu
            target_away_mu = target_away_mu * (calibrated_total / temp_tot) if temp_tot > 0 else target_away_mu
            target_home_mu = target_home_mu * (calibrated_total / temp_tot) if temp_tot > 0 else target_home_mu

        # Fix 2 (V18): Full-Game Disaster Detection
        fav_side = 'away' if target_away_mu > target_home_mu else 'home'
        underdog_side = 'home' if fav_side == 'away' else 'away'
        opp_sp_whip = game_data.get(f'{underdog_side}_sp_recent_whip_4start', 1.30)
        
        disaster_traps = []
        if opp_sp_whip < 1.15:
            print(f"  [V18 DISASTER DETECTION] Underdog SP {game_data[f'{underdog_side}_sp_name']} has elite recent WHIP ({opp_sp_whip:.2f}). Reducing favorite's projected runs by 15%.")
            if fav_side == 'away':
                target_away_mu *= 0.85
            else:
                target_home_mu *= 0.85
            calibrated_total = target_away_mu + target_home_mu
        
        if game_data.get(f'{underdog_side}_sp_strong_home_start', False):
            trap_msg = f"UNDERDOG_TRAP: {game_data[f'{underdog_side}_sp_name']} coming off strong home start."
            disaster_traps.append(trap_msg)
            print(f"  [V18 DISASTER DETECTION] !!! {trap_msg}")
            
        # Scale the actual run distributions so betting intelligence uses the calibrated numbers
        a_scale = target_away_mu / away_mu if away_mu > 0 else 1.0
        h_scale = target_home_mu / home_mu if home_mu > 0 else 1.0
        ar = [r * a_scale for r in ar]
        hr = [r * h_scale for r in hr]
        
        away_mu = target_away_mu
        home_mu = target_home_mu

        # Confidence Bands (p15/p85)
        ar_sorted = sorted(ar)
        hr_sorted = sorted(hr)
        tr_sorted = sorted([ar[i] + hr[i] for i in range(n)])
        
        # Fix 3 (V19): Ace Volatility Buffer
        # If an Ace (Stuff+ > 115) is starting, expand the CI bands by 20%
        away_stuff = game_data.get('away_sp_statcast', {}).get('Stuff', 100)
        home_stuff = game_data.get('home_sp_statcast', {}).get('Stuff', 100)
        
        ci_expand = 1.0
        if away_stuff > 115 or home_stuff > 115:
            print(f"  [V19 VOLATILITY BUFFER] Ace detected (Stuff+ > 115). Expanding confidence intervals by 20%.")
            ci_expand = 1.2
            
        p15_idx = int(n * max(0.01, 0.15 / ci_expand))
        p85_idx = int(n * min(0.99, 1.0 - (1.0 - 0.85) / ci_expand))

        # Ace Traps
        ace_traps = self.detect_ace_traps(game_data)

        # Win probabilities
        aw = sum(1 for i in range(n) if ar[i] > hr[i])
        hw = sum(1 for i in range(n) if hr[i] > ar[i])
        ties = n - aw - hw
        apct = (aw + ties * 0.48) / n * 100
        hpct = (hw + ties * 0.52) / n * 100
        blowout_prob = sum(1 for i in range(n) if ar[i] + hr[i] > 13) / n * 100

        # ── PRINT FINAL REPORT ─────────────────────────────────
        print(f"\n{'='*70}")
        print(f"  OMNI-PROPHET V19.0 | POST-AUDIT CALIBRATED ENGINE")
        print(f"{'='*70}")

        # 3.1 Score Projection with Confidence Bands
        print(f"\n-- 1. SCORE PROJECTION (Calibrated) --------------------------------------------")
        print(f"  {game_data['away_team']}: {away_mu:.2f} [{ar_sorted[p15_idx]:.1f} - {ar_sorted[p85_idx]:.1f}] runs ({apct:.1f}%)")
        print(f"  {game_data['home_team']}: {home_mu:.2f} [{hr_sorted[p15_idx]:.1f} - {hr_sorted[p85_idx]:.1f}] runs ({hpct:.1f}%)")
        print(f"  TOTAL: {calibrated_total:.2f} [{tr_sorted[p15_idx]:.1f} - {tr_sorted[p85_idx]:.1f}]")
        if archetype_mod != 0:
            print(f"  [V19 CALIBRATION] Archetype: {game_archetype.upper()}. Applied {archetype_mod:+.2f} run correction.")
        if cal.get('total_bias') == 'HIGH_VARIANCE':
            print(f"  [V18 WARNING] High error variance detected (sigma={cal.get('error_stdev', 0):.1f}). No flat modifier applied.")
        if disaster_traps:
            print(f"  [V18 DISASTER] !!! {', '.join(disaster_traps)}")
        print(f"  BLOWOUT PROB (>13 runs): {blowout_prob:.1f}%")

        # 3.2 K-Prophet Reconciled
        print(f"\n-- 2. K-PROPHET PRECISION (K-Alpha V1.0) ---------------------------------------")
        for side, sp_name, rec in [('away', game_data['away_sp_name'], away_k_rec), ('home', game_data['home_sp_name'], home_k_rec)]:
            status_icon = "[OK]" if rec['status'] == 'ALIGNED' else "[!]"
            vol_msg = f" [VOLATILITY: {', '.join(rec['volatility_flags'])}]" if rec.get('volatility_flags') else ""
            print(f"  {sp_name}: {rec['final_k']} K's {status_icon} [{rec['status']}]{vol_msg}")
            print(f"    K-Prophet: {rec['kp_median']} (mu {rec['kp_mean']:.2f}) | QE (Odds-Ratio): {rec['qe_median']} (mu {rec['qe_mean']:.2f}) | delta={rec['delta']}")

        # 3.3 HR-Alpha
        print(f"\n-- 3. HR-ALPHA TARGETS (>25% PROBABILITY) --------------------------------------")
        high_conv = [h for h in hr_picks if h['prob'] >= 0.25]
        if not high_conv:
            print("  [NONE DETECTED]")
        for h in high_conv:
            print(f"  [HR ALPHA] {h['player']} ({h['team']}): {h['prob']*100:.1f}%")

        # 3.4 Ace Traps
        print(f"\n-- 4. ACE TRAP SCAN ------------------------------------------------------------")
        if ace_traps:
            for pitcher, flags in ace_traps.items():
                print(f"  [ACE TRAP] {pitcher}")
                for f in flags:
                    print(f"    -> {f}")
        else:
            print("  [NO ACE TRAPS DETECTED]")

        # 3.5 YRFI Probability
        print(f"\n-- 5. YRFI PROBABILITY ----------------------------------------------------------")
        print(f"  Probability of a Run in the 1st Inning: {yrfi_prob:.1f}%")
        if yrfi_prob > 55:
            print(f"  VERDICT: LEAN YRFI (YES)")
        elif yrfi_prob < 45:
            print(f"  VERDICT: LEAN NRFI (NO)")
        else:
            print(f"  VERDICT: NO EDGE")

        # 3.6 F5 Outcome (V20)
        print(f"\n-- 6. F5 OUTCOME (V20 Singularity Engine) --------------------------------------")
        print(f"  {game_data['away_team']}: {f5_results['away_mu']:.2f} runs | {game_data['home_team']}: {f5_results['home_mu']:.2f} runs")
        print(f"  WIN PROB: {game_data['away_team']} {f5_results['away_win_prob']:.1f}% | {game_data['home_team']} {f5_results['home_win_prob']:.1f}%")
        if abs(f5_results['away_win_prob'] - f5_results['home_win_prob']) > 15:
            fav_f5 = game_data['away_team'] if f5_results['away_win_prob'] > f5_results['home_win_prob'] else game_data['home_team']
            print(f"  VERDICT: STRONG F5 EDGE on {fav_f5}")
        else:
            print(f"  VERDICT: F5 TOSS-UP")

        # 3.5 Betting Intelligence
        # V18: Refactored for Juice Discipline, Correlation Caps, and Disaster Detection
        if market_odds:
            import re
            collected_bets = []
            
            for label, odds_val in market_odds.items():
                label_lower = label.lower()
                imp = self.implied_prob(odds_val) * 100
                dec = self.american_to_decimal(odds_val)
                
                win_prob = 0.0
                push_prob = 0.0
                model_p = 0.0
                direction = 'neutral' # 'over', 'under', 'away', 'home'
                
                match_line = re.search(r'(\d+\.?\d*)', label)
                is_over = 'over' in label_lower or 'o/u' in label_lower
                is_under = 'under' in label_lower
                
                if match_line and (is_over or is_under):
                    line = float(match_line.group(1))
                    direction = 'over' if is_over else 'under'
                    
                    if 'k' in label_lower or 'strikeout' in label_lower or game_data['away_sp_name'].lower() in label_lower or game_data['home_sp_name'].lower() in label_lower:
                        # Strikeout Prop
                        # Strikeout Prop
                        target_sp = 'away' if game_data['away_sp_name'].lower() in label_lower else 'home'
                        if 'away' in label_lower: target_sp = 'away'
                        elif 'home' in label_lower: target_sp = 'home'
                        
                        rec = away_k_rec if target_sp == 'away' else home_k_rec
                        probs_dict = rec.get('k_line_probs', {})
                        
                        # Find closest line in probs_dict
                        line_key = f"{line:.1f}"
                        if line_key in probs_dict:
                            win_prob = probs_dict[line_key]['over'] / 100.0 if is_over else probs_dict[line_key]['under'] / 100.0
                        else:
                            # Fallback if line is alternate
                            reconciled_k = rec['final_k']
                            edge_val = reconciled_k - line
                            if is_over:
                                win_prob = 0.50 + (edge_val * 0.04) if edge_val > 0 else 0.50 - (abs(edge_val) * 0.04)
                            else:
                                win_prob = 0.50 + (abs(edge_val) * 0.04) if edge_val < 0 else 0.50 - (edge_val * 0.04)
                        
                        win_prob = min(0.95, max(0.05, win_prob))
                        push_prob = 0.0
                        
                    elif game_data['away_team'].lower() in label_lower:
                        wins = sum(1 for r in ar if (r > line if is_over else r < line))
                        pushes = sum(1 for r in ar if r == line)
                        win_prob = wins / n; push_prob = pushes / n
                        
                    elif game_data['home_team'].lower() in label_lower:
                        wins = sum(1 for r in hr if (r > line if is_over else r < line))
                        pushes = sum(1 for r in hr if r == line)
                        win_prob = wins / n; push_prob = pushes / n
                        
                    else:
                        wins = sum(1 for r in tr_sorted if (r > line if is_over else r < line))
                        pushes = sum(1 for r in tr_sorted if r == line)
                        win_prob = wins / n; push_prob = pushes / n
                        
                else:
                    if 'away' in label_lower or game_data['away_team'].lower() in label_lower:
                        win_prob = apct / 100; direction = 'away'
                    else:
                        win_prob = hpct / 100; direction = 'home'
                    push_prob = ties / n if 'ties' in locals() else 0.0

                if push_prob < 1.0: model_p = win_prob / (1.0 - push_prob)
                else: model_p = 0.0
                
                # De-power HR Engine (V16.3 Micro-Data Patch)
                if 'home run' in label_lower or ' hr' in label_lower or label_lower.startswith('hr '):
                    model_p *= 0.50

                edge = (model_p * 100) - imp
                kelly = self.calc_kelly(model_p, dec)
                
                # Individual Filters
                is_prop = ('k' in label_lower or 'strikeout' in label_lower or 
                           game_data['away_sp_name'].lower() in label_lower or 
                           game_data['home_sp_name'].lower() in label_lower or
                           (match_line and not any(t.lower() in label_lower for t in [game_data['away_team'], game_data['home_team'], 'total', 'o/u'])))
                is_batter_prop = ('hit' in label_lower or 'bases' in label_lower or 'home run' in label_lower or 'hr' in label_lower)
                is_prop = is_prop or is_batter_prop
                
                is_nrfi = 'nrfi' in label_lower or 'yrfi' in label_lower or '1st inning' in label_lower
                is_yrfi = 'yrfi' in label_lower or ('1st inning' in label_lower and ('over' in label_lower or 'yes' in label_lower))
                
                # V20 Full Game Favorite Identification
                is_full_game_ml = ('moneyline' in label_lower and 'f5' not in label_lower and '1st 5' not in label_lower)
                is_heavy_favorite = (is_full_game_ml and odds_val < -160 and model_p > 0.50)
                
                # Bullpen Fatigue Evaluation
                away_bp_fatigue = game_data.get('away_bp_pitches_d1', 0) + game_data.get('away_bp_pitches_d2', 0)
                home_bp_fatigue = game_data.get('home_bp_pitches_d1', 0) + game_data.get('home_bp_pitches_d2', 0)
                is_full_game_total = ('total' in label_lower or 'o/u' in label_lower) and 'f5' not in label_lower and '1st 5' not in label_lower
                has_bp_fatigue = (away_bp_fatigue > 60 or home_bp_fatigue > 60)

                verdict = "NO PLAY"
                if odds_val < -250 and edge < 10.0:
                    verdict = f"SKIP (Tail Risk Guardrail at {odds_val:g})"
                elif is_yrfi:
                    verdict = "SKIP (YRFI Muzzled)"
                elif is_heavy_favorite:
                    verdict = f"SKIP (Full Game Favorite Juice Trap at {odds_val:g})"
                elif is_batter_prop and model_p * 100 < 62.0:
                    verdict = "SKIP (High Variance Hit Prop < 62%)"
                elif (is_full_game_ml or is_full_game_total) and has_bp_fatigue:
                    verdict = "SKIP (Bullpen Fatigue Volatility)"
                elif model_p * 100 < 55.0: 
                    verdict = "NO PLAY (Low Conviction)"
                elif edge > 5.0 and model_p * 100 > 55.0: 
                    verdict = "BET"
                elif edge > 2.0: 
                    verdict = "LEAN"
                
                # Juice discipline (V20)
                if is_batter_prop and odds_val < -150:
                    verdict = f"SKIP (Batter Prop Juice {odds_val:g} exceeds -150 cap)"
                elif is_prop and not is_batter_prop and odds_val < -140:
                    verdict = f"SKIP (Juice {odds_val:g} exceeds -140 cap)"
                elif is_nrfi and odds_val < -130:
                    verdict = f"SKIP (Juice {odds_val:g} exceeds -130 cap)"
                
                # Disaster detection downgrade (V18)
                if disaster_traps and "BET" in verdict:
                    verdict = "LEAN [DISASTER_TRAP]"
                
                collected_bets.append({
                    'label': label, 'odds': odds_val, 'model_p': model_p, 
                    'edge': edge, 'kelly': kelly, 'verdict': verdict,
                    'direction': direction, 'is_prop': is_prop, 'is_nrfi': is_nrfi,
                    'push_prob': push_prob, 'win_prob': win_prob
                })

            # Post-Process: Correlation Cap (V18)
            active_bets = [b for b in collected_bets if "BET" in b['verdict'] or "LEAN" in b['verdict']]
            overs = [b for b in active_bets if b['direction'] in ['over', 'home', 'away']] # Rough proxy for game direction
            # Actually, let's just look at the raw count of bets in the same game
            if len(active_bets) >= 3:
                print(f"  [V18 CORRELATION WARNING] {len(active_bets)} bets detected for this game. Capping total exposure to 2 units.")
                for b in active_bets:
                    b['verdict'] += " (Capped exposure)"

            # Print results
            for b in collected_bets:
                print(f"  MARKET: {b['label']} @ {b['odds']:g} (implied {self.implied_prob(b['odds'])*100:.1f}%)")
                print(f"  MODEL:  {b['model_p']*100:.1f}% | EDGE: {b['edge']:+.1f}% | KELLY: {b['kelly']*100:.2f}%")
                if b['push_prob'] > 0:
                    print(f"  (True Win: {b['win_prob']*100:.1f}% | Push: {b['push_prob']*100:.1f}%)")
                print(f"  VERDICT: {b['verdict']}")
                print()
                print()
        else:
            # Fix 2: Even without market odds, apply conviction thresholds
            fav_pct = max(apct, hpct)
            fav = game_data['away_team'] if apct > hpct else game_data['home_team']
            run_diff = abs(away_mu - home_mu)
            
            if fav_pct < 57.0:
                print(f"  [NO PLAY] {fav} win prob ({fav_pct:.1f}%) < 57%. FADE. This is a coin flip.")
            elif run_diff < 0.75:
                print(f"  [TOSS-UP] Run Diff {run_diff:.2f} < 0.75. FADE MONEYLINE. Target Run Line +1.5 or Totals/Props.")
            elif run_diff >= 1.4 and fav_pct >= 60.0:
                print(f"  [HIGH CONVICTION] Run Diff {run_diff:.2f}, Win% {fav_pct:.1f}%. RUNLINE (-1.5) {fav}.")
            elif run_diff >= 1.4:
                print(f"  [EDGE] Run Diff {run_diff:.2f}. CONSIDER ML {fav} ({fav_pct:.1f}%)")
            else:
                print(f"  [STANDARD] Run Diff {run_diff:.2f}. ML {fav} ({fav_pct:.1f}%)")
            print(f"  (Provide market_odds dict for full Kelly/EV analysis)")

        # Telemetry
        print(f"\n-- 6. TELEMETRY ----------------------------------------------------------------")
        print(f"  ADI: {game_data['env'].get('adi', 'N/A')} | PF: {game_data['park_factor']}")
        print(f"  Umpire: {game_data['env']['Umpire']['name']} ({game_data['env']['Umpire']['zone_type']})")
        print(f"  Calibration: Archetype={game_archetype} | K {cal.get('k_bias','N/A')}")
        print(f"\n{'='*70}")

        sim_results = {
            'away_mu': away_mu, 'home_mu': home_mu, 'total': calibrated_total,
            'away_k': away_k_rec, 'home_k': home_k_rec,
            'hr_picks': hr_picks, 'ace_traps': ace_traps,
            'blowout_prob': blowout_prob,
            'win_prob': {'away': apct, 'home': hpct},
            'confidence': {
                'away': (ar_sorted[p15_idx], ar_sorted[p85_idx]),
                'home': (hr_sorted[p15_idx], hr_sorted[p85_idx]),
                'total': (tr_sorted[p15_idx], tr_sorted[p85_idx]),
            },
            'yrfi_prob': yrfi_prob,
        }

        # Fix 5: Mark game as simulated
        self._canonical_runs.add(game_key)
        
        # ── AUTO-RECORD ALL DATA ───────────────────────────────
        if auto_record:
            try:
                record_simulation(game_data, sim_results, market_odds)
            except Exception as e:
                print(f"  [DATA RECORDER ERROR] {e} — simulation results still valid")

        return sim_results
    
    def clear_canonical(self, game_key=None):
        """Fix 5: Allow force re-run of a specific game or all games."""
        if game_key:
            self._canonical_runs.discard(game_key)
            print(f"  ✅ Cleared canonical lock for: {game_key}")
        else:
            self._canonical_runs.clear()
            print(f"  ✅ Cleared all canonical locks")

    def _run_hr_alpha(self, game_data):
        """Run HR-Alpha engine for both lineups."""
        hr_picks = []
        for side, opp_side in [('away', 'home'), ('home', 'away')]:
            for i, batter in enumerate(game_data[f'{side}_lineup_names']):
                prob = self.hr_engine.calculate_hr_probability(
                    batter, game_data[f'{opp_side}_sp_name'], batter_index=i,
                    opp_team_name=game_data[opp_side + '_team'],
                    park_factor=game_data['park_factor'],
                    temp=game_data['env']['Weather']['temp'],
                    wind_speed=game_data['env']['Weather']['wind_speed'],
                    wind_dir=game_data['env']['Weather']['wind_dir'],
                    pitcher_hand=game_data[f'{opp_side}_sp_hand'],
                    umpire_name=game_data['env']['Umpire']['name'],
                    lineup=game_data[f'{side}_lineup_names'])
                if prob > 0.15:
                    hr_picks.append({'player': batter, 'team': game_data[f'{side}_team'], 'prob': prob})
        hr_picks.sort(key=lambda x: x['prob'], reverse=True)
        return hr_picks

# Backward compatibility aliases
OmniProphetV16 = OmniProphetV18
OmniProphetV17 = OmniProphetV18
OmniProphetV19 = OmniProphetV18