import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)
#!/usr/bin/env python3
"""
K PROPHET V7.0 — DEEP DIVE PROTOCOL
===================================
V7.0 Integration: Statcast, Umpire, and Physics Overrides
"""
import math
import os
import json
from engine import KProphetEngine
from runner import load_csv, load_json, PITCHER_HANDS, STADIUM_WEATHER, PARK_K_FACTOR, nb_prob, over_under_prob
from games_data import GAMES

def main():
    # Load All Data
    p_adv  = load_csv('pitching_advanced.csv')
    p_plus = load_csv('pitching_plus.csv')
    p_sc   = load_csv('pitching_statcast.csv')
    
    b_adv  = load_csv('batting_advanced.csv')
    b_lhp  = load_csv('batting_lhp.csv')
    b_rhp  = load_csv('batting_rhp.csv')
    b_sc   = load_csv('batting_statcast.csv')
    
    umpires = load_csv('umpires.csv')
    overrides = load_json('overrides.json').get('Pitchers', {})
    
    engine = KProphetEngine()

    # Deep Dive into Game 1 (or allow selection)
    game_idx = 0
    game = GAMES[game_idx]
    away, home = game['away'], game['home']
    home_team = home['team']
    ump_name = game.get('umpire', 'MISSING')
    ump_data = umpires.get(ump_name, umpires.get('MISSING'))

    print("=" * 80)
    print(f"  K PROPHET V7.0 — GAME DEEP DIVE: {away['team']} @ {home['team']}")
    print(f"  Umpire: {ump_name} (K-Factor: {ump_data.get('K_Factor', '1.00')})")
    print("=" * 80)

    for role, team_data in [('AWAY', away), ('HOME', home)]:
        pitcher = team_data['pitcher']
        if pitcher == 'TBD': continue
        
        p_hand = PITCHER_HANDS.get(pitcher, "RHP")
        opp_lineup = (home if role == 'AWAY' else away)['lineup']
        
        p_bundle = {
            'adv': p_adv.get(pitcher, {}),
            'plus': p_plus.get(pitcher, {}),
            'sc': p_sc.get(pitcher, {})
        }
        b_bundle = {'adv': b_adv, 'lhp': b_lhp, 'rhp': b_rhp, 'sc': b_sc}
        env = {
            'Umpire': ump_data,
            'Weather': STADIUM_WEATHER.get(home_team, {"temp": 70, "dome": False}),
            'ParkFactor': PARK_K_FACTOR.get(home_team, 1.0)
        }
        p_overrides = overrides.get(pitcher)
        
        proj = engine.project(pitcher, p_hand, p_bundle, opp_lineup, b_bundle, env, p_overrides)
        mu, r = proj['mu'], proj['r']

        print(f"\n{'━' * 80}")
        print(f"  {role} PITCHER: {pitcher} ({team_data['team']})")
        print(f"  Hand: {p_hand} | Base K%: {p_bundle['adv'].get('K_pct', '---')}% | Stuff+: {p_bundle['plus'].get('Stuff', '---')}")
        print(f"{'━' * 80}")

        # Batter breakdown
        print(f"\n  ┌─ LINEUP BREAKDOWN (vs {pitcher}) ───────────────────")
        print(f"  │  {'#':<3} {'Batter':<22} {'K%':<8} {'xwOBA':<8} {'Verdict'}")
        print(f"  │  {'─'*3} {'─'*22} {'─'*8} {'─'*8} {'─'*12}")

        split_data = b_lhp if p_hand == "LHP" else b_rhp
        for i, b_entry in enumerate(opp_lineup, 1):
            name = b_entry[0] if isinstance(b_entry, (list, tuple)) else b_entry
            bd = split_data.get(name) or b_adv.get(name, {})
            bsc = b_sc.get(name, {})
            
            bk = float(bd.get('K_pct', 22.7) or 22.7)
            xw = float(bsc.get('xwOBA', 0.320) or 0.320)
            
            verdict = "⚪ NEUTRAL"
            if bk > 28: verdict = "🔴 K-PRONE"
            elif bk < 15: verdict = "🟢 K-RESIST"
            
            print(f"  │  {i:<3} {name:<22} {bk:>5.1f}% | {xw:>5.3f} | {verdict}")
        print(f"  └─────────────────────────────────────────────────────────")

        print(f"\n  PROJECTION SUMMARY:")
        print(f"  ► Mean (μ):       {mu:.2f}")
        print(f"  ► Adj K%:         {proj['k_pct']}%")
        print(f"  ► Drivers:        {', '.join(proj['flags']) if proj['flags'] else 'Baseline'}")
        
        print(f"\n  O/U PROBABILITIES (r={r}):")
        for line in [3.5, 4.5, 5.5, 6.5]:
            over_p, under_p, _ = over_under_prob(line, mu, r)
            side = "OVER" if over_p >= 0.5 else "UNDER"
            pct = over_p if over_p >= 0.5 else under_p
            print(f"    {line}: {side:<6} {pct*100:>5.1f}%")

if __name__ == "__main__":
    main()