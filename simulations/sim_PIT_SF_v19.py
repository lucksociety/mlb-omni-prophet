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

from omni_prophet_v16 import OmniProphetV18

def run_pit_sf_sim():
    # PIT Lineup Data (May 10, 2026) - Confirmed Lineup
    # Stats from ingest_user_batting_v2.py
    away_lineup = [
        {'Name': 'Oneil Cruz', 'Hand': 'L', 'K_pct': 34.9, 'O_Swing': 35.0, 'Z_Contact': 78.0, 'wOBA': 0.355},
        {'Name': 'Brandon Lowe', 'Hand': 'L', 'K_pct': 22.2, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.384},
        {'Name': 'Nick Gonzales', 'Hand': 'R', 'K_pct': 18.3, 'O_Swing': 28.0, 'Z_Contact': 86.0, 'wOBA': 0.344},
        {'Name': 'Ryan O\'Hearn', 'Hand': 'L', 'K_pct': 19.3, 'O_Swing': 32.0, 'Z_Contact': 84.0, 'wOBA': 0.383},
        {'Name': 'Marcell Ozuna', 'Hand': 'R', 'K_pct': 26.4, 'O_Swing': 34.0, 'Z_Contact': 78.0, 'wOBA': 0.257},
        {'Name': 'Spencer Horwitz', 'Hand': 'L', 'K_pct': 12.9, 'O_Swing': 24.0, 'Z_Contact': 90.0, 'wOBA': 0.335},
        {'Name': 'Konnor Griffin', 'Hand': 'R', 'K_pct': 27.2, 'O_Swing': 33.0, 'Z_Contact': 79.0, 'wOBA': 0.323},
        {'Name': 'Nick Yorke', 'Hand': 'R', 'K_pct': 19.2, 'O_Swing': 30.0, 'Z_Contact': 83.0, 'wOBA': 0.285},
        {'Name': 'Henry Davis', 'Hand': 'R', 'K_pct': 19.0, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.250},
    ]
    
    # SF Lineup Data (May 10, 2026) - Confirmed Lineup
    home_lineup = [
        {'Name': 'Jung Hoo Lee', 'Hand': 'L', 'K_pct': 13.1, 'O_Swing': 22.0, 'Z_Contact': 91.0, 'wOBA': 0.320},
        {'Name': 'Luis Arraez', 'Hand': 'L', 'K_pct': 4.2, 'O_Swing': 20.0, 'Z_Contact': 94.0, 'wOBA': 0.328},
        {'Name': 'Casey Schmitt', 'Hand': 'R', 'K_pct': 19.7, 'O_Swing': 32.0, 'Z_Contact': 82.0, 'wOBA': 0.392},
        {'Name': 'Rafael Devers', 'Hand': 'L', 'K_pct': 29.9, 'O_Swing': 35.0, 'Z_Contact': 76.0, 'wOBA': 0.255},
        {'Name': 'Heliot Ramos', 'Hand': 'R', 'K_pct': 28.4, 'O_Swing': 34.0, 'Z_Contact': 77.0, 'wOBA': 0.317},
        {'Name': 'Willy Adames', 'Hand': 'R', 'K_pct': 31.3, 'O_Swing': 35.0, 'Z_Contact': 75.0, 'wOBA': 0.257},
        {'Name': 'Matt Chapman', 'Hand': 'R', 'K_pct': 23.4, 'O_Swing': 30.0, 'Z_Contact': 80.0, 'wOBA': 0.301},
        {'Name': 'Drew Gilbert', 'Hand': 'L', 'K_pct': 18.2, 'O_Swing': 26.0, 'Z_Contact': 87.0, 'wOBA': 0.307},
        {'Name': 'Jesus Rodriguez', 'Hand': 'R', 'K_pct': 22.7, 'O_Swing': 30.0, 'Z_Contact': 83.0, 'wOBA': 0.320}, # Regressed
    ]

    game_data = {
        'away_team': 'PIT',
        'home_team': 'SF',
        'away_sp_name': 'Bubba Chandler',
        'home_sp_name': 'Tyler Mahle',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': 4.76,
        'home_sp_era': 5.00,
        'away_sp_statcast': {
            'Name': 'Bubba Chandler',
            'Hand': 'R',
            'Stuff': 98.8,
            'K_pct': 22.0,      # Based on 8.38 K/9
            'BB_pct': 16.0,     # Based on 6.21 BB/9
            'VAA': -4.5,
            'IP': 29.0,         # ROOKIE Regression Triggered (< 30 IP)
            'Starts': 6,
            'ERA': 4.76,
            'xERA': 5.69,       # xFIP
            'HR/FB%': 13.5,
            'LastPitchCount': 85
        },
        'home_sp_statcast': {
            'Name': 'Tyler Mahle',
            'Hand': 'R',
            'Stuff': 92.5,
            'K_pct': 22.0,      # Based on 8.50 K/9
            'BB_pct': 12.0,     # Based on 4.50 BB/9
            'VAA': -4.4,
            'IP': 36.0,
            'Starts': 7,
            'ERA': 5.00,
            'xERA': 4.92,       # xFIP
            'HR/FB%': 17.6,
            'LastPitchCount': 90
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'away_lineup_k_pct': statistics.mean([b['K_pct'] for b in away_lineup]),
        'home_lineup_k_pct': statistics.mean([b['K_pct'] for b in home_lineup]),
        'park_factor': 97,      # Oracle Park
        'is_dome': False,
        'away_drs': 2,
        'home_drs': 5,          # SF defensive backbone mentioned
        'away_manager_hook': 0.1,
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 25,
        'away_bp_pitches_d2': 10,
        'home_bp_pitches_d1': 15,
        'home_bp_pitches_d2': 20,
        'away_catcher': 'Henry Davis',
        'home_catcher': 'Jesus Rodriguez',
        'game_time_decimal': 16.08,  # 4:05 PM ET
        'game_time': '16:05',
        'location': 'SF',
        'away_bp_avg_era': 4.20,
        'home_bp_avg_era': 4.10,
        'env': {
            'Weather': {
                'temp': 60,
                'wind_speed': 9,
                'wind_dir': 0,        # Blowing OUT (rare for Oracle)
                'humidity': 55
            },
            'altitude': 10,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        }
    }

    market_odds = {
        'SF Moneyline': -126,
        'PIT Moneyline': 112,
        'Total Over 8.0': -110,
        'Total Under 8.0': -110,
        'Bubba Chandler Over 4.5 K': -115,
        'Bubba Chandler Under 4.5 K': -105,
        'Tyler Mahle Over 4.5 K': -120,
        'Tyler Mahle Under 4.5 K': -100
    }

    omni = OmniProphetV18()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_pit_sf_sim()