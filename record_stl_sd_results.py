import csv
import os

base_dir = '/Users/danielreiss/Desktop/Antigravity/MLB'
pred_file = os.path.join(base_dir, 'predictions_history.csv')
k_file = os.path.join(base_dir, 'K Prophet/performance_tracker.csv')

def update_csv(file_path, match_dict, update_dict):
    rows = []
    updated = False
    with open(file_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            match = True
            for k, v in match_dict.items():
                if row.get(k) != v:
                    match = False
                    break
            if match:
                row.update(update_dict)
                updated = True
            rows.append(row)
    
    if updated:
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Updated {file_path}")
    else:
        print(f"No match found in {file_path}")

# 1. Update Game Result (STL @ SD)
# Since there are multiple entries for this game in history (duplicates from re-runs), 
# I will update all of them for consistency.
update_csv(pred_file, 
           {'Date': '2026-05-07', 'Away_Team': 'STL', 'Home_Team': 'SD'},
           {'Result_Away_Score': '2', 'Result_Home_Score': '1', 'Result_Winner': 'STL', 'Result_Total': '3'})

# 2. Update Michael King K
update_csv(k_file,
           {'Date': '2026-05-07', 'Name': 'Michael King', 'Matchup': 'STL@SD'},
           {'Actual': '6', 'Bet': 'Under 4.5', 'Odds': '-105', 'Result': 'Loss', 'PNL': '-1.0'})

# 3. Update Matthew Liberatore K
update_csv(k_file,
           {'Date': '2026-05-07', 'Name': 'Matthew Liberatore', 'Matchup': 'STL@SD'},
           {'Actual': '6', 'Bet': 'Under 3.5', 'Odds': '100', 'Result': 'Loss', 'PNL': '-1.0'})

print("Forensic Audit Complete. Ready for Calibration Check.")
