import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

"""
MLB OMNI-PROPHET V20.0 — THE UNIFIED SINGULARITY (MAY 14)
V20 Features (The Synchronization Patch):
  - Intelligence Hub: Shared state between K-Prophet, HR-Alpha, YRFI, and QE.
  - Stuff+ Anchor: K-Prophet's Stuff+ suppresses runs in QE and F5.
  - HR-Alpha YRFI: Precision HR probabilities directly inform 1st Inning outcome.
  - Umpire Sync: Unified zone bias across all sub-engines.
  - V20 Logic: Advanced Pitcher-Catcher Synergy and Lineup Clustering.
"""

import json, math, statistics
from datetime import datetime
import nrfi_yrfi_model as yrfi
from intelligence_hub import HUB

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

class OmniProphetV20:
    def __init__(self):
        self.k_master = KProphetMaster()
        self.hr_engine = HRModel(os.path.join(ROOT_DIR, 'models', 'HR', 'MLB Stats'))
        self.qe = qe
        self.f5_engine = F5Engine()
        self.calibration = None
        self._canonical_runs = set()

    def run_calibration(self):
        self.calibration = run_calibration_check()
        return self.calibration

    def preflight_check(self, game_data):
        errors = []
        warnings = []
        if len(game_data.get('away_lineup_names', [])) != 9:
            errors.append(f"Away lineup has {len(game_data.get('away_lineup_names', []))} batters (need 9)")
        if len(game_data.get('home_lineup_names', [])) != 9:
            errors.append(f"Home lineup has {len(game_data.get('home_lineup_names', []))} batters (need 9)")
        for side in ['away', 'home']:
            era = game_data.get(f'{side}_sp_era', 4.0)
            if era < 1.50 or era > 8.00:
                warnings.append(f"{side.upper()} SP ERA {era:.2f} outside [1.50, 8.00]")
        print(f"\n-- PRE-FLIGHT CHECK -----------------------------------------------------------")
        if errors:
            for e in errors: print(f"  ❌ ERROR: {e}")
            return False
        if warnings:
            for w in warnings: print(f"  ⚠ WARNING: {w}")
        print(f"  STATUS: PASS")
        return True

    def detect_ace_traps(self, game_data):
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
                if avg_chase < 27.0: flags.append(f"Stuff+{sp_sc['Stuff']} vs disciplined lineup")
            xera = sp_sc.get('xERA')
            if xera and xera - sp_era > 0.80: flags.append(f"xERA {xera:.2f} >> ERA {sp_era:.2f}")
            if env.get('Umpire', {}).get('zone_type') == 'tight': flags.append("Tight umpire zone")
            if len(flags) >= 2: traps[game_data.get(f'{side}_sp_name', '?')] = flags
        return traps

    def apply_smf_regression(self, sp_name, current_stats, bp_avg, league_avg=4.40):
        ip = current_stats.get('IP', 0)
        starts = current_stats.get('Starts', 0)
        if starts >= 5 or ip >= 30: return current_stats
        prior_era = (league_avg * 0.4 + bp_avg * 0.6)
        current_era = current_stats.get('ERA', league_avg)
        regressed_era = (prior_era * 0.6) + (current_era * 0.4)
        regressed_stats = current_stats.copy()
        regressed_stats['ERA'] = regressed_era
        regressed_stats['SMF_Active'] = True
        return regressed_stats

    def detect_lineup_clusters(self, lineup_statcast):
        if not lineup_statcast: return 0.0
        wobas = [b.get('wOBA', 0.320) for b in lineup_statcast]
        max_cluster_bonus = 0.0
        for i in range(len(wobas) - 2):
            cluster = wobas[i:i+3]
            if all(w > 0.350 for w in cluster):
                bonus = (statistics.mean(cluster) - 0.350) * 5.0 
                max_cluster_bonus = max(max_cluster_bonus, bonus)
        return min(max_cluster_bonus, 1.0)

    def reconcile_k_projections(self, kp_result, qe_k_dist, sp_name, sp_era=None, sp_ip=None, env=None, sp_sc=None, side='away', game_data=None):
        kp_median = kp_result['exact_k']
        kp_mean = kp_result['mean_k']
        kp_dist = kp_result.get('distribution', {})
        qe_median = int(statistics.median(qe_k_dist))
        qe_mean = statistics.mean(qe_k_dist)
        diff = abs(kp_median - qe_median)
        
        tier = 'veteran'
        if sp_ip is not None and sp_ip < 30: tier = 'rookie'
        elif sp_era is not None and sp_era < 2.50 and sp_sc and sp_sc.get('Stuff', 0) > 105: tier = 'ace'
        
        if tier == 'rookie':
            final_k = qe_median
            status = 'QE_ANCHOR'
            confidence = 'LOW'
        elif tier == 'ace':
            final_k = round(kp_median * 0.8 + qe_median * 0.2)
            status = 'ALIGNED' if diff <= 1 else 'SPLIT_SIGNAL [KP_ANCHOR]'
            confidence = 'MEDIUM'
        else:
            final_k = round(kp_median * 0.8 + qe_median * 0.2)
            status = 'ALIGNED' if diff <= 1 else 'SPLIT_SIGNAL [BLENDED]'
            confidence = 'MEDIUM'
            
        # Volume/Leash
        leash_mod = 1.0
        if sp_sc:
            lpc = sp_sc.get('LastPitchCount', 0)
            if lpc > 0 and lpc < 85: 
                leash_mod = 0.85
                status += ' [SHORT_LEASH]'
        
        final_k = round(final_k * leash_mod)
        if game_data:
            final_k = self.apply_gameflow_k_adjustment(final_k, side, game_data)
        
        k_line_probs = self.evaluate_k_lines(kp_dist, qe_k_dist, tier, p_data=sp_sc)

        return {
            'final_k': final_k, 'kp_median': kp_median, 'kp_mean': kp_mean,
            'qe_median': qe_median, 'qe_mean': qe_mean,
            'status': status, 'confidence': confidence, 'delta': diff, 'tier': tier,
            'k_line_probs': k_line_probs
        }

    def apply_gameflow_k_adjustment(self, final_k, side, game_data):
        my_era = game_data.get(f'{side}_sp_era', 4.0)
        pra = (my_era / 9.0) * 6.5
        adjusted_k = final_k
        if pra > 4.5:
            adjusted_k *= 0.88
        elif pra < 2.5:
            adjusted_k *= 1.08
        return round(adjusted_k)

    def evaluate_k_lines(self, kp_dist, qe_k_dist, tier, p_data=None):
        total_sims = len(qe_k_dist)
        if total_sims == 0: return {}
        lines = [3.5, 4.5, 5.5, 6.5, 7.5]
        line_probs = {}
        for line in lines:
            over_hits = sum(1 for k in qe_k_dist if k > line)
            p_over = over_hits / total_sims
            line_probs[f"{line:.1f}"] = {
                'over': p_over * 100, 'under': (1.0 - p_over) * 100
            }
        return line_probs

    def run_omni_simulation(self, game_data, market_odds=None, auto_record=True):
        game_id = f"{game_data['away_team']}_{game_data['home_team']}_{datetime.now().strftime('%Y%m%d')}"
        HUB.clear(game_id)
        HUB.set("GameID", game_id)
        
        print(f"\n{'='*70}")
        print(f"  OMNI-PROPHET V20.0 — THE UNIFIED SINGULARITY")
        print(f"  {game_data['away_team']} @ {game_data['home_team']} | ID: {game_id}")
        print(f"{'='*70}")

        # Phase 0: Calibration
        cal = self.run_calibration()

        # Phase 1: SMF Regression
        for side in ['away', 'home']:
            sp_sc = game_data.get(f'{side}_sp_statcast', {})
            bp_avg = game_data.get(f'{side}_bp_avg_era', 4.40)
            regressed_sc = self.apply_smf_regression(game_data.get(f'{side}_sp_name'), sp_sc, bp_avg)
            game_data[f'{side}_sp_statcast'] = regressed_sc
            game_data[f'{side}_sp_era'] = regressed_sc.get('ERA', 4.40)

        # Pre-flight
        if not self.preflight_check(game_data): return None

        # ── THE V20 SYNCHRONIZED SEQUENCE ─────────────────────
        
        # 1. K-Prophet (The Physics Anchor)
        print(f"\n  [1/4] Running K-Prophet V20 (Physics Anchor)...")
        env_context = game_data['env'].copy()
        env_context['GameID'] = game_id
        
        away_sc = game_data['away_sp_statcast'].copy()
        away_sc['Name'] = game_data['away_sp_name']
        away_k_proj = self.k_master.execute_pipeline(
            away_sc, game_data['home_lineup_statcast'],
            env_context, {'PitchLimit': 92})
            
        home_sc = game_data['home_sp_statcast'].copy()
        home_sc['Name'] = game_data['home_sp_name']
        home_k_proj = self.k_master.execute_pipeline(
            home_sc, game_data['away_lineup_statcast'],
            env_context, {'PitchLimit': 92})

        # 2. HR-Alpha (Consumes Stuff+ from Hub)
        print(f"  [2/4] Running HR-Alpha (Consuming Stuff+)...")
        hr_picks = self._run_hr_alpha(game_data)

        # 3. YRFI (Consumes HR Prob & Umpire Bias)
        print(f"  [3/4] Running YRFI Model (Consuming HR Risks)...")
        # Top 1st: Away Lineup vs Home SP
        top_sim = yrfi.FirstInningSim(game_data['home_sp_name'], game_data['away_lineup_names'], game_data['away_team'], game_data['home_team'])
        top_nr_prob = top_sim.simulate_half_inning()
        
        # Bottom 1st: Home Lineup vs Away SP
        bottom_sim = yrfi.FirstInningSim(game_data['away_sp_name'], game_data['home_lineup_names'], game_data['home_team'], game_data['home_team'])
        bottom_nr_prob = bottom_sim.simulate_half_inning()
        
        nrfi_prob = top_nr_prob * bottom_nr_prob
        yrfi_prob = 1.0 - nrfi_prob

        # 4. F5 & Quant-Elite (Full Sync)
        print(f"  [4/4] Running Outcome Engines (V20 Sync Active)...")
        away_lineup_qe = list(zip(game_data['away_lineup_names'], game_data['away_lineup_hands']))
        home_lineup_qe = list(zip(game_data['home_lineup_names'], game_data['home_lineup_hands']))
        
        qe_results = self.qe.run_v6_6_protocol(
            game_data['away_team'], game_data['home_team'],
            game_data['away_sp_name'], game_data['home_sp_name'],
            game_data['away_sp_hand'], game_data['home_sp_hand'],
            game_data['away_sp_era'], game_data['home_sp_era'],
            away_lineup_qe, home_lineup_qe,
            game_data['park_factor'], game_data['is_dome'],
            game_data['env']['Weather']['temp'], game_data['env']['Weather']['wind_speed'],
            game_data['env']['Weather']['wind_dir'], game_data['env']['Weather']['humidity'],
            game_data['env']['altitude'], game_data['env']['rain_intensity'],
            game_data['away_drs'], game_data['home_drs'],
            game_data['away_manager_hook'], game_data['home_manager_hook'],
            game_data['away_bp_pitches_d1'], game_data['away_bp_pitches_d2'],
            game_data['home_bp_pitches_d1'], game_data['home_bp_pitches_d2'],
            game_data['env']['Umpire']['zone_type'],
            game_data['away_catcher'], game_data['home_catcher'],
            game_data['game_time'])

        ar, hr, a_k, h_k = qe_results[:4]
        
        f5_results = self.f5_engine.simulate_f5(
            {'Blended': game_data['away_sp_era'], 'Name': game_data['away_sp_name'], 'Exp_IP': 6.0},
            {'Blended': game_data['home_sp_era'], 'Name': game_data['home_sp_name'], 'Exp_IP': 6.0},
            {}, {}, 100, 100, 1.0, game_id=game_id
        )

        # Reconcile K's
        away_k_rec = self.reconcile_k_projections(away_k_proj, a_k, game_data['away_sp_name'], sp_ip=game_data['away_sp_statcast'].get('IP'), sp_sc=game_data['away_sp_statcast'], side='away', game_data=game_data)
        home_k_rec = self.reconcile_k_projections(home_k_proj, h_k, game_data['home_sp_name'], sp_ip=game_data['home_sp_statcast'].get('IP'), sp_sc=game_data['home_sp_statcast'], side='home', game_data=game_data)

        # Archetype & Final Scaled Score
        n = len(ar)
        away_mu = sum(ar)/n
        home_mu = sum(hr)/n
        
        # Win probabilities
        aw = sum(1 for i in range(n) if ar[i] > hr[i])
        hw = sum(1 for i in range(n) if hr[i] > ar[i])
        ties = n - aw - hw
        apct = (aw + ties * 0.48) / n * 100
        hpct = (hw + ties * 0.52) / n * 100

        # Confidence Bands (p15/p85)
        ar_sorted = sorted(ar)
        hr_sorted = sorted(hr)
        tr_sorted = sorted([ar[i] + hr[i] for i in range(n)])
        
        p15_idx = int(n * 0.15)
        p85_idx = int(n * 0.85)

        print(f"\n-- V20 UNIFIED REPORT ---------------------------------------------------------")
        print(f"  SCORE: {game_data['away_team']} {away_mu:.2f} | {game_data['home_team']} {home_mu:.2f}")
        print(f"  YRFI: {yrfi_prob*100:.1f}% | F5: {game_data['away_team']} {f5_results['away_win_prob']:.1f}%")
        print(f"  K-SYNC: {game_data['away_sp_name']} {away_k_rec['final_k']} | {game_data['home_sp_name']} {home_k_rec['final_k']}")
        print(f"{'='*70}")

        sim_results = {
            'game_data': game_data,
            'away_mu': away_mu, 'home_mu': home_mu, 'total': away_mu + home_mu,
            'away_k': away_k_rec, 'home_k': home_k_rec,
            'hr_picks': hr_picks, 'yrfi_prob': yrfi_prob * 100,
            'f5': f5_results,
            'ar_dist': ar, 'hr_dist': hr,
            'confidence': {
                'away': [ar_sorted[p15_idx], ar_sorted[p85_idx]],
                'home': [hr_sorted[p15_idx], hr_sorted[p85_idx]],
                'total': [tr_sorted[p15_idx], tr_sorted[p85_idx]]
            },
            'win_prob': {'away': apct, 'home': hpct}
        }

        if game_data.get('absolute_mode'):
            self.generate_absolute_report(sim_results)

        if auto_record: record_simulation(game_data, sim_results, market_odds)
        return sim_results

    def generate_absolute_report(self, res):
        """Mandatory output format for MLB_ABSOLUTE_BEST_PREDICTION_LAW."""
        gd = res['game_data']
        print(f"\n{'#'*80}")
        print(f"### OMNI-PROPHET V20: ABSOLUTE BEST PREDICTION REPORT")
        print(f"{'#'*80}")

        # I. FIRST INNING PREDICTION
        yrfi_prob = res['yrfi_prob']
        call = "YES RUN" if yrfi_prob > 52 else "NO RUN"
        print(f"\nI. FIRST INNING PREDICTION")
        print(f"  Call: {call}")
        print(f"  Probability: {yrfi_prob:.1f}%")

        # II. FIRST 5 INNING SCORE PREDICTION
        f5 = res['f5']
        print(f"\nII. FIRST 5 INNING SCORE PREDICTION")
        print(f"  {gd['away_team']}: {f5['away_mu']:.2f} runs | {gd['home_team']}: {f5['home_mu']:.2f} runs")
        print(f"  Win Probability: {gd['away_team']} {f5['away_win_prob']:.1f}% | {gd['home_team']} {f5['home_win_prob']:.1f}% | Tie {f5['tie_prob']:.1f}%")
        
        # Estimate F5 Total Prob (using median as line)
        f5_total = f5['away_mu'] + f5['home_mu']
        print(f"  F5 Total Projection: {f5_total:.2f}")

        # III. STRIKEOUT PROJECTIONS (STARTING PITCHERS)
        print(f"\nIII. STRIKEOUT PROJECTIONS (STARTING PITCHERS)")
        for side in ['away', 'home']:
            name = gd[f'{side}_sp_name']
            k_rec = res[f'{side}_k']
            print(f"  {name}: {k_rec['final_k']} Ks (μ {k_rec['qe_mean']:.2f})")
            # Find a relevant line to report prob for
            line = 5.5 if k_rec['final_k'] >= 5 else 4.5
            line_str = f"{line:.1f}"
            if line_str in k_rec['k_line_probs']:
                prob = k_rec['k_line_probs'][line_str]['over']
                print(f"    Probability Over {line_str}: {prob:.1f}%")

        # IV. FINAL SCORE PREDICTIONS
        bands = res['confidence']
        print(f"\nIV. FINAL SCORE PREDICTIONS")
        print(f"  {gd['away_team']}: {res['away_mu']:.2f} [{bands['away'][0]:.1f} — {bands['away'][1]:.1f}] runs | Win Prob: {res['win_prob']['away']:.1f}%")
        print(f"  {gd['home_team']}: {res['home_mu']:.2f} [{bands['home'][0]:.1f} — {bands['home'][1]:.1f}] runs | Win Prob: {res['win_prob']['home']:.1f}%")
        print(f"  Total: {res['total']:.2f} [{bands['total'][0]:.1f} — {bands['total'][1]:.1f}]")

        # V. HOME RUN TRACKER (>25% PROBABILITY)
        print(f"\nV. HOME RUN TRACKER (>25% PROBABILITY)")
        hr_targets = [h for h in res['hr_picks'] if h['prob'] >= 0.25]
        if hr_targets:
            for h in hr_targets:
                print(f"  {h['player']} ({h['team']}): {h['prob']*100:.1f}% Probability")
        else:
            print("  No high-probability HR targets detected.")
        
        print(f"\n{'#'*80}\n")

    def _run_hr_alpha(self, game_data):
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
        return hr_picks

# Alias for easy access
OmniProphetV20Master = OmniProphetV20
