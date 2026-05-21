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
import csv
import os
import json
import unicodedata
from k_pipeline import KProphetMaster

DATA_DIR = 'data'

def normalize_name(name):
    if not name: return ""
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('utf-8')
    name = name.lower().replace('.', '').replace(',', '')
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

def run_audit():
    print("█" + "▀"*78 + "█")
    print("█ K PROPHET V10.0 — PERFORMANCE BACKTEST & CALIBRATION AUDIT                        █")
    print("█" + "▄"*78 + "█")
    print("")

    tracker_path = 'performance_tracker.csv'
    if not os.path.exists(tracker_path):
        print("Error: performance_tracker.csv not found.")
        return

    p_adv  = load_csv_mapped('pitching_advanced.csv')
    p_disc = load_csv_mapped('pitching_discipline.csv')
    p_sc   = load_csv_mapped('pitching_statcast.csv')
    p_plus = load_csv_mapped('pitching_plus.csv')
    
    overrides = {}
    if os.path.exists('overrides.json'):
        with open('overrides.json', 'r') as f:
            overrides = json.load(f).get('Pitchers', {})
    
    master = KProphetMaster()
    
    results = []
    exact_hits = 0
    within_one = 0
    total_samples = 0
    
    with open(tracker_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Type') != 'Pitcher Prop':
                continue
            name = row['Name']
            norm_name = normalize_name(name)
            try:
                actual_k = int(row['Actual'])
            except ValueError:
                continue
            
            pa = p_adv.get(norm_name, {})
            pd = p_disc.get(norm_name, {})
            ps = p_sc.get(norm_name, {})
            pp = p_plus.get(norm_name, {})
            ovr = overrides.get(name, {})
            
            pitcher_data = {
                'Name': name,
                'Hand': 'R', # Defaulting to R for historical audit unless mapped
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
            
            # Baseline Lineup (League Average)
            lineup_data = []
            for _ in range(9):
                lineup_data.append({
                    'Name': 'Average Batter',
                    'Hand': 'R',
                    'O_Swing': 30.0,
                    'Z_Contact': 85.0,
                    'K_pct': 22.7
                })
            
            env_data = {
                'Weather': {'temp': 72, 'dome': False},
                'Umpire': {'CS_pct': 16.5},
                'Catcher': {'Name': 'MISSING'},
                'ParkFactor': 1.0
            }
            
            manager_data = {'PitchLimit': ovr.get('PitchLimit', 92)}
            
            proj = master.execute_pipeline(pitcher_data, lineup_data, env_data, manager_data)
            
            pred_k = proj['exact_k']
            error = pred_k - actual_k
            
            total_samples += 1
            if pred_k == actual_k:
                exact_hits += 1
            if abs(error) <= 1:
                within_one += 1
                
            results.append({
                'name': name,
                'pred': pred_k,
                'actual': actual_k,
                'error': error,
                'mean': proj['mean_k']
            })

    # Output Results
    print(f"┌{'─'*25}┬{'─'*10}┬{'─'*10}┬{'─'*10}┬{'─'*15}┐")
    print(f"│ {'Pitcher':<23} │ {'Pred':<8} │ {'Actual':<8} │ {'Error':<8} │ {'Mean Proj':<13} │")
    print(f"├{'─'*25}┼{'─'*10}┼{'─'*10}┼{'─'*10}┼{'─'*15}┤")
    
    for r in results:
        print(f"│ {r['name']:<23} │ {r['pred']:<8} │ {r['actual']:<8} │ {r['error']:>+7}  │ {r['mean']:>13.2f} │")
        
    print(f"└{'─'*25}┴{'─'*10}┴{'─'*10}┴{'─'*10}┴{'─'*15}┘")
    
    if total_samples > 0:
        hit_rate = (exact_hits / total_samples) * 100
        within_one_rate = (within_one / total_samples) * 100
        print(f"\nFINAL METRICS:")
        print(f"  Exact Integer Hit Rate: {hit_rate:.2f}%")
        print(f"  Within +/- 1 Hit Rate:  {within_one_rate:.2f}%")
        print(f"  Total Samples Audited:  {total_samples}")
    else:
        print("\nNo valid samples found in tracker.")

if __name__ == "__main__":
    run_audit()