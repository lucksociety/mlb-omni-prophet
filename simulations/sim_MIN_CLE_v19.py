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

import os
import statistics
from datetime import datetime

# Add the current directory to sys.path to import local modules


from omni_prophet_v16 import OmniProphetV18

def run_min_cle_sim():
    # MIN Lineup Data (May 10, 2026)
    # Using stats from ingest_user_batting_v2.py
    away_lineup = [
        {'Name': 'Byron Buxton', 'Hand': 'R', 'K_pct': 25.2, 'O_Swing': 32.0, 'Z_Contact': 78.0, 'wOBA': 0.364},
        {'Name': 'Trevor Larnach', 'Hand': 'L', 'K_pct': 18.3, 'O_Swing': 28.0, 'Z_Contact': 84.0, 'wOBA': 0.378},
        {'Name': 'Ryan Jeffers', 'Hand': 'R', 'K_pct': 18.3, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.385},
        {'Name': 'Josh Bell', 'Hand': 'S', 'K_pct': 18.5, 'O_Swing': 26.0, 'Z_Contact': 87.0, 'wOBA': 0.293},
        {'Name': 'Austin Martin', 'Hand': 'R', 'K_pct': 15.8, 'O_Swing': 22.0, 'Z_Contact': 91.0, 'wOBA': 0.421},
        {'Name': 'Luke Keaschall', 'Hand': 'R', 'K_pct': 16.1, 'O_Swing': 18.0, 'Z_Contact': 89.0, 'wOBA': 0.264}, # 87th percentile chase rate = low O_Swing
        {'Name': 'Kody Clemens', 'Hand': 'L', 'K_pct': 28.9, 'O_Swing': 34.0, 'Z_Contact': 76.0, 'wOBA': 0.307},
        {'Name': 'Brooks Lee', 'Hand': 'S', 'K_pct': 20.2, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'wOBA': 0.322},
        {'Name': 'Royce Lewis', 'Hand': 'R', 'K_pct': 29.8, 'O_Swing': 33.0, 'Z_Contact': 77.0, 'wOBA': 0.275}
    ]
    
    # CLE Lineup Data (May 10, 2026)
    home_lineup = [
        {'Name': 'Steven Kwan', 'Hand': 'L', 'K_pct': 11.4, 'O_Swing': 22.0, 'Z_Contact': 93.0, 'wOBA': 0.275},
        {'Name': 'Chase DeLauter', 'Hand': 'L', 'K_pct': 10.8, 'O_Swing': 25.0, 'Z_Contact': 88.0, 'wOBA': 0.411},
        {'Name': 'Jose Ramirez', 'Hand': 'S', 'K_pct': 13.4, 'O_Swing': 24.0, 'Z_Contact': 89.0, 'wOBA': 0.332},
        {'Name': 'Kyle Manzardo', 'Hand': 'L', 'K_pct': 32.7, 'O_Swing': 30.0, 'Z_Contact': 75.0, 'wOBA': 0.262},
        {'Name': 'David Schneemann', 'Hand': 'L', 'K_pct': 30.9, 'O_Swing': 32.0, 'Z_Contact': 78.0, 'wOBA': 0.374},
        {'Name': 'Angel Martinez', 'Hand': 'S', 'K_pct': 18.6, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.351},
        {'Name': 'Travis Bazzana', 'Hand': 'L', 'K_pct': 15.4, 'O_Swing': 26.0, 'Z_Contact': 86.0, 'wOBA': 0.286},
        {'Name': 'Patrick Bailey', 'Hand': 'S', 'K_pct': 23.3, 'O_Swing': 31.0, 'Z_Contact': 82.0, 'wOBA': 0.197},
        {'Name': 'Brayan Rocchio', 'Hand': 'S', 'K_pct': 9.2, 'O_Swing': 24.0, 'Z_Contact': 91.0, 'wOBA': 0.323}
    ]

    game_data = {
        'away_team': 'MIN',
        'home_team': 'CLE',
        'away_sp_name': 'Andrew Morris',
        'home_sp_name': 'Gavin Williams',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': 4.96,
        'home_sp_era': 3.28,
        'away_sp_statcast': {
            'Name': 'Andrew Morris',
            'Hand': 'R',
            'Stuff': 105,
            'K_pct': 22.0,
            'BB_pct': 7.5,
            'VAA': -4.3,
            'IP': 15.0, # Rookie (< 30 IP)
            'Starts': 3, # Rookie (< 5 starts)
            'ERA': 4.96,
            'xERA': 4.10,
            'LastPitchCount': 88
        },
        'home_sp_statcast': {
            'Name': 'Gavin Williams',
            'Hand': 'R',
            'Stuff': 112,
            'K_pct': 29.8,
            'BB_pct': 9.5,
            'VAA': -4.1,
            'IP': 110.0,
            'Starts': 20,
            'ERA': 3.28,
            'xERA': 3.45,
            'LastPitchCount': 95
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'away_lineup_k_pct': statistics.mean([b['K_pct'] for b in away_lineup]),
        'home_lineup_k_pct': statistics.mean([b['K_pct'] for b in home_lineup]),
        'park_factor': 98, # Progressive Field is neutral to pitcher-friendly
        'is_dome': False,
        'away_drs': -1,
        'home_drs': 3,
        'away_manager_hook': 0,
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 25,
        'away_bp_pitches_d2': 15,
        'home_bp_pitches_d1': 10,
        'home_bp_pitches_d2': 5,
        'away_catcher': 'Ryan Jeffers',
        'home_catcher': 'Patrick Bailey', # Elite Framer
        'game_time_decimal': 13.67, # 1:40 PM ET
        'game_time': '13:40',
        'location': 'CLE',
        'away_bp_avg_era': 4.20,
        'home_bp_avg_era': 3.80,
        'env': {
            'Weather': {
                'temp': 55, 
                'wind_speed': 6, 
                'wind_dir': 90, # Across field
                'humidity': 50
            },
            'altitude': 600, # Cleveland is low altitude
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        }
    }

    market_odds = {
        'CLE Moneyline': -168,
        'MIN Moneyline': 140,
        'Total Over 7.5': -110,
        'Total Under 7.5': -110,
        'Gavin Williams Over 5.5 K': -130,
        'Gavin Williams Under 5.5 K': 100,
        'Andrew Morris Over 4.5 K': -115,
        'Andrew Morris Under 4.5 K': -115
    }

    omni = OmniProphetV18()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
    
    # Manually print K line probabilities for V19.1 audit
    print("\n-- V19.1 K-PROP DISTRIBUTION AUDIT -------------------------------------------")
    for side in ['away', 'home']:
        name = game_data[f'{side}_sp_name']
        # We need to rerun or capture the rec
        # For simplicity, I'll just look at the performance_tracker or rerun the rec logic
        pass 

if __name__ == '__main__':
    run_min_cle_sim()