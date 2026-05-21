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

def run_col_phi_sim():
    # Final Lineup Data for COL @ PHI (May 10, 2026)
    # Estimates based on prompt and MLB Stats forensic data
    away_lineup = [
        {'Name': 'Jordan Beck', 'Hand': 'R', 'K_pct': 29.4, 'O_Swing': 32.5, 'Z_Contact': 80.0, 'wOBA': 0.295},
        {'Name': 'Tyler Freeman', 'Hand': 'R', 'K_pct': 13.9, 'O_Swing': 25.0, 'Z_Contact': 88.0, 'wOBA': 0.300},
        {'Name': 'Hunter Goodman', 'Hand': 'R', 'K_pct': 29.1, 'O_Swing': 34.0, 'Z_Contact': 78.0, 'wOBA': 0.345},
        {'Name': 'Willi Castro', 'Hand': 'S', 'K_pct': 24.0, 'O_Swing': 30.0, 'Z_Contact': 84.0, 'wOBA': 0.315},
        {'Name': 'Brenton Doyle', 'Hand': 'R', 'K_pct': 27.8, 'O_Swing': 33.0, 'Z_Contact': 81.0, 'wOBA': 0.310},
        {'Name': 'Mickey Moniak', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 35.0, 'Z_Contact': 79.0, 'wOBA': 0.425},
        {'Name': 'Kyle Karros', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.310},
        {'Name': 'Ezequiel Tovar', 'Hand': 'R', 'K_pct': 27.6, 'O_Swing': 31.0, 'Z_Contact': 82.0, 'wOBA': 0.290},
        {'Name': 'Jake McCarthy', 'Hand': 'L', 'K_pct': 18.0, 'O_Swing': 26.0, 'Z_Contact': 89.0, 'wOBA': 0.340}
    ]
    
    home_lineup = [
        {'Name': 'Trea Turner', 'Hand': 'R', 'K_pct': 17.6, 'O_Swing': 31.0, 'Z_Contact': 86.0, 'wOBA': 0.345},
        {'Name': 'Kyle Schwarber', 'Hand': 'L', 'K_pct': 29.8, 'O_Swing': 22.0, 'Z_Contact': 82.0, 'wOBA': 0.385},
        {'Name': 'Bryce Harper', 'Hand': 'L', 'K_pct': 21.2, 'O_Swing': 28.0, 'Z_Contact': 84.0, 'wOBA': 0.395},
        {'Name': 'Adolis Garcia', 'Hand': 'R', 'K_pct': 25.0, 'O_Swing': 33.0, 'Z_Contact': 80.0, 'wOBA': 0.300},
        {'Name': 'Brandon Marsh', 'Hand': 'L', 'K_pct': 25.6, 'O_Swing': 30.0, 'Z_Contact': 83.0, 'wOBA': 0.355},
        {'Name': 'J.T. Realmuto', 'Hand': 'R', 'K_pct': 22.8, 'O_Swing': 32.0, 'Z_Contact': 84.0, 'wOBA': 0.325},
        {'Name': 'Bryson Stott', 'Hand': 'L', 'K_pct': 14.3, 'O_Swing': 24.0, 'Z_Contact': 91.0, 'wOBA': 0.325},
        {'Name': 'Alec Bohm', 'Hand': 'R', 'K_pct': 18.0, 'O_Swing': 27.0, 'Z_Contact': 87.0, 'wOBA': 0.340},
        {'Name': 'Justin Crawford', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'wOBA': 0.310}
    ]

    game_data = {
        'away_team': 'COL',
        'home_team': 'PHI',
        'away_sp_name': 'Tomoyuki Sugano',
        'home_sp_name': 'Cristopher Sanchez',
        'away_sp_hand': 'R',
        'home_sp_hand': 'L',
        'away_sp_era': 3.41,
        'home_sp_era': 2.42,
        'away_sp_statcast': {
            'Name': 'Tomoyuki Sugano',
            'Hand': 'R',
            'Stuff': 92,
            'K_pct': 15.6,
            'BB_pct': 5.0,
            'VAA': -4.3,
            'IP': 37.0,
            'Starts': 5,
            'ERA': 3.41,
            'xERA': 3.60,
            'LastPitchCount': 90
        },
        'home_sp_statcast': {
            'Name': 'Cristopher Sanchez',
            'Hand': 'L',
            'Stuff': 105,
            'K_pct': 32.7, # 60 K in 48.1 IP
            'BB_pct': 6.5,
            'VAA': -4.6,
            'IP': 48.1,
            'Starts': 6,
            'ERA': 2.42,
            'xERA': 3.10,
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
        'park_factor': 112, # Citizens Bank Park is HR friendly
        'is_dome': False,
        'away_drs': -2,
        'home_drs': 2,
        'away_manager_hook': 0,
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 20,
        'away_bp_pitches_d2': 10,
        'home_bp_pitches_d1': 15,
        'home_bp_pitches_d2': 5,
        'away_catcher': 'Hunter Goodman',
        'home_catcher': 'J.T. Realmuto',
        'game_time_decimal': 13.5, # 1:35 PM ET
        'game_time': '13:35',
        'env': {
            'Weather': {
                'temp': 79, 
                'wind_speed': 8, 
                'wind_dir': 0, # Blowing OUT
                'humidity': 45
            },
            'altitude': 40,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        }
    }

    market_odds = {
        'PHI Moneyline': -308,
        'COL Moneyline': 250,
        'Total Over 8.5': -110,
        'Total Under 8.5': -110,
        'Cristopher Sanchez Over 6.5 K': -120,
        'Tomoyuki Sugano Under 4.5 K': -115
    }

    omni = OmniProphetV18()
    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_col_phi_sim()