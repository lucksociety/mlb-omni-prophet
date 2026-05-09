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

# Update Game Result
update_csv(pred_file, 
           {'Date': '2026-05-04', 'Away_Team': 'MIL', 'Home_Team': 'STL'},
           {'Result_Away_Score': '3', 'Result_Home_Score': '6', 'Result_Winner': 'STL', 'Result_Total': '9'})

# Update Chad Patrick K
update_csv(k_file,
           {'Date': '2026-05-04', 'Name': 'Chad Patrick', 'Matchup': 'MIL@STL'},
           {'Actual': '4', 'Bet': 'Under 3.5', 'Odds': '110', 'Result': 'Loss', 'PNL': '-1.0'})

# Update Kyle Leahy K
update_csv(k_file,
           {'Date': '2026-05-04', 'Name': 'Kyle Leahy', 'Matchup': 'MIL@STL'},
           {'Actual': '5', 'Bet': 'Under 4.5', 'Odds': '-105', 'Result': 'Loss', 'PNL': '-1.0'})
