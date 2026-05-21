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

K_TRACKER_CSV = '/Users/danielreiss/Desktop/Antigravity/MLB/models/K Prophet/performance_tracker.csv'
date_filter = '2026-05-06'

with open(K_TRACKER_CSV, 'r') as f:
    reader = csv.DictReader(f)
    pending_count = 0
    for i, row in enumerate(reader):
        actual_val = row.get('Actual')
        actual = str(actual_val).strip() if actual_val is not None else ''
        if actual in ('TBD', '', 'None'):
            if row.get('Type') == 'Pitcher Prop' and row.get('Date') == date_filter:
                pending_count += 1
                print(f"Pending K #{pending_count}: {row.get('Name')} ({row.get('Matchup')})")