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

base_dir = '/Users/danielreiss/Desktop/Antigravity/MLB'
predictions_csv = os.path.join(base_dir, 'predictions_history.csv')
k_tracker_csv = os.path.join(base_dir, 'K Prophet/performance_tracker.csv')

# Fix predictions_history.csv
rows = []
with open(predictions_csv, 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Row 42 is index 41. Verify it's the right one.
if len(rows) > 41 and rows[41][1] == 'ATL' and rows[41][2] == 'SEA':
    # Date,Away_Team,Home_Team,Pred_Away_Score,Pred_Home_Score,Pred_Total,Calibrated_Total,Cal_Modifier,Away_Win_Pct,Home_Win_Pct,ML_Edge,Away_CI_Low,Away_CI_High,Home_CI_Low,Home_CI_High,Total_CI_Low,Total_CI_High,Blowout_Pct,Away_SP,Home_SP,Away_K_Pred,Home_K_Pred,Away_K_Status,Home_K_Status,Ace_Traps,Park_Factor,Umpire,Umpire_Zone,Temp,Wind_Speed,Wind_Dir,Humidity,Engine_Version,Result_Away_Score,Result_Home_Score,Result_Winner,Result_Total
    rows[41][33] = '4' # Result_Away_Score
    rows[41][34] = '5' # Result_Home_Score
    rows[41][35] = 'SEA' # Result_Winner
    rows[41][36] = '9' # Result_Total
    print("Updated predictions_history.csv row 42")
else:
    print(f"Error: Row 42 is not ATL@SEA. It is {rows[41] if len(rows)>41 else 'missing'}")

with open(predictions_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# Fix performance_tracker.csv
rows_k = []
with open(k_tracker_csv, 'r') as f:
    reader = csv.reader(f)
    rows_k = list(reader)

# JR Ritchie at index 134 (line 135)
if len(rows_k) > 134 and rows_k[134][3] == 'JR Ritchie':
    rows_k[134][11] = '2' # Actual
    rows_k[134][12] = 'None' # Bet
    rows_k[134][14] = 'N/A' # Result
    rows_k[134][15] = '0.0' # PNL
    print("Updated JR Ritchie K's")

# Logan Gilbert at index 135 (line 136)
if len(rows_k) > 135 and rows_k[135][3] == 'Logan Gilbert':
    rows_k[135][11] = '4' # Actual
    rows_k[135][12] = 'Under 5.5' # Bet
    rows_k[135][13] = '-130' # Odds
    rows_k[135][14] = 'Win' # Result
    rows_k[135][15] = '0.77' # PNL
    print("Updated Logan Gilbert K's")

# Also add the ML bet for ATL if not there? 
# performance_tracker.csv usually tracks Props. Game Total/ML might be in a different file or just in predictions_history.
# I'll just update these.

with open(k_tracker_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows_k)