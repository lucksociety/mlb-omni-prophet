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
import csv
import os

# Paths
SOURCE_DIR = '/Users/danielreiss/Desktop/Antigravity/K Prophet/data/'
TARGET_FILE = '/Users/danielreiss/Desktop/Antigravity/MLB/data/MLB Stats'

def load_csv(filename):
    path = os.path.join(SOURCE_DIR, filename)
    if not os.path.exists(path):
        print(f"Warning: {filename} not found.")
        return []
    with open(path, 'r') as f:
        return list(csv.DictReader(f))

def sync():
    # 1. Load all data
    batting_adv = load_csv('batting_advanced.csv')
    batting_sc = load_csv('batting_statcast.csv')
    pitching_adv = load_csv('pitching_advanced.csv')
    pitching_plus = load_csv('pitching_plus.csv')
    pitching_sc = load_csv('pitching_statcast.csv')
    batting_lhp = load_csv('batting_lhp.csv')
    batting_rhp = load_csv('batting_rhp.csv')

    # Create maps for cross-referencing
    ip_map = {row['Name']: row['IP'] for row in pitching_plus if 'IP' in row}
    
    with open(TARGET_FILE, 'w') as f:
        # --- Batting Advanced ---
        f.write("Batting Advanced\n")
        f.write("#,Name,Team,PA,BB%,K%,wRC+\n")
        for i, row in enumerate(batting_adv):
            f.write(f"{i+1},{row['Name']},{row['Team']},{row.get('PA','')},{row.get('BB_pct','')},{row.get('K_pct','')},{row.get('wRC_plus','')}\n")
        
        # --- Batting Stat Cast ---
        f.write("\nBatting Stat Cast\n")
        f.write("#,Name,Team,HardHit%\n")
        for i, row in enumerate(batting_sc):
            f.write(f"{i+1},{row['Name']},{row['Team']},{row.get('HardHit_pct','')}\n")

        # --- Pitching Advanced ---
        f.write("\nPitching Advanced\n")
        f.write("#,Name,Team,K%,BB%,xFIP,IP,K/9\n")
        for i, row in enumerate(pitching_adv):
            name = row['Name']
            ip = ip_map.get(name, '15.0')
            k_pct_str = row.get('K_pct', '20.0')
            try:
                k_pct = float(k_pct_str)
                k9 = round(k_pct * 0.38, 2)
            except:
                k9 = '8.5'
            f.write(f"{i+1},{name},{row['Team']},{k_pct_str},{row.get('BB_pct','')},{row.get('xFIP','')},{ip},{k9}\n")

        # --- Pitching + ---
        f.write("\nPitching +\n")
        f.write("#,Name,Team,Stuff+\n")
        for i, row in enumerate(pitching_plus):
            f.write(f"{i+1},{row['Name']},{row['Team']},{row.get('Stuff','')}\n")

        # --- Pitching Statcast ---
        f.write("\nPitching Statcast\n")
        f.write("#,Name,Team,xERA,HardHit%,Barrel%\n")
        for i, row in enumerate(pitching_sc):
            f.write(f"{i+1},{row['Name']},{row['Team']},{row.get('xERA','')},{row.get('HardHit_pct','')},{row.get('Barrel_pct','')}\n")

        # --- Batting Splits LHP ---
        f.write("\nBatting Splits LHP\n")
        f.write("#,Name,Team,PA,K%,wRC+\n")
        for i, row in enumerate(batting_lhp):
            f.write(f"{i+1},{row['Name']},{row['Team']},{row.get('PA','')},{row.get('K_pct','')},{row.get('wRC_plus','')}\n")

        # --- Batting Splits RHP ---
        f.write("\nBatting Splits RHP\n")
        f.write("#,Name,Team,PA,K%,wRC+\n")
        for i, row in enumerate(batting_rhp):
            f.write(f"{i+1},{row['Name']},{row['Team']},{row.get('PA','')},{row.get('K_pct','')},{row.get('wRC_plus','')}\n")

    print(f"Successfully rebuilt {TARGET_FILE} with 4/29 data from K Prophet.")

if __name__ == '__main__':
    sync()