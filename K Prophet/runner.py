#!/usr/bin/env python3
import csv
import json
import os
import math
import unicodedata
from k_pipeline import KProphetMaster
from market_engine import MarketEngine
from games_data import GAMES

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# ── DATA LOADERS ───────────────────────────────────────────
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
        ump_data = get_data_fuzzy(ump_name, umpires) if ump_name != 'MISSING' else {'CS_pct': 16.5}
        
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
                'Pit+ FA': float(pp.get('FA', 100) or 100),
                'Pit+ SI': float(pp.get('SI', 100) or 100),
                'Pit+ SL': float(pp.get('SL', 100) or 100),
                'Pit+ CU': float(pp.get('CU', 100) or 100),
                'Pit+ CH': float(pp.get('CH', 100) or 100),
                'ShortLeash': ovr.get('ShortLeash', False),
                'TTT_Penalty': ovr.get('TTT_Penalty', 0.85)
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
            env_data = {
                'Weather': game.get('weather', {'temp': 72, 'dome': False}),
                'Umpire': {'CS_pct': float(ump_data.get('CS_pct', 16.5))},
                'Catcher': {'Name': game.get('catcher', 'MISSING')},
                'ParkFactor': game.get('park_factor', 1.0)
            }
            
            manager_data = {
                'PitchLimit': ovr.get('PitchLimit', 92)
            }
            
            live_telemetry = ovr.get('Live_Telemetry', None)
            
            proj = master.execute_pipeline(pitcher_data, lineup_data, env_data, manager_data, live_telemetry)
            
            results.append({
                'name': pitcher_name,
                'team': team_data['team'],
                'proj': proj
            })

    results.sort(key=lambda x: x['proj'].get('mean_k', 0), reverse=True)

    print("█" + "▀"*90 + "█")
    print("█ K PROPHET V10.0 — THE SINGULARITY (DETERMINISTIC REALITY ENGINE)                        █")
    print("█ Batter-Specific Vision Geometry | Archetype Synergy | Catcher Framing Logic              █")
    print("█" + "▄"*90 + "█")
    print("")
    
    for r in results:
        p = r['proj']
        name = f"{r['name']} ({r['team']})"
        print(f"┌{'─'*30}┬{'─'*60}┐")
        print(f"│ {name:<28} │ INEVITABLE K: {p['exact_k']} | Mean: {p['mean_k']:.2f} | Confidence: {p['confidence']*100:.1f}% │")
        print(f"├{'─'*30}┼{'─'*60}┤")
        
        probs = p['probabilities']
        prob_str = " | ".join([f"{line}: O {probs[line]['Over']*100:4.1f}% / U {probs[line]['Under']*100:4.1f}%" for line in [3.5, 4.5, 5.5, 6.5, 7.5]])
        print(f"│ {'Line Probabilities':<28} │ {prob_str} │")
        
        tel = p['telemetry']
        telemetry_str = f"BF: {tel['ExpectedBF']:.1f} | pK: {tel['Final_pK']:.3f} | Arch: {tel.get('Archetype', 'N/A')}"
        print(f"│ {'Telemetry':<28} │ {telemetry_str:<60} │")
        print(f"└{'─'*30}┴{'─'*60}┘")


if __name__ == "__main__":
    import sys
    idx = None
    if len(sys.argv) > 1:
        try: idx = int(sys.argv[1])
        except: pass
    main(idx)
