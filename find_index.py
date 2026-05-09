import csv
import os

PREDICTIONS_CSV = '/Users/danielreiss/Desktop/Antigravity/MLB/predictions_history.csv'
date_filter = '2026-05-06'

with open(PREDICTIONS_CSV, 'r') as f:
    reader = csv.DictReader(f)
    pending_count = 0
    for i, row in enumerate(reader):
        if not row.get('Result_Away_Score') and not row.get('Result_Winner'):
            if row.get('Date') == date_filter:
                pending_count += 1
                if row.get('Away_Team') == 'CLE' and row.get('Home_Team') == 'KC':
                    print(f"CLE@KC is pending game #{pending_count}")
                    break
