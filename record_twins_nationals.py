import csv
import json
import os
import glob
from datetime import datetime

BASE_DIR = '/Users/danielreiss/Desktop/Antigravity/MLB'
PREDICTIONS_CSV = os.path.join(BASE_DIR, 'predictions_history.csv')
K_TRACKER_CSV = os.path.join(BASE_DIR, 'K Prophet', 'performance_tracker.csv')
AUDITS_DIR = os.path.join(BASE_DIR, 'audits')

def update_predictions(date, away, home, away_score, home_score):
    rows = []
    updated = False
    with open(PREDICTIONS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['Date'] == date and row['Away_Team'] == away and row['Home_Team'] == home:
                row['Result_Away_Score'] = str(away_score)
                row['Result_Home_Score'] = str(home_score)
                row['Result_Winner'] = away if away_score > home_score else home
                row['Result_Total'] = str(away_score + home_score)
                updated = True
            rows.append(row)
    
    if updated:
        with open(PREDICTIONS_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Updated predictions for {away} @ {home}")
    else:
        print(f"No prediction found for {away} @ {home} on {date}")

def update_k_props(date, matchup, player_ks):
    rows = []
    updated_count = 0
    with open(K_TRACKER_CSV, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['Date'] == date and row['Matchup'] == matchup and row['Name'] in player_ks:
                row['Actual'] = str(player_ks[row['Name']])
                # Note: Skipping PNL calculation for now as it requires bet info, but user didn't provide bets.
                updated_count += 1
            rows.append(row)
            
    if updated_count > 0:
        with open(K_TRACKER_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Updated {updated_count} K-prop entries for {matchup}")
    else:
        print(f"No K-props found for {matchup} on {date}")

def update_audit(date, away, home, away_score, home_score, player_ks):
    pattern = os.path.join(AUDITS_DIR, f"audit_{away}_{home}_{date}*.json")
    files = glob.glob(pattern)
    for filepath in files:
        with open(filepath, 'r') as f:
            audit = json.load(f)
        
        winner = away if away_score > home_score else home
        audit['results'] = {
            'status': 'COMPLETE',
            'away_score': away_score,
            'home_score': home_score,
            'winner': winner,
            'total': away_score + home_score,
            'recorded_at': datetime.now().isoformat(),
        }
        
        # Determine SP K's from player_ks
        # In audit, SPs are identified by away/home
        # This script assumes player_ks contains names.
        # We need to map them to away/home SP.
        away_sp_obj = audit.get('inputs', {}).get('away_sp', {})
        home_sp_obj = audit.get('inputs', {}).get('home_sp', {})
        
        away_sp_name = away_sp_obj.get('name') if isinstance(away_sp_obj, dict) else None
        home_sp_name = home_sp_obj.get('name') if isinstance(home_sp_obj, dict) else None
        
        if away_sp_name in player_ks:
            audit['results']['away_sp_k_actual'] = player_ks[away_sp_name]
        if home_sp_name in player_ks:
            audit['results']['home_sp_k_actual'] = player_ks[home_sp_name]

        # Accuracy
        pred_away = audit.get('outputs', {}).get('score_projection', {}).get('away_mu', 0)
        pred_home = audit.get('outputs', {}).get('score_projection', {}).get('home_mu', 0)
        audit['accuracy'] = {
            'away_error': away_score - pred_away,
            'home_error': home_score - pred_home,
            'total_error': (away_score + home_score) - (pred_away + pred_home),
            'ml_correct': (pred_away > pred_home) == (away_score > home_score),
        }
        
        with open(filepath, 'w') as f:
            json.dump(audit, f, indent=2)
        print(f"Updated audit file: {os.path.basename(filepath)}")

if __name__ == "__main__":
    date = "2026-05-05"
    away = "Twins"
    home = "Nationals"
    away_score = 11
    home_score = 3
    player_ks = {
        "Taj Bradley": 8,
        "Cade Cavalli": 2
    }
    
    update_predictions(date, away, home, away_score, home_score)
    update_k_props(date, "Twins@Nationals", player_ks)
    # Also handle the variant matchup names if any
    update_k_props(date, "WSH@MIN", player_ks) 
    update_audit(date, away, home, away_score, home_score, player_ks)
