import csv
import os

K_TRACKER_CSV = '/Users/danielreiss/Desktop/Antigravity/MLB/K Prophet/performance_tracker.csv'
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
