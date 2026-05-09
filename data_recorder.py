#!/usr/bin/env python3
"""
MLB DATA RECORDER — AUTOMATIC PERSISTENCE FOR OMNI-PROPHET V18.0
Records all simulation inputs, outputs, and post-game results to:
  - predictions_history.csv      (game scores, ML direction)
  - K Prophet/performance_tracker.csv  (K-prop predictions)
  - audits/                      (full JSON audit trails per game)
  - intelligence/                (matchup research reports)
"""
import csv
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICTIONS_CSV = os.path.join(BASE_DIR, 'predictions_history.csv')
K_TRACKER_CSV = os.path.join(BASE_DIR, 'K Prophet', 'performance_tracker.csv')
AUDITS_DIR = os.path.join(BASE_DIR, 'audits')
INTELLIGENCE_DIR = os.path.join(BASE_DIR, 'intelligence')

# Ensure directories exist
os.makedirs(AUDITS_DIR, exist_ok=True)
os.makedirs(INTELLIGENCE_DIR, exist_ok=True)

PREDICTIONS_HEADERS = [
    'Date', 'Away_Team', 'Home_Team',
    'Pred_Away_Score', 'Pred_Home_Score', 'Pred_Total',
    'Calibrated_Total', 'Cal_Modifier',
    'Away_Win_Pct', 'Home_Win_Pct', 'ML_Edge',
    'Away_CI_Low', 'Away_CI_High', 'Home_CI_Low', 'Home_CI_High',
    'Total_CI_Low', 'Total_CI_High', 'Blowout_Pct', 'YRFI_Prob',
    'Away_SP', 'Home_SP',
    'Away_K_Pred', 'Home_K_Pred',
    'Away_K_Status', 'Home_K_Status',
    'Ace_Traps', 'Park_Factor', 'Umpire', 'Umpire_Zone',
    'Temp', 'Wind_Speed', 'Wind_Dir', 'Humidity',
    'Engine_Version',
    'Result_Away_Score', 'Result_Home_Score', 'Result_Winner', 'Result_Total',
]

K_TRACKER_HEADERS = [
    'Date', 'Type', 'Matchup', 'Name',
    'Projection', 'KP_Median', 'KP_Mean', 'QE_Median', 'QE_Mean',
    'Reconciliation', 'Confidence',
    'Actual', 'Bet', 'Odds', 'Result', 'PNL',
]


def _ensure_csv_headers(filepath, headers):
    """Create CSV with headers if it doesn't exist, or verify header compatibility."""
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        return True
    return False


def record_simulation(game_data, sim_results, market_odds=None):
    """
    Record a complete simulation run. Called automatically by omni_prophet_v15.py.

    Args:
        game_data: The full game_data dict passed to the simulation
        sim_results: The dict returned by run_omni_simulation()
        market_odds: Optional dict of market odds used

    Returns:
        dict with paths to all recorded files
    """
    if sim_results is None:
        print("  [RECORDER] No results to record (simulation may have been aborted).")
        return None

    date_str = datetime.now().strftime('%Y-%m-%d')
    matchup = f"{game_data['away_team']}@{game_data['home_team']}"
    recorded_files = {}

    # ── 1. APPEND TO predictions_history.csv ────────────────────
    _record_predictions_csv(game_data, sim_results, date_str)
    recorded_files['predictions_csv'] = PREDICTIONS_CSV

    # ── 2. APPEND TO K Prophet/performance_tracker.csv ──────────
    _record_k_tracker(game_data, sim_results, date_str, matchup)
    recorded_files['k_tracker_csv'] = K_TRACKER_CSV

    # ── 3. WRITE FULL AUDIT JSON ────────────────────────────────
    audit_path = _record_audit_json(game_data, sim_results, date_str, matchup, market_odds)
    recorded_files['audit_json'] = audit_path

    # ── 4. WRITE INTELLIGENCE REPORT ────────────────────────────
    intel_path = _record_intelligence_report(game_data, sim_results, date_str)
    recorded_files['intelligence_report'] = intel_path

    print(f"\n── DATA RECORDER ───────────────────────────────────────────────")
    print(f"  ✅ predictions_history.csv  — game score prediction appended")
    print(f"  ✅ performance_tracker.csv  — K-prop predictions appended")
    print(f"  ✅ audits/{os.path.basename(audit_path)}  — full audit trail saved")
    print(f"  ✅ intelligence/{os.path.basename(intel_path)}  — intel report saved")
    print(f"  📝 Run 'python3 record_results.py' after game to enter actuals")

    return recorded_files


def _record_predictions_csv(game_data, results, date_str):
    """Append game-level prediction to predictions_history.csv."""
    away = game_data['away_team']
    home = game_data['home_team']
    fav = away if results['win_prob']['away'] > results['win_prob']['home'] else home
    ace_trap_str = '; '.join(results.get('ace_traps', {}).keys()) or 'None'

    ci = results.get('confidence', {})
    away_ci = ci.get('away', (0, 0))
    home_ci = ci.get('home', (0, 0))
    total_ci = ci.get('total', (0, 0))

    row = {
        'Date': date_str,
        'Away_Team': away,
        'Home_Team': home,
        'Pred_Away_Score': f"{results['away_mu']:.2f}",
        'Pred_Home_Score': f"{results['home_mu']:.2f}",
        'Pred_Total': f"{results['away_mu'] + results['home_mu']:.2f}",
        'Calibrated_Total': f"{results['total']:.2f}",
        'Cal_Modifier': f"{results['total'] - (results['away_mu'] + results['home_mu']):.2f}",
        'Away_Win_Pct': f"{results['win_prob']['away']:.1f}",
        'Home_Win_Pct': f"{results['win_prob']['home']:.1f}",
        'ML_Edge': fav,
        'Away_CI_Low': away_ci[0], 'Away_CI_High': away_ci[1],
        'Home_CI_Low': home_ci[0], 'Home_CI_High': home_ci[1],
        'Total_CI_Low': total_ci[0], 'Total_CI_High': total_ci[1],
        'Blowout_Pct': f"{results.get('blowout_prob', 0):.1f}",
        'YRFI_Prob': f"{results.get('yrfi_prob', 0):.1f}",
        'Away_SP': game_data.get('away_sp_name', ''),
        'Home_SP': game_data.get('home_sp_name', ''),
        'Away_K_Pred': results['away_k']['final_k'],
        'Home_K_Pred': results['home_k']['final_k'],
        'Away_K_Status': results['away_k']['status'],
        'Home_K_Status': results['home_k']['status'],
        'Ace_Traps': ace_trap_str,
        'Park_Factor': game_data.get('park_factor', ''),
        'Umpire': game_data.get('env', {}).get('Umpire', {}).get('name', ''),
        'Umpire_Zone': game_data.get('env', {}).get('Umpire', {}).get('zone_type', ''),
        'Temp': game_data.get('env', {}).get('Weather', {}).get('temp', ''),
        'Wind_Speed': game_data.get('env', {}).get('Weather', {}).get('wind_speed', ''),
        'Wind_Dir': game_data.get('env', {}).get('Weather', {}).get('wind_dir', ''),
        'Humidity': game_data.get('env', {}).get('Weather', {}).get('humidity', ''),
        'Engine_Version': 'V15.0',
        'Result_Away_Score': '', 'Result_Home_Score': '',
        'Result_Winner': '', 'Result_Total': '',
    }

    file_exists = os.path.exists(PREDICTIONS_CSV)
    with open(PREDICTIONS_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=PREDICTIONS_HEADERS, extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def _record_k_tracker(game_data, results, date_str, matchup):
    """Append K-prop predictions to K Prophet/performance_tracker.csv."""
    rows = []
    for side, sp_key in [('away', 'away_k'), ('home', 'home_k')]:
        k_rec = results[sp_key]
        rows.append({
            'Date': date_str,
            'Type': 'Pitcher Prop',
            'Matchup': matchup,
            'Name': game_data.get(f'{side}_sp_name', ''),
            'Projection': f"{k_rec['kp_mean']:.2f}",
            'KP_Median': k_rec['kp_median'],
            'KP_Mean': f"{k_rec['kp_mean']:.2f}",
            'QE_Median': k_rec['qe_median'],
            'QE_Mean': f"{k_rec['qe_mean']:.2f}",
            'Reconciliation': k_rec['status'],
            'Confidence': k_rec['confidence'],
            'Actual': 'TBD',
            'Bet': 'TBD',
            'Odds': 'TBD',
            'Result': 'TBD',
            'PNL': '0.0',
        })

    # Append to existing tracker (preserving original format for backward compat)
    with open(K_TRACKER_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=K_TRACKER_HEADERS, extrasaction='ignore')
        for row in rows:
            writer.writerow(row)


def _record_audit_json(game_data, results, date_str, matchup, market_odds):
    """Write complete audit trail as JSON for future analysis."""
    audit = {
        'metadata': {
            'engine_version': 'OMNI-PROPHET V15.0',
            'timestamp': datetime.now().isoformat(),
            'date': date_str,
            'matchup': matchup,
        },
        'inputs': {
            'away_team': game_data.get('away_team'),
            'home_team': game_data.get('home_team'),
            'away_sp': {
                'name': game_data.get('away_sp_name'),
                'hand': game_data.get('away_sp_hand'),
                'era': game_data.get('away_sp_era'),
                'statcast': game_data.get('away_sp_statcast', {}),
            },
            'home_sp': {
                'name': game_data.get('home_sp_name'),
                'hand': game_data.get('home_sp_hand'),
                'era': game_data.get('home_sp_era'),
                'statcast': game_data.get('home_sp_statcast', {}),
            },
            'away_lineup': game_data.get('away_lineup_names', []),
            'home_lineup': game_data.get('home_lineup_names', []),
            'environment': game_data.get('env', {}),
            'park_factor': game_data.get('park_factor'),
            'is_dome': game_data.get('is_dome'),
            'game_time': game_data.get('game_time'),
            'operational': {
                'away_drs': game_data.get('away_drs'),
                'home_drs': game_data.get('home_drs'),
                'away_manager_hook': game_data.get('away_manager_hook'),
                'home_manager_hook': game_data.get('home_manager_hook'),
                'away_bp_pitches_d1': game_data.get('away_bp_pitches_d1'),
                'away_bp_pitches_d2': game_data.get('away_bp_pitches_d2'),
                'home_bp_pitches_d1': game_data.get('home_bp_pitches_d1'),
                'home_bp_pitches_d2': game_data.get('home_bp_pitches_d2'),
                'away_catcher': game_data.get('away_catcher'),
                'home_catcher': game_data.get('home_catcher'),
            },
            'market_odds': market_odds,
        },
        'outputs': {
            'score_projection': {
                'away_mu': results['away_mu'],
                'home_mu': results['home_mu'],
                'total_raw': results['away_mu'] + results['home_mu'],
                'total_calibrated': results['total'],
                'yrfi_prob': results.get('yrfi_prob'),
            },
            'win_probability': results['win_prob'],
            'confidence_bands': {
                'away_p15_p85': list(results['confidence']['away']),
                'home_p15_p85': list(results['confidence']['home']),
                'total_p15_p85': list(results['confidence']['total']),
            },
            'k_projections': {
                'away': results['away_k'],
                'home': results['home_k'],
            },
            'hr_picks': results.get('hr_picks', []),
            'ace_traps': results.get('ace_traps', {}),
        },
        'results': {
            'status': 'PENDING',
            'away_score': None,
            'home_score': None,
            'winner': None,
            'total': None,
            'away_sp_k_actual': None,
            'home_sp_k_actual': None,
        },
    }

    filename = f"audit_{game_data['away_team']}_{game_data['home_team']}_{date_str}.json"
    filepath = os.path.join(AUDITS_DIR, filename)

    # Handle multiple sims for same matchup (append index)
    counter = 1
    while os.path.exists(filepath):
        counter += 1
        filename = f"audit_{game_data['away_team']}_{game_data['home_team']}_{date_str}_{counter}.json"
        filepath = os.path.join(AUDITS_DIR, filename)

    with open(filepath, 'w') as f:
        json.dump(audit, f, indent=2, default=str)

    return filepath


def _record_intelligence_report(game_data, results, date_str):
    """Generate a structured intelligence report markdown file."""
    away = game_data['away_team']
    home = game_data['home_team']
    filename = f"matchup_{away}_{home}_{date_str}.md"
    filepath = os.path.join(INTELLIGENCE_DIR, filename)

    # V16.0: Overwrite report with latest simulation results
    # (Removed existence check)

    away_k = results['away_k']
    home_k = results['home_k']
    ci = results.get('confidence', {})
    env = game_data.get('env', {})
    weather = env.get('Weather', {})

    lines = [
        f"# Intelligence Report: {away} @ {home}",
        f"**Date**: {date_str}",
        f"**Engine**: OMNI-PROPHET V18.0",
        f"**Status**: SIMULATION COMPLETE",
        "",
        "## 1. Starting Pitchers",
        f"- **Away SP**: {game_data.get('away_sp_name', '?')} ({game_data.get('away_sp_hand', '?')}) — ERA: {game_data.get('away_sp_era', '?')}",
        f"  - Stuff+: {game_data.get('away_sp_statcast', {}).get('Stuff', 'N/A')} | VAA: {game_data.get('away_sp_statcast', {}).get('VAA', 'N/A')} | xERA: {game_data.get('away_sp_statcast', {}).get('xERA', 'N/A')}",
        f"- **Home SP**: {game_data.get('home_sp_name', '?')} ({game_data.get('home_sp_hand', '?')}) — ERA: {game_data.get('home_sp_era', '?')}",
        f"  - Stuff+: {game_data.get('home_sp_statcast', {}).get('Stuff', 'N/A')} | VAA: {game_data.get('home_sp_statcast', {}).get('VAA', 'N/A')} | xERA: {game_data.get('home_sp_statcast', {}).get('xERA', 'N/A')}",
        "",
        "## 2. Score Projection",
        f"- {away}: **{results['away_mu']:.2f}** [{ci.get('away', ('?','?'))[0]} — {ci.get('away', ('?','?'))[1]}] runs ({results['win_prob']['away']:.1f}%)",
        f"- {home}: **{results['home_mu']:.2f}** [{ci.get('home', ('?','?'))[0]} — {ci.get('home', ('?','?'))[1]}] runs ({results['win_prob']['home']:.1f}%)",
        f"- Total: **{results['total']:.2f}** [{ci.get('total', ('?','?'))[0]} — {ci.get('total', ('?','?'))[1]}]",
        f"- YRFI Prob: **{results.get('yrfi_prob', 0):.1f}%**",
        "",
        "## 3. K Projections (Reconciled)",
        f"- {game_data.get('away_sp_name', '?')}: **{away_k['final_k']} K's** [{away_k['status']}] (KP: {away_k['kp_median']}, QE: {away_k['qe_median']})",
        f"  - Volatility: {', '.join(away_k.get('volatility_flags', [])) or 'None'}",
        f"- {game_data.get('home_sp_name', '?')}: **{home_k['final_k']} K's** [{home_k['status']}] (KP: {home_k['kp_median']}, QE: {home_k['qe_median']})",
        f"  - Volatility: {', '.join(home_k.get('volatility_flags', [])) or 'None'}",
        "",
        "## 4. Environment",
        f"- Park Factor: {game_data.get('park_factor', 'N/A')} | Dome: {game_data.get('is_dome', 'N/A')}",
        f"- Weather: {weather.get('temp', '?')}°F, {weather.get('wind_speed', '?')}mph wind @ {weather.get('wind_dir', '?')}°, {weather.get('humidity', '?')}% humidity",
        f"- Umpire: {env.get('Umpire', {}).get('name', '?')} ({env.get('Umpire', {}).get('zone_type', '?')})",
        "",
        "## 5. Risk Factors",
    ]

    traps = results.get('ace_traps', {})
    if traps:
        for pitcher, flags in traps.items():
            lines.append(f"- 🚨 **ACE TRAP ({pitcher})**: {', '.join(flags)}")
    
    disaster_traps = results.get('disaster_traps', [])
    if disaster_traps:
        for d in disaster_traps:
            lines.append(f"- ⚠️ **DISASTER TRAP**: {d}")

    if not traps and not disaster_traps:
        lines.append("- No significant risk factors detected")

    lines.extend([
        "",
        "## 6. Post-Game Results",
        "- **Status**: PENDING",
        f"- Away Score ({away}): ___",
        f"- Home Score ({home}): ___",
        f"- {game_data.get('away_sp_name', '?')} K Actual: ___",
        f"- {game_data.get('home_sp_name', '?')} K Actual: ___",
        "",
        "---",
        f"*Generated by OMNI-PROPHET V18.0 at {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
    ])

    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))

    return filepath
