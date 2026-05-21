#!/usr/bin/env python3
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import csv
import json
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)


# Add current dir to path to import local modules
sys.path.append(os.path.dirname(__file__))

def check_files():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    required_csvs = [
        'pitching_advanced.csv',
        'pitching_plus.csv',
        'pitching_statcast.csv',
        'pitching_discipline.csv',
        'batting_advanced.csv',
        'batting_lhp.csv',
        'batting_rhp.csv',
        'batting_statcast.csv',
        'batting_discipline.csv',
        'umpires.csv'
    ]
    required_jsons = ['overrides.json']
    
    all_ok = True
    print("--- File Integrity Check ---")
    for f in required_csvs:
        path = os.path.join(data_dir, f)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {f} found ({size} bytes)")
        else:
            print(f"❌ {f} MISSING")
            all_ok = False
            
    for f in required_jsons:
        path = os.path.join(data_dir, f)
        if os.path.exists(path):
            print(f"✅ {f} found")
        else:
            print(f"❌ {f} MISSING")
            all_ok = False
            
    return all_ok

def check_logic():
    print("\n--- Engine & Games Check ---")
    try:
        from games_data import GAMES
        print(f"✅ games_data.py loaded, {len(GAMES)} games found.")
    except Exception as e:
        print(f"❌ Failed to load games_data.py: {e}")
        return False
        
    try:
        from engine import KProphetEngine
        engine = KProphetEngine()
        print("✅ engine.py loaded and initialized.")
    except Exception as e:
        print(f"❌ Failed to load engine.py: {e}")
        return False
        
    return True

def run_test_projection():
    print("\n--- Running Test Projection ---")
    try:
        import runner
        # Mocking the runner's main loop for one game
        runner.main()
        print("\n✅ Runner executed successfully.")
        return True
    except Exception as e:
        print(f"\n❌ Runner failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    files_ok = check_files()
    logic_ok = check_logic()
    
    if files_ok and logic_ok:
        print("\n🚀 Preflight PASSED. Environment is stable.")
        run_test_projection()
    else:
        print("\n⚠️ Preflight FAILED. Please address missing components.")