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

sys.path.append('C:/Users/dreis/OneDrive/Desktop/Antigravity/MLB')
import record_results as rr

# Data
date_str = '2026-05-09'
away_team = 'Houston Astros'
home_team = 'Cincinnati Reds'
away_score = 1
home_score = 3
arrighetti_k = 4
burns_k = 8

# Find rows
pending_games = rr.find_pending_predictions(date_str)
hou_cin_game = None
for p in pending_games:
    if p.get('Away_Team') == away_team and p.get('Home_Team') == home_team:
        hou_cin_game = p
        break

if hou_cin_game:
    print(f"Updating game result for {away_team} @ {home_team}")
    rr.update_predictions_csv(hou_cin_game['row_index'], away_score, home_score)
    rr.update_audit_json(away_team, home_team, date_str, away_score, home_score, away_sp_k=arrighetti_k, home_sp_k=burns_k)
else:
    print("Game prediction not found in history.")

# Update K-props
pending_ks = rr.find_pending_k_props(date_str)
for p in pending_ks:
    name = p.get('Name')
    if name == 'Spencer Arrighetti':
        print(f"Updating K-prop for {name}")
        res, pnl = rr.calc_pnl('Over 5.5', '105', arrighetti_k)
        rr.update_k_tracker(p['row_index'], arrighetti_k, 'Over 5.5', '105', res, pnl)
    elif name == 'Chase Burns':
        print(f"Updating K-prop for {name}")
        res, pnl = rr.calc_pnl('Over 6.5', '-145', burns_k)
        rr.update_k_tracker(p['row_index'], burns_k, 'Over 6.5', '-145', res, pnl)

print("Done.")