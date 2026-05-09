#!/usr/bin/env python3
"""Audit script V4.0: check data quality for advanced Statcast and Umpire metrics."""

from runner import load_csv, load_json
from games_data import GAMES

def main():
    p_adv  = load_csv('pitching_advanced.csv')
    p_plus = load_csv('pitching_plus.csv')
    p_sc   = load_csv('pitching_statcast.csv')
    umpires = load_csv('umpires.csv')
    overrides = load_json('overrides.json').get('Pitchers', {})

    print("=" * 80)
    print("K PROPHET V7.0 DATA QUALITY AUDIT")
    print("=" * 80)

    all_pitchers = set()
    for game in GAMES:
        if game['away']['pitcher'] != 'TBD': all_pitchers.add(game['away']['pitcher'])
        if game['home']['pitcher'] != 'TBD': all_pitchers.add(game['home']['pitcher'])

    print(f"\nAnalyzing {len(all_pitchers)} Pitchers:")
    for p in sorted(all_pitchers):
        adv = p_adv.get(p)
        plus = p_plus.get(p)
        sc = p_sc.get(p)
        ovr = overrides.get(p)

        status = []
        if adv: status.append("Adv ✓")
        else: status.append("Adv ✗")
        
        if plus: status.append("Plus ✓")
        else: status.append("Plus ✗")
        
        if sc: status.append("Statcast ✓")
        else: status.append("Statcast ✗")
        
        if ovr: status.append("Ovr ✓")
        else: status.append("Ovr ---")

        k_pct = adv.get('K_pct', '---') if adv else '---'
        stuff = plus.get('Stuff', '---') if plus else '---'
        xera = sc.get('xERA', '---') if sc else '---'
        
        print(f"  {p:<25} | {' '.join(status):<30} | K%:{k_pct:>5} | Stuff:{stuff:>4} | xERA:{xera:>4}")

    print("\n" + "=" * 80)
    print("UMPIRE AUDIT")
    print("=" * 80)
    for game in GAMES:
        ump_name = game.get('umpire', 'MISSING')
        ump_data = umpires.get(ump_name)
        status = "✓" if ump_data else "✗ NOT FOUND (Using Neutral)"
        k_factor = ump_data.get('K_Factor', '1.00') if ump_data else '1.00'
        print(f"  {game['away']['team']} @ {game['home']['team']:<15} | Ump: {ump_name:<18} | Status: {status:<20} | K-Factor: {k_factor}")

if __name__ == "__main__":
    main()
