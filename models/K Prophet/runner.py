#!/usr/bin/env python3
import csv
import json
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import math
import unicodedata
from k_pipeline import KProphetMaster
from market_engine import MarketEngine
from games_data import GAMES

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# ── OPERATOR CONFIG (v2) ──────────────────────────────────
AUDIT_MODE = True  # Set to False to hide internal checkpoints
# ──────────────────────────────────────────────────────────
def normalize_name(name):
    """Normalize names for fuzzy matching (remove accents, suffixes, case)."""
    if not name: return ""
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('utf-8')
    name = name.lower().replace('.', '').replace(',', '')
    suffixes = [' jr', ' sr', ' ii', ' iii', ' iv']
    for s in suffixes:
        if name.endswith(s):
            name = name[:-len(s)]
    return name.strip()

def load_csv_mapped(filename, key_col='Name'):
    filepath = os.path.join(DATA_DIR, filename)
    data = {}
    if not os.path.exists(filepath): return data
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get(key_col)
            if not key: continue
            data[normalize_name(key)] = row
    return data

def get_data_fuzzy(name, dataset):
    return dataset.get(normalize_name(name), {})

# ── MAIN EXECUTION ─────────────────────────────────────────
def main(game_index=None):
    p_adv  = load_csv_mapped('pitching_advanced.csv')
    p_plus = load_csv_mapped('pitching_plus.csv')
    p_sc   = load_csv_mapped('pitching_statcast.csv')
    p_disc = load_csv_mapped('pitching_discipline.csv')
    
    b_adv  = load_csv_mapped('batting_advanced.csv')
    b_disc = load_csv_mapped('batting_discipline.csv')
    
    umpires = load_csv_mapped('umpires.csv')
    
    overrides = {}
    if os.path.exists('overrides.json'):
        with open('overrides.json', 'r') as f:
            overrides = json.load(f).get('Pitchers', {})
    
    master = KProphetMaster()
    results = []

    target_games = [GAMES[game_index]] if game_index is not None else GAMES

    for game in target_games:
        away, home = game['away'], game['home']
        ump_name = game.get('umpire', 'MISSING')
        ump_data = get_data_fuzzy(ump_name, umpires)
        if not ump_data:
            ump_data = {'CS_pct': 16.5, 'K_Factor': 1.0, 'Zone_Size': 'Neutral'}
        
        for role, team_data in [('away', away), ('home', home)]:
            pitcher_name = team_data['pitcher']
            if pitcher_name == 'TBD': continue
            
            opp_lineup_raw = home['lineup'] if role == 'away' else away['lineup']
            
            # 1. Build Pitcher Data
            pa = get_data_fuzzy(pitcher_name, p_adv)
            pd = get_data_fuzzy(pitcher_name, p_disc)
            ps = get_data_fuzzy(pitcher_name, p_sc)
            pp = get_data_fuzzy(pitcher_name, p_plus)
            ovr = overrides.get(pitcher_name, {})
            
            pitcher_data = {
                'Name': pitcher_name,
                'Hand': team_data.get('p_hand', 'R'),
                'K_pct': float(pa.get('K_pct', 22.7) or 22.7),
                'BB_pct': float(pa.get('BB_pct', 8.5) or 8.5),
                'SwStr': float(pd.get('SwStr', 11.0) or 11.0),
                'CSW': float(pd.get('CSW', 27.0) or 27.0),
                'Stuff': float(pp.get('Stuff', 100) or 100),
                'VAA': float(ps.get('VAA', -4.5) or -4.5),
                'xERA': float(ps.get('xERA', 4.0) or 4.0),
                'IP': float(pa.get('IP', 0) or 0),
                'ShortLeash': ovr.get('ShortLeash', False),
                # ── NEW QUANT FIELDS ──
                'Last_5_Pitches': ovr.get('PitchCounts', [float(pa.get('P/G', 92) or 92)]*5),
                'Tunneling_SD': ovr.get('Tunneling_SD', 1.0),
                'PlanB': ovr.get('PlanB', True), # Assume True for vets, False for some rookies
                'DSR': ovr.get('DSR', 0.10),
                'Career_Max_BF': ovr.get('Career_Max_BF', 27),
                'PPA': float(pd.get('P/PA', 3.9) or 3.9)
            }
            
            # 2. Build Lineup Data
            lineup_data = []
            for b_entry in opp_lineup_raw:
                b_name = b_entry[0]
                b_hand = b_entry[1] if len(b_entry) > 1 else 'R'
                bd = get_data_fuzzy(b_name, b_disc)
                ba = get_data_fuzzy(b_name, b_adv)
                
                lineup_data.append({
                    'Name': b_name,
                    'Hand': b_hand,
                    'O_Swing': float(bd.get('O-Swing_pct', 30.0) or 30.0),
                    'Z_Contact': float(bd.get('Z-Contact_pct', 85.0) or 85.0),
                    'K_pct': float(ba.get('K_pct', 22.7) or 22.7)
                })
                
            # 3. Environment & Manager
            weather = game.get('weather', {'temp': 72, 'dome': False})
            env_data = {
                'Weather': {
                    'temp': weather.get('temp', 72),
                    'dome': weather.get('dome', False),
                    'dew_point': weather.get('dew_point', 50),
                    'pressure': weather.get('pressure', 29.92)
                },
                'Umpire': {
                    'name': ump_name,
                    'CS_pct': float(ump_data.get('CS_pct', 16.5)),
                    'K_Factor': float(ump_data.get('K_Factor', 1.0)),
                    'Zone_Size': ump_data.get('Zone_Size', 'Neutral'),
                    'zone_type': 'neutral' if ump_data.get('Zone_Size') == 'Neutral' else ('wide' if 'Expand' in str(ump_data.get('Zone_Size')) else 'neutral')
                },
                'Catcher': {'Name': game.get('catcher', 'MISSING')},
                'ParkFactor': game.get('park_factor', 1.0),
                'Moneyline': game.get('moneyline', 0),
                'Bullpen_Unavailable': game.get('bullpen_unavailable', False),
                'Opponent_PPA': sum(b['K_pct'] for b in lineup_data)/len(lineup_data)/5.8 # Proxy
            }
            
            manager_data = {'PitchLimit': ovr.get('PitchLimit', 92)}
            live_telemetry = ovr.get('Live_Telemetry', None)
            
            proj = master.execute_pipeline(pitcher_data, lineup_data, env_data, manager_data, live_telemetry)
            
            results.append({
                'name': pitcher_name,
                'team': team_data['team'],
                'proj': proj,
                'calibration': proj.get('telemetry', {}).get('Calibration', {}),
                'flags': proj.get('telemetry', {}).get('Flags', [])
            })

    # ── STEP 7: OUTPUT ──
    print("\n" + "═"*80)
    print(" MLB K-PROJECTION MODEL — v2.0 (STRICT_QUANT_EXECUTION)")
    print(" " + "="*78)
    
    # Calibration Summary
    if results:
        cal = results[0]['proj'].get('telemetry', {}).get('Calibration', {})
        print(f" CAL SUMMARY: DBS={cal.get('DBS',0):.2f} | BF Mult={cal.get('BF_Multiplier',1.0):.2f} | Flags={', '.join(cal.get('Flags', []))}")
    print("═"*80)

    print("\n┌" + "─"*77 + "┐")
    print("│ PROJECTED STRIKEOUT MEANS (μ)                                               │")
    print("├" + "─"*26 + "┬" + "─"*19 + "┬" + "─"*30 + "┤")
    print("│ Pitcher                  │ Projected Mean (μ)│ Key Driver                   │")
    print("├" + "─"*26 + "┼" + "─"*19 + "┼" + "─"*30 + "┤")
    for r in results:
        p = r['proj']
        name = f"{r['name']} ({r['team']})"
        driver = "Stuff+ Synergy" if p['telemetry']['Final_pK'] > 0.25 else "Volume Anchor"
        if p.get('is_fragile'): driver = "FRAGILE: " + driver
        print(f"│ {name:<24} │ {p['mean_k']:<17.2f} │ {driver:<28} │")
    print("└" + "─"*26 + "┴" + "─"*19 + "┴" + "─"*30 + "┘")

    print("\n┌" + "─"*77 + "┐")
    print("│ CONVICTION SUMMARY                                                          │")
    print("├" + "─"*26 + "┬" + "─"*14 + "┬" + "─"*14 + "┬" + "─"*20 + "┤")
    print("│ Pitcher                  │ Direction    │ Conviction   │ Active Flags       │")
    print("├" + "─"*26 + "┼" + "─"*14 + "┼" + "─"*14 + "┼" + "─"*20 + "┤")
    for r in results:
        p = r['proj']
        name = f"{r['name']} ({r['team']})"
        
        # Determine Direction/Conviction based on 4.5 line (as example)
        line = 4.5
        over_p = p['probabilities'][line]['Over']
        under_p = p['probabilities'][line]['Under']
        
        direction = "Over" if over_p > under_p else "Under"
        prob = max(over_p, under_p)
        
        conviction = "NO EDGE"
        if prob >= 0.60: conviction = "HIGH"
        elif prob >= 0.56: conviction = "LEAN"
        
        if p.get('is_fragile') and conviction == "LEAN": conviction = "NO EDGE (FRG)"
        
        flags = []
        if not p.get('telemetry', {}).get('PlanB', True): flags.append('PLAN_B_MISSING')
        if p.get('is_fragile'): flags.append('FRAGILE')
        
        flag_str = ", ".join(flags[:2])
        print(f"│ {name:<24} │ {direction:<12} │ {conviction:<12} │ {flag_str:<18} │")
    print("└" + "─"*26 + "┴" + "─"*14 + "┴" + "─"*14 + "┴" + "─"*20 + "┘")

    # ── INTERNAL CHECKPOINTS (AUDIT_MODE) ──
    if AUDIT_MODE:
        print("\n" + "═"*80)
        print(" INTERNAL CHECKPOINTS (AUDIT_MODE = ON)")
        print(" " + "="*78)
        for r in results:
            p = r['proj']
            tel = p['telemetry']
            print(f"\n [AUDIT] {r['name']} ({r['team']}):")
            print(f"  - BF Anchor Applied: {tel.get('ExpectedBF', 0):.2f}")
            print(f"  - Plan B Status: {'ACTIVE' if tel.get('PlanB', True) else 'MISSING (Penalty Applied)'}")
            print(f"  - Archetype Detection: {tel.get('Archetype', 'N/A')}")
            print(f"  - Negative Binomial (r): {p.get('r', 0):.2f}")
            print(f"  - Sensitivity Drift: {'HIGH' if p.get('is_fragile') else 'STABLE'}")
            
            # Show prob distribution for the most relevant lines
            print(f"  - Distribution Detail: ", end="")
            detail = [f"{line}: {p['probabilities'][line]['Over']*100:.1f}%" for line in [4.5, 5.5, 6.5]]
            print(" | ".join(detail))
        print("═"*80)

if __name__ == "__main__":
    import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

    idx = None
    if len(sys.argv) > 1:
        try: idx = int(sys.argv[1])
        except: pass
    main(idx)


if __name__ == "__main__":
    import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

    idx = None
    if len(sys.argv) > 1:
        try: idx = int(sys.argv[1])
        except: pass
    main(idx)