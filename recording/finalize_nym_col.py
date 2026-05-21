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

sys.path.append("/Users/danielreiss/Desktop/Antigravity/MLB")
from record_results import update_predictions_csv, update_k_tracker, update_audit_json, find_pending_predictions, find_pending_k_props

DATE = "2026-05-06"
AWAY = "NYM"
HOME = "COL"
AWAY_SCORE = 10
HOME_SCORE = 5
PERALTA_K = 1
LORENZEN_K = 2

# 1. Update Game Score
pending_games = find_pending_predictions(DATE)
for p in pending_games:
    if p.get('Away_Team') == AWAY and p.get('Home_Team') == HOME:
        update_predictions_csv(p['row_index'], AWAY_SCORE, HOME_SCORE)
        update_audit_json(AWAY, HOME, DATE, AWAY_SCORE, HOME_SCORE, away_sp_k=PERALTA_K, home_sp_k=LORENZEN_K)
        print(f"✅ Recorded Game Result: {AWAY} {AWAY_SCORE} - {HOME} {HOME_SCORE}")

# 2. Update K Props
pending_ks = find_pending_k_props(DATE)
for p in pending_ks:
    if p.get('Name') == 'Freddy Peralta':
        update_k_tracker(p['row_index'], PERALTA_K, bet='Under 6.5', odds='-170', result='Win', pnl='0.59')
        print(f"✅ Recorded Peralta K: {PERALTA_K}")
    elif p.get('Name') == 'Michael Lorenzen':
        update_k_tracker(p['row_index'], LORENZEN_K, bet='Under 3.5', odds='-110', result='Win', pnl='0.91')
        print(f"✅ Recorded Lorenzen K: {LORENZEN_K}")

print("\nDone. All results finalized and persisted.")