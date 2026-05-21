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
from quant_elite_v6_2 import parse_csv, get_bullpen_tiers

sections = parse_csv('/Users/danielreiss/Desktop/Antigravity/MLB/data/MLB Stats')
teams = ['CLE', 'PIT', 'LAA', 'LAD']

print("--- Bullpen Tiers Diagnostic ---")
for team in teams:
    tiers = get_bullpen_tiers(team, "NONE", sections)
    print(f"Team: {team}")
    print(f"  Tier A: {tiers['A']:.2f}")
    print(f"  Tier B: {tiers['B']:.2f}")
    print(f"  Tier C: {tiers['C']:.2f}")