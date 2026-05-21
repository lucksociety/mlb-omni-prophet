
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

# Add the directory to path so we can import OmniProphet
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV17

def run_simulation():
    omni = OmniProphetV17()
    
    # Odds from user report: ARI -118, PIT +100
    # Odds from user images
    market_odds = {
        'PIT ML': -105,
        'ARI ML': -115,
        'Total Over 8.5': -120,
        'Total Under 8.5': 100,
        'YRFI': -115,
        'NRFI': -115,
        'Mitch Keller Over 4.5 K': 120,
        'Mitch Keller Under 4.5 K': -160,
        'Zac Gallen Over 4.5 K': -125,
        'Zac Gallen Under 4.5 K': -105,
        'PIT F5 ML': -110,
        'ARI F5 ML': -120,
        'Total Over 5.0 F5': -105,
        'Total Under 5.0 F5': -125
    }

    game_data = {
        'away_team': 'PIT',
        'home_team': 'ARI',
        'game_time': '15:40', # 3:40 PM ET
        'is_dome': True,
        'park_factor': 102,
        'env': {
            'Weather': {
                'temp': 75,
                'wind_speed': 0,
                'wind_dir': 0,
                'humidity': 40
            },
            'altitude': 1082,
            'rain_intensity': 0.0,
            'Umpire': {
                'name': 'Neutral',
                'CS_pct': 17.5,
                'zone_type': 'neutral'
            }
        },
        'away_sp_name': 'Mitch Keller',
        'away_sp_hand': 'R',
        'away_sp_era': 2.85,
        'away_sp_statcast': {
            'Name': 'Mitch Keller',
            'Hand': 'R',
            'Stuff': 94,
            'K_pct': 21.5,
            'BB_pct': 7.2,
            'VAA': -4.2,
            'IP': 45.0,
            'xERA': 3.48,
            'L3_CSW': 28.5,
            'L3_SwStr': 11.2,
            'LastPitchCount': 95
        },
        'home_sp_name': 'Zac Gallen',
        'home_sp_hand': 'R',
        'home_sp_era': 4.45,
        'home_sp_statcast': {
            'Name': 'Zac Gallen',
            'Hand': 'R',
            'Stuff': 89,
            'K_pct': 17.8,
            'BB_pct': 9.1,
            'VAA': -4.0,
            'IP': 38.0,
            'xERA': 5.28,
            'L3_CSW': 24.5,
            'L3_SwStr': 9.2,
            'LastPitchCount': 80
        },
        'away_lineup_names': ['Oneil Cruz', 'Brandon Lowe', 'Bryan Reynolds', 'Ryan O\'Hearn', 'Spencer Horwitz', 'Konnor Griffin', 'Jared Triolo', 'Jake Mangum', 'Joey Bart'],
        'away_lineup_hands': ['L', 'L', 'S', 'L', 'L', 'R', 'R', 'S', 'R'],
        'away_lineup_statcast': [
            {'Name': 'Oneil Cruz', 'Hand': 'L', 'K_pct': 30.8, 'O_Swing': 35, 'Z_Contact': 78},
            {'Name': 'Brandon Lowe', 'Hand': 'L', 'K_pct': 28.1, 'O_Swing': 28, 'Z_Contact': 88},
            {'Name': 'Bryan Reynolds', 'Hand': 'S', 'K_pct': 27.3, 'O_Swing': 27, 'Z_Contact': 86},
            {'Name': 'Ryan O\'Hearn', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 30, 'Z_Contact': 88},
            {'Name': 'Spencer Horwitz', 'Hand': 'L', 'K_pct': 15.4, 'O_Swing': 25, 'Z_Contact': 92},
            {'Name': 'Konnor Griffin', 'Hand': 'R', 'K_pct': 25.8, 'O_Swing': 34, 'Z_Contact': 82},
            {'Name': 'Jared Triolo', 'Hand': 'R', 'K_pct': 25.0, 'O_Swing': 28, 'Z_Contact': 85},
            {'Name': 'Jake Mangum', 'Hand': 'S', 'K_pct': 18.0, 'O_Swing': 32, 'Z_Contact': 88},
            {'Name': 'Joey Bart', 'Hand': 'R', 'K_pct': 30.0, 'O_Swing': 34, 'Z_Contact': 80}
        ],
        'home_lineup_names': ['Geraldo Perdomo', 'Ketel Marte', 'Corbin Carroll', 'Adrian Del Castillo', 'Ildemaro Vargas', 'Jordan Fernandez', 'Jorge Barrosa', 'James McCann', 'Alek Thomas'],
        'home_lineup_hands': ['S', 'S', 'L', 'L', 'S', 'R', 'S', 'R', 'L'],
        'home_lineup_statcast': [
            {'Name': 'Geraldo Perdomo', 'Hand': 'S', 'K_pct': 11.2, 'O_Swing': 24, 'Z_Contact': 92},
            {'Name': 'Ketel Marte', 'Hand': 'S', 'K_pct': 15.4, 'O_Swing': 28, 'Z_Contact': 90},
            {'Name': 'Corbin Carroll', 'Hand': 'L', 'K_pct': 23.4, 'O_Swing': 28, 'Z_Contact': 84},
            {'Name': 'Adrian Del Castillo', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 30, 'Z_Contact': 85},
            {'Name': 'Ildemaro Vargas', 'Hand': 'S', 'K_pct': 14.8, 'O_Swing': 28, 'Z_Contact': 90},
            {'Name': 'Jordan Fernandez', 'Hand': 'R', 'K_pct': 25.0, 'O_Swing': 30, 'Z_Contact': 84},
            {'Name': 'Jorge Barrosa', 'Hand': 'S', 'K_pct': 20.0, 'O_Swing': 28, 'Z_Contact': 88},
            {'Name': 'James McCann', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 42.9, 'Z_Contact': 66.7},
            {'Name': 'Alek Thomas', 'Hand': 'L', 'K_pct': 21.2, 'O_Swing': 33, 'Z_Contact': 85}
        ],
        'away_catcher': 'Joey Bart',
        'home_catcher': 'James McCann',
        'away_drs': 5,
        'home_drs': 2,
        'away_manager_hook': 0.0,
        'home_manager_hook': -0.5, # Quicker hook for struggling Gallen
        'away_bp_pitches_d1': 20,
        'away_bp_pitches_d2': 45,
        'home_bp_pitches_d1': 40,
        'home_bp_pitches_d2': 30
    }
    
    # Run simulation
    # We clear canonical locks to ensure it runs
    omni.clear_canonical()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
    return results

if __name__ == "__main__":
    run_simulation()