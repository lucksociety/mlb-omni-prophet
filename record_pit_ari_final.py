
import sys
import os

# Add the directory to path
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

import record_results as rr

def record():
    date_str = '2026-05-06'
    away_t = 'PIT'
    home_t = 'ARI'
    away_score = 1
    home_score = 0
    skenes_k = 7
    soroka_k = 6
    
    # 1. Find and update predictions_history.csv
    pending_games = rr.find_pending_predictions(date_str)
    for p in pending_games:
        if p.get('Away_Team') == away_t and p.get('Home_Team') == home_t:
            print(f"Updating game record for {away_t}@{home_t} on {date_str}...")
            rr.update_predictions_csv(p['row_index'], away_score, home_score)
            rr.update_audit_json(away_t, home_t, date_str, away_score, home_score,
                                 away_sp_k=skenes_k, home_sp_k=soroka_k)

    # 2. Find and update K Prophet/performance_tracker.csv
    pending_ks = rr.find_pending_k_props(date_str)
    for p in pending_ks:
        if p.get('Matchup') == f"{away_t}@{home_t}":
            name = p.get('Name')
            if 'Skenes' in name:
                actual = skenes_k
                bet = 'Under 5.5'
                odds = 120
            elif 'Soroka' in name:
                actual = soroka_k
                bet = 'Under 5.5'
                odds = -135
            else:
                continue
                
            print(f"Updating K record for {name}...")
            res, pnl = rr.calc_pnl(bet, odds, actual)
            rr.update_k_tracker(p['row_index'], actual, bet, odds, res, pnl)

if __name__ == '__main__':
    record()
