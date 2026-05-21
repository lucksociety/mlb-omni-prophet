#!/usr/bin/env python3
"""
MLB OMNI-PROPHET V15.0 — CALIBRATED FORENSIC ARCHITECTURE
Fixes: V14 + Calibration Loop, K-Reconciliation, Ace Traps, Confidence Bands,
       Kelly/EV Betting Output, Pre-flight Checks, Opener Detection.
"""
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)
import json, math, statistics
from datetime import datetime




try:
    from engine import KProphetEngine
    from hr_model import HRModel
    import quant_elite_v6_5 as qe
    from calibration_check import run_calibration_check
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

class OmniProphetV15:
    def __init__(self):
        self.k_engine = KProphetEngine()
        self.hr_engine = HRModel(os.path.join(os.path.dirname(__file__), "HR/MLB Stats"))
        self.qe = qe
        self.calibration = None

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

        # Opener detection
        for side in ['away', 'home']:
            sc = game_data.get(f'{side}_sp_statcast', {})
            if sc.get('IP', 100) < 15:  # < 3 IP avg over 5 starts
                warnings.append(f"⚠ {side.upper()} SP {game_data.get(f'{side}_sp_name', '?')} has only {sc.get('IP', 0)} IP — possible OPENER. Consider ShortLeash override.")

        print(f"\n── PRE-FLIGHT CHECK ─────────────────────────────────────────────")
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

            if sp_sc.get('xERA', 4.0) - sp_era > 0.80:
                flags.append(f"xERA {sp_sc['xERA']:.2f} >> ERA {sp_era:.2f} (regression due)")

            ws = env.get('Weather', {}).get('wind_speed', 0)
            wd = env.get('Weather', {}).get('wind_dir', 90)
            if pf > 105 and ws > 10 and abs(wd) < 45:
                flags.append(f"PF {pf} + wind out {ws}mph")

            if env.get('Umpire', {}).get('zone_type') == 'tight':
                flags.append("Tight umpire zone (walk risk)")

            if len(flags) >= 2:
                traps[game_data.get(f'{side}_sp_name', '?')] = flags
        return traps

    # ── K-PROPHET RECONCILIATION ───────────────────────────────
    def reconcile_k_projections(self, kp_result, qe_k_dist, sp_name):
        """Reconcile K-Prophet and QE K distributions."""
        kp_median = kp_result['exact_k']
        kp_mean = kp_result['mean_k']
        qe_median = int(statistics.median(qe_k_dist))
        qe_mean = statistics.mean(qe_k_dist)

        diff = abs(kp_median - qe_median)
        if diff <= 1:
            status = 'ALIGNED'
            final_k = kp_median  # Trust K-Prophet when aligned
            confidence = 'HIGH'
        else:
            status = 'SPLIT_SIGNAL'
            final_k = round(kp_median * 0.6 + qe_median * 0.4)
            confidence = 'LOW'

        return {
            'final_k': final_k,
            'kp_median': kp_median, 'kp_mean': kp_mean,
            'qe_median': qe_median, 'qe_mean': qe_mean,
            'status': status, 'confidence': confidence,
            'delta': diff,
        }

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
        """Full V15.0 simulation pipeline."""
        print(f"\n{'='*70}")
        print(f"  OMNI-PROPHET V15.0 | CALIBRATED FORENSIC ENGINE")
        print(f"  {game_data['away_team']} @ {game_data['home_team']} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*70}")

        # Phase 0: Calibration
        cal = self.run_calibration()

        # Phase 1.5: Pre-flight
        if not self.preflight_check(game_data):
            print("\n  ⛔ SIMULATION ABORTED — Fix pre-flight errors.")
            return None

        # Phase 2A: K-Prophet
        print(f"\n  [1/3] Running K-Prophet V11.0 Engine...")
        away_k_proj = self.k_engine.project(
            game_data['away_sp_statcast'], game_data['home_lineup_statcast'],
            game_data['env'], game_data.get('away_sp_overrides'))
        home_k_proj = self.k_engine.project(
            game_data['home_sp_statcast'], game_data['away_lineup_statcast'],
            game_data['env'], game_data.get('home_sp_overrides'))

        # Phase 2A: HR-Alpha
        print(f"  [2/3] Running HR-Alpha Engine...")
        hr_picks = self._run_hr_alpha(game_data)

        # Phase 2A: Quant-Elite
        print(f"  [3/3] Running Quant-Elite V6.5 Score Engine...")
        away_lineup_qe = list(zip(game_data['away_lineup_names'], game_data['away_lineup_hands']))
        home_lineup_qe = list(zip(game_data['home_lineup_names'], game_data['home_lineup_hands']))

        ar, hr, a_k, h_k = self.qe.run_v6_5_protocol(
            game_data['away_team'], game_data['home_team'],
            game_data['away_sp_name'], game_data['home_sp_name'],
            game_data['away_sp_hand'], game_data['home_sp_hand'],
            game_data['away_sp_era'], game_data['home_sp_era'],
            away_lineup_qe, home_lineup_qe,
            game_data['park_factor'], game_data['is_dome'],
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
            game_data['game_time'])

        # Phase 2B: K-Reconciliation
        away_k_rec = self.reconcile_k_projections(away_k_proj, a_k, game_data['away_sp_name'])
        home_k_rec = self.reconcile_k_projections(home_k_proj, h_k, game_data['home_sp_name'])

        # Phase 2C: Calibration Application
        n = len(ar)
        away_mu = sum(ar) / n
        home_mu = sum(hr) / n
        total_mu = away_mu + home_mu
        cal_modifier = cal.get('total_modifier', 0.0)
        calibrated_total = total_mu + cal_modifier

        # Confidence Bands (p15/p85)
        ar_sorted = sorted(ar)
        hr_sorted = sorted(hr)
        tr_sorted = sorted([ar[i] + hr[i] for i in range(n)])
        p15_idx = int(n * 0.15)
        p85_idx = int(n * 0.85)

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
        print(f"  OMNI-PROPHET V15.0 | FORENSIC INTELLIGENCE REPORT")
        print(f"{'='*70}")

        # 3.1 Score Projection with Confidence Bands
        print(f"\n── 1. SCORE PROJECTION (Calibrated) ────────────────────────────")
        print(f"  {game_data['away_team']}: {away_mu:.2f} [{ar_sorted[p15_idx]} — {ar_sorted[p85_idx]}] runs ({apct:.1f}%)")
        print(f"  {game_data['home_team']}: {home_mu:.2f} [{hr_sorted[p15_idx]} — {hr_sorted[p85_idx]}] runs ({hpct:.1f}%)")
        print(f"  TOTAL: {calibrated_total:.2f} [{tr_sorted[p15_idx]} — {tr_sorted[p85_idx]}]")
        if cal_modifier != 0:
            print(f"  (Raw: {total_mu:.2f} + Calibration: {cal_modifier:+.2f})")
        print(f"  BLOWOUT PROB (>13 runs): {blowout_prob:.1f}%")

        # 3.2 K-Prophet Reconciled
        print(f"\n── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────")
        for sp_name, rec in [(game_data['away_sp_name'], away_k_rec), (game_data['home_sp_name'], home_k_rec)]:
            status_icon = "✅" if rec['status'] == 'ALIGNED' else "⚠️"
            print(f"  {sp_name}: {rec['final_k']} K's {status_icon} [{rec['status']}]")
            print(f"    K-Prophet: {rec['kp_median']} (μ {rec['kp_mean']:.2f}) | QE: {rec['qe_median']} (μ {rec['qe_mean']:.2f}) | Δ={rec['delta']}")

        # 3.3 HR-Alpha
        print(f"\n── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────")
        high_conv = [h for h in hr_picks if h['prob'] >= 0.25]
        if not high_conv:
            print("  [NONE DETECTED]")
        for h in high_conv:
            print(f"  🔥 {h['player']} ({h['team']}): {h['prob']*100:.1f}%")

        # 3.4 Ace Traps
        print(f"\n── 4. ACE TRAP SCAN ────────────────────────────────────────────")
        if ace_traps:
            for pitcher, flags in ace_traps.items():
                print(f"  🚨 ACE TRAP: {pitcher}")
                for f in flags:
                    print(f"    → {f}")
        else:
            print("  [NO ACE TRAPS DETECTED]")

        # 3.5 Betting Intelligence
        print(f"\n── 5. BETTING INTELLIGENCE ─────────────────────────────────────")
        run_diff = abs(away_mu - home_mu)
        fav = game_data['away_team'] if away_mu > home_mu else game_data['home_team']
        fav_pct = max(apct, hpct)

        if market_odds:
            for label, odds_val in market_odds.items():
                imp = self.implied_prob(odds_val) * 100
                dec = self.american_to_decimal(odds_val)
                if 'away' in label.lower() or game_data['away_team'].lower() in label.lower():
                    model_p = apct / 100
                else:
                    model_p = hpct / 100
                edge = (model_p * 100) - imp
                kelly = self.calc_kelly(model_p, dec)
                verdict = "BET" if edge > 3.0 else ("LEAN" if edge > 1.0 else "NO EDGE")
                if ace_traps and verdict == "BET":
                    verdict = "BET (⚠ Ace Trap Active)"
                print(f"  MARKET: {label} @ {odds_val:+d} (implied {imp:.1f}%)")
                print(f"  MODEL:  {model_p*100:.1f}% | EDGE: {edge:+.1f}% | KELLY: {kelly*100:.2f}%")
                print(f"  VERDICT: {verdict}")
                print()
        else:
            if run_diff < 0.5:
                print(f"  [TOSS-UP] Run Diff {run_diff:.2f} < 0.5. FADE MONEYLINE. Focus totals/props.")
            elif run_diff >= 1.4:
                print(f"  [MASSIVE EDGE] Run Diff {run_diff:.2f}. CONSIDER RUNLINE (-1.5) {fav} ({fav_pct:.1f}%)")
            else:
                print(f"  [EDGE] Run Diff {run_diff:.2f}. CONSIDER ML {fav} ({fav_pct:.1f}%)")
            print(f"  (Provide market_odds dict for full Kelly/EV analysis)")

        # Telemetry
        print(f"\n── 6. TELEMETRY ────────────────────────────────────────────────")
        print(f"  ADI: {game_data['env'].get('adi', 'N/A')} | PF: {game_data['park_factor']}")
        print(f"  Umpire: {game_data['env']['Umpire']['name']} ({game_data['env']['Umpire']['zone_type']})")
        print(f"  Calibration: Total {cal.get('total_bias','N/A')} | K {cal.get('k_bias','N/A')}")
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
        }

        # ── AUTO-RECORD ALL DATA ───────────────────────────────
        if auto_record:
            try:
                record_simulation(game_data, sim_results, market_odds)
            except Exception as e:
                print(f"  ⚠ DATA RECORDER ERROR: {e} — simulation results still valid")

        return sim_results

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