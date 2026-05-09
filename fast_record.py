import csv
import json
import os
from datetime import datetime

BASE_DIR = '/Users/danielreiss/Desktop/Antigravity/MLB'
TRACKER_CSV = os.path.join(BASE_DIR, 'K Prophet/performance_tracker.csv')
AUDIT_FILE = os.path.join(BASE_DIR, 'audits/audit_TOR_TB_2026-05-04.json')

# 1. Update Tracker CSV
rows = []
with open(TRACKER_CSV, 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

for i, row in enumerate(rows):
    if len(row) > 3 and row[0] == '2026-05-04' and row[3] == 'Eric Lauer' and 'TOR@TB' in row[2]:
        # Date,Type,Matchup,Name,Projection,KP_Median,KP_Mean,QE_Median,QE_Mean,Reconciliation,Confidence,Actual,Bet,Odds,Result,PNL
        row[11] = '2'
        row[14] = 'Win'
        row[15] = '0.91' # Assumed -110 for a winner
    if len(row) > 3 and row[0] == '2026-05-04' and row[3] == 'Nick Martinez' and 'TOR@TB' in row[2]:
        row[11] = '4'
        row[12] = 'Under 4.5'
        row[13] = '-135'
        row[14] = 'Win'
        row[15] = '0.74'

with open(TRACKER_CSV, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# 2. Update Audit JSON
if os.path.exists(AUDIT_FILE):
    with open(AUDIT_FILE, 'r') as f:
        audit = json.load(f)
    
    audit['results'] = {
        'status': 'COMPLETE',
        'away_score': 1,
        'home_score': 5,
        'winner': 'TB',
        'total': 6,
        'away_sp_k_actual': 2,
        'home_sp_k_actual': 4,
        'recorded_at': datetime.now().isoformat()
    }
    
    pred_away = audit['outputs']['score_projection']['away_mu']
    pred_home = audit['outputs']['score_projection']['home_mu']
    
    audit['accuracy'] = {
        'away_error': 1 - pred_away,
        'home_error': 5 - pred_home,
        'total_error': 6 - (pred_away + pred_home),
        'ml_correct': False,
        'away_k_error': 2 - audit['outputs']['k_projections']['away']['final_k'],
        'home_k_error': 4 - audit['outputs']['k_projections']['home']['final_k']
    }
    
    with open(AUDIT_FILE, 'w') as f:
        json.dump(audit, f, indent=2)

print("Results recorded successfully.")
