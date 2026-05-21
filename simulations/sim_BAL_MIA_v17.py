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
from datetime import datetime

from omni_prophet_v16 import OmniProphetV17

def run_bal_mia_sim():
    # Final Lineup Data for BAL @ MIA
    away_lineup = [
        {'Name': 'Gunnar Henderson', 'Hand': 'L', 'K_pct': 30.9, 'O_Swing': 31.7, 'Z_Contact': 84.9, 'wRC_plus': 102},
        {'Name': 'Taylor Ward', 'Hand': 'R', 'K_pct': 16.2, 'O_Swing': 21.2, 'Z_Contact': 89.0, 'wRC_plus': 145},
        {'Name': 'Dylan Beavers', 'Hand': 'L', 'K_pct': 24.2, 'O_Swing': 21.2, 'Z_Contact': 87.7, 'wRC_plus': 84},
        {'Name': 'Pete Alonso', 'Hand': 'R', 'K_pct': 25.6, 'O_Swing': 29.0, 'Z_Contact': 84.6, 'wRC_plus': 109},
        {'Name': 'Samuel Basallo', 'Hand': 'L', 'K_pct': 22.6, 'O_Swing': 39.6, 'Z_Contact': 82.8, 'wRC_plus': 117},
        {'Name': "Tyler O'Neill", 'Hand': 'R', 'K_pct': 28.5, 'O_Swing': 33.0, 'Z_Contact': 79.0, 'wRC_plus': 90},
        {'Name': 'Colton Cowser', 'Hand': 'L', 'K_pct': 29.7, 'O_Swing': 27.7, 'Z_Contact': 75.7, 'wRC_plus': 57},
        {'Name': 'Coby Mayo', 'Hand': 'R', 'K_pct': 29.8, 'O_Swing': 31.3, 'Z_Contact': 83.7, 'wRC_plus': 50},
        {'Name': 'Jeremiah Jackson', 'Hand': 'R', 'K_pct': 22.4, 'O_Swing': 39.0, 'Z_Contact': 76.9, 'wRC_plus': 85}
    ]
    
    home_lineup = [
        {'Name': 'Otto Lopez', 'Hand': 'R', 'K_pct': 8.8, 'O_Swing': 32.4, 'Z_Contact': 91.9, 'wRC_plus': 140},
        {'Name': 'Connor Norby', 'Hand': 'R', 'K_pct': 16.1, 'O_Swing': 29.4, 'Z_Contact': 80.6, 'wRC_plus': 63},
        {'Name': 'Liam Hicks', 'Hand': 'L', 'K_pct': 8.8, 'O_Swing': 21.7, 'Z_Contact': 95.0, 'wRC_plus': 172},
        {'Name': 'Christopher Morel', 'Hand': 'R', 'K_pct': 36.2, 'O_Swing': 28.6, 'Z_Contact': 80.0, 'wRC_plus': 97},
        {'Name': 'Heriberto Hernandez', 'Hand': 'R', 'K_pct': 20.0, 'O_Swing': 23.8, 'Z_Contact': 76.3, 'wRC_plus': 41},
        {'Name': 'Esteury Ruiz', 'Hand': 'R', 'K_pct': 40.0, 'O_Swing': 26.7, 'Z_Contact': 75.0, 'wRC_plus': 88},
        {'Name': 'Jakob Marsee', 'Hand': 'L', 'K_pct': 27.0, 'O_Swing': 24.1, 'Z_Contact': 92.1, 'wRC_plus': 94},
        {'Name': 'Leo Jimenez', 'Hand': 'R', 'K_pct': 25.1, 'O_Swing': 23.0, 'Z_Contact': 98.2, 'wRC_plus': 86},
        {'Name': 'Javier Sanoja', 'Hand': 'R', 'K_pct': 25.8, 'O_Swing': 38.8, 'Z_Contact': 93.2, 'wRC_plus': 109}
    ]

    game_data = {
        'away_team': 'BAL',
        'home_team': 'MIA',
        'away_sp_name': 'Cade Povich',
        'home_sp_name': 'Max Meyer',
        'away_sp_hand': 'L',
        'home_sp_hand': 'R',
        'away_sp_era': 4.41,
        'home_sp_era': 2.68,
        'away_sp_statcast': {
            'Name': 'Cade Povich',
            'Hand': 'L',
            'Stuff': 94,
            'K_pct': 20.0,
            'BB_pct': 8.0,
            'VAA': -4.3,
            'IP': 25,
            'xERA': 4.20
        },
        'home_sp_statcast': {
            'Name': 'Max Meyer',
            'Hand': 'R',
            'Stuff': 107,
            'K_pct': 25.2,
            'BB_pct': 7.5,
            'VAA': -4.5,
            'IP': 30,
            'xERA': 3.96
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'park_factor': 94,
        'is_dome': True,
        'away_drs': 0,
        'home_drs': 0,
        'away_manager_hook': 0,
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 0,
        'away_bp_pitches_d2': 0,
        'home_bp_pitches_d1': 0,
        'home_bp_pitches_d2': 0,
        'away_catcher': 'Samuel Basallo',
        'home_catcher': 'Liam Hicks',
        'game_time': 18.66, # 6:40 PM ET
        'env': {
            'Weather': {
                'temp': 72, 
                'wind_speed': 0, 
                'wind_dir': 0,
                'humidity': 50
            },
            'altitude': 10,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        }
    }

    market_odds = {
        'BAL Moneyline': 108,
        'MIA Moneyline': -126,
        'Total Over 8.5': -110
    }

    omni = OmniProphetV17()
    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_bal_mia_sim()