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

def run_hou_cin_sim():
    # HOU Lineup Data (May 10, 2026) - Confirmed Lineup
    away_lineup = [
        {'Name': 'Jose Altuve', 'Hand': 'R', 'K_pct': 16.0, 'O_Swing': 30.0, 'Z_Contact': 88.0, 'wOBA': 0.324},
        {'Name': 'Yordan Alvarez', 'Hand': 'L', 'K_pct': 20.5, 'O_Swing': 26.0, 'Z_Contact': 85.0, 'wOBA': 0.453},
        {'Name': 'Isaac Paredes', 'Hand': 'R', 'K_pct': 18.0, 'O_Swing': 28.0, 'Z_Contact': 86.0, 'wOBA': 0.339},
        {'Name': 'Christian Walker', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 83.0, 'wOBA': 0.400},
        {'Name': 'Cam Smith', 'Hand': 'R', 'K_pct': 26.9, 'O_Swing': 33.0, 'Z_Contact': 79.0, 'wOBA': 0.294},
        {'Name': 'Brice Matthews', 'Hand': 'R', 'K_pct': 45.0, 'O_Swing': 38.0, 'Z_Contact': 70.0, 'wOBA': 0.317},
        {'Name': 'Zach Cole', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.488},
        {'Name': 'Nick Allen', 'Hand': 'R', 'K_pct': 35.1, 'O_Swing': 34.0, 'Z_Contact': 75.0, 'wOBA': 0.267},
        {'Name': 'Cesar Salazar', 'Hand': 'L', 'K_pct': 28.0, 'O_Swing': 32.0, 'Z_Contact': 78.0, 'wOBA': 0.180},  # Very limited sample, called up May 4
    ]
    
    # CIN Lineup Data (May 10, 2026) - Confirmed Lineup
    home_lineup = [
        {'Name': 'Will Benson', 'Hand': 'L', 'K_pct': 26.0, 'O_Swing': 30.0, 'Z_Contact': 81.0, 'wOBA': 0.330},
        {'Name': 'Spencer Steer', 'Hand': 'R', 'K_pct': 19.0, 'O_Swing': 26.0, 'Z_Contact': 87.0, 'wOBA': 0.343},
        {'Name': 'Elly De La Cruz', 'Hand': 'S', 'K_pct': 28.0, 'O_Swing': 35.0, 'Z_Contact': 76.0, 'wOBA': 0.384},
        {'Name': 'Sal Stewart', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 29.0, 'Z_Contact': 84.0, 'wOBA': 0.357},
        {'Name': 'JJ Bleday', 'Hand': 'L', 'K_pct': 14.9, 'O_Swing': 24.0, 'Z_Contact': 90.0, 'wOBA': 0.407},
        {'Name': 'Tyler Stephenson', 'Hand': 'R', 'K_pct': 28.2, 'O_Swing': 32.0, 'Z_Contact': 80.0, 'wOBA': 0.273},
        {'Name': 'Blake Dunn', 'Hand': 'R', 'K_pct': 31.2, 'O_Swing': 34.0, 'Z_Contact': 77.0, 'wOBA': 0.287},
        {'Name': 'Matt McLain', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.306},
        {'Name': "Ke'Bryan Hayes", 'Hand': 'R', 'K_pct': 20.0, 'O_Swing': 27.0, 'Z_Contact': 86.0, 'wOBA': 0.193},
    ]

    game_data = {
        'away_team': 'HOU',
        'home_team': 'CIN',
        'away_sp_name': 'Cody Bolton',
        'home_sp_name': 'Andrew Abbott',
        'away_sp_hand': 'R',
        'home_sp_hand': 'L',
        'away_sp_era': 4.63,
        'home_sp_era': 5.13,
        'away_sp_statcast': {
            'Name': 'Cody Bolton',
            'Hand': 'R',
            'Stuff': 98,        # No Stuff+ data available, using league-avg estimate
            'K_pct': 25.0,      # 2026: 25.0% K rate
            'BB_pct': 16.1,     # 2026: 16.1% BB rate — extremely high
            'VAA': -4.4,
            'IP': 11.2,         # ROOKIE: < 30 IP → SMF regression triggered
            'Starts': 3,        # ROOKIE: < 5 starts → SMF regression triggered
            'ERA': 4.63,
            'xERA': 4.42,       # Based on FIP of 4.42
            'HR/FB%': 12.5,
            'LastPitchCount': 75  # Limited pitch count expected for opener/primary
        },
        'home_sp_statcast': {
            'Name': 'Andrew Abbott',
            'Hand': 'L',
            'Stuff': 102,       # Estimated — elite stuff in 2025 (All-Star), slight regression 2026
            'K_pct': 15.4,      # 2026: 15.4% — MASSIVE drop from 18.7% in 2025 (2025 anchor: ~17.5% blended)
            'BB_pct': 10.4,     # 2026: 10.4% — up from 5.4% in 2025
            'VAA': -4.6,
            'IP': 40.1,         # 8 starts, 40.1 IP — established
            'Starts': 8,
            'ERA': 5.13,
            'xERA': 4.77,       # xFIP 4.77
            'HR/FB%': 11.1,
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
        'park_factor': 112,     # Great American Ball Park — one of the most HR-friendly parks in MLB (123 HR factor)
        'is_dome': False,
        'away_drs': -3,         # HOU defense in transition with youth
        'home_drs': 1,          # CIN avg defense, De La Cruz SS range
        'away_manager_hook': 0.2,  # Bolton likely on short leash as "PRIM"
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 20,
        'away_bp_pitches_d2': 10,
        'home_bp_pitches_d1': 15,
        'home_bp_pitches_d2': 10,
        'away_catcher': 'Cesar Salazar',
        'home_catcher': 'Tyler Stephenson',
        'game_time_decimal': 13.67,  # 1:40 PM ET
        'game_time': '13:40',
        'location': 'CIN',
        'away_bp_avg_era': 4.30,  # HOU bullpen — league avg
        'home_bp_avg_era': 3.90,  # CIN bullpen — slightly better
        'env': {
            'Weather': {
                'temp': 66,           # 66°F — neutral
                'wind_speed': 3,      # 3 mph wind blowing OUT — slight fly-ball boost
                'wind_dir': 0,        # Blowing OUT
                'humidity': 50
            },
            'altitude': 482,          # Cincinnati elevation
            'rain_intensity': 0.0,    # 3% precip chance = negligible
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}  # Umpire not announced
        }
    }

    market_odds = {
        'CIN Moneyline': -121,
        'HOU Moneyline': 103,
        'Total Over 9.5': -110,
        'Total Under 9.5': -110,
        'Andrew Abbott Over 4.5 K': -115,
        'Andrew Abbott Under 4.5 K': -105,
        'Cody Bolton Over 3.5 K': -120,
        'Cody Bolton Under 3.5 K': -100
    }

    omni = OmniProphetV18()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_hou_cin_sim()