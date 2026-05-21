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
from quant_elite_v6_5 import parse_csv, get_pitcher_stats, ARCHETYPES

sections = parse_csv('MLB Stats')
burke = get_pitcher_stats('Sean Burke', 'CHW', sections)
king = get_pitcher_stats('Michael King', 'SDP', sections)

print("Sean Burke Stats:", burke)
print("Michael King Stats:", king)
print("Sean Burke Archetype:", ARCHETYPES.get('Sean Burke', 'Not Found'))
print("Michael King Archetype:", ARCHETYPES.get('Michael King', 'Not Found'))