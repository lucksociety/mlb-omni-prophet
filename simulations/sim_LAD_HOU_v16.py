
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

# Add the directory to path so we can import OmniProphet
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV16

def run_simulation():
    omni = OmniProphetV16()
    
    market_odds = {
        'LAD ML': -207,
        'HOU ML': 175,
        'Total O/U 9.0': -110
    }

    # Fixing all keys to match KProphet/QE expectations (Capitalized)
    game_data = {
        'away_team': 'LAD',
        'home_team': 'HOU',
        'game_time': '20:10', # Engine expects HH:MM
        'is_dome': True,
        'park_factor': 104,
        'env': {
            'Weather': {
                'temp': 72,
                'wind_speed': 0,
                'wind_dir': 0,
                'humidity': 50
            },
            'altitude': 31,
            'rain_intensity': 0.0,
            'Umpire': {
                'name': 'Neutral',
                'CS_pct': 17.5,
                'zone_type': 'neutral'
            }
        },
        'away_sp_name': 'Yoshinobu Yamamoto',
        'away_sp_hand': 'R',
        'away_sp_era': 2.87,
        'away_sp_statcast': {
            'Name': 'Yoshinobu Yamamoto',
            'Hand': 'R',
            'Stuff': 112,
            'K_pct': 21.8,
            'BB_pct': 6.1,
            'VAA': -4.3,
            'IP': 37.2,
            'xERA': 3.98,
            'L3_CSW': 28.5,
            'L3_SwStr': 13.5
        },
        'home_sp_name': 'Ryan Weiss',
        'home_sp_hand': 'R',
        'home_sp_era': 6.65,
        'home_sp_statcast': {
            'Name': 'Ryan Weiss',
            'Hand': 'R',
            'Stuff': 104,
            'K_pct': 23.6,
            'BB_pct': 15.1,
            'VAA': -4.8,
            'IP': 21.2,
            'xERA': 6.37,
            'L3_CSW': 28.5,
            'L3_SwStr': 11.9
        },
        'away_lineup_names': ['Shohei Ohtani', 'Freddie Freeman', 'Will Smith', 'Teoscar Hernandez', 'Kyle Tucker', 'Max Muncy', 'Andy Pages', 'Hyeseong Kim', 'Alex Freeland'],
        'away_lineup_hands': ['L', 'L', 'R', 'R', 'L', 'L', 'R', 'L', 'S'],
        'away_lineup_statcast': [
            {'Name': 'Shohei Ohtani', 'Hand': 'L', 'K_pct': 24, 'O_Swing': 28, 'Z_Contact': 85},
            {'Name': 'Freddie Freeman', 'Hand': 'L', 'K_pct': 16, 'O_Swing': 22, 'Z_Contact': 92},
            {'Name': 'Will Smith', 'Hand': 'R', 'K_pct': 18, 'O_Swing': 25, 'Z_Contact': 88},
            {'Name': 'Teoscar Hernandez', 'Hand': 'R', 'K_pct': 28, 'O_Swing': 35, 'Z_Contact': 82},
            {'Name': 'Kyle Tucker', 'Hand': 'L', 'K_pct': 15, 'O_Swing': 23, 'Z_Contact': 90},
            {'Name': 'Max Muncy', 'Hand': 'L', 'K_pct': 25, 'O_Swing': 20, 'Z_Contact': 80},
            {'Name': 'Andy Pages', 'Hand': 'R', 'K_pct': 26, 'O_Swing': 32, 'Z_Contact': 84},
            {'Name': 'Hyeseong Kim', 'Hand': 'L', 'K_pct': 19, 'O_Swing': 24, 'Z_Contact': 88},
            {'Name': 'Alex Freeland', 'Hand': 'S', 'K_pct': 22, 'O_Swing': 27, 'Z_Contact': 86}
        ],
        'home_lineup_names': ['Carlos Correa', 'Yordan Alvarez', 'Isaac Paredes', 'Christian Walker', 'Jose Altuve', 'Brice Matthews', 'Cam Smith', 'Zach Cole', 'Christian Vazquez'],
        'home_lineup_hands': ['R', 'L', 'R', 'R', 'R', 'R', 'R', 'L', 'R'],
        'home_lineup_statcast': [
            {'Name': 'Carlos Correa', 'Hand': 'R', 'K_pct': 20, 'O_Swing': 26, 'Z_Contact': 88},
            {'Name': 'Yordan Alvarez', 'Hand': 'L', 'K_pct': 18, 'O_Swing': 24, 'Z_Contact': 86},
            {'Name': 'Isaac Paredes', 'Hand': 'R', 'K_pct': 14, 'O_Swing': 22, 'Z_Contact': 90},
            {'Name': 'Christian Walker', 'Hand': 'R', 'K_pct': 22, 'O_Swing': 28, 'Z_Contact': 84},
            {'Name': 'Jose Altuve', 'Hand': 'R', 'K_pct': 15, 'O_Swing': 32, 'Z_Contact': 92},
            {'Name': 'Brice Matthews', 'Hand': 'R', 'K_pct': 25, 'O_Swing': 30, 'Z_Contact': 82},
            {'Name': 'Cam Smith', 'Hand': 'R', 'K_pct': 24, 'O_Swing': 29, 'Z_Contact': 85},
            {'Name': 'Zach Cole', 'Hand': 'L', 'K_pct': 23, 'O_Swing': 26, 'Z_Contact': 84},
            {'Name': 'Christian Vazquez', 'Hand': 'R', 'K_pct': 18, 'O_Swing': 35, 'Z_Contact': 88}
        ],
        'away_catcher': 'Will Smith',
        'home_catcher': 'Christian Vazquez',
        'away_drs': 12,
        'home_drs': -4,
        'away_manager_hook': 0.0,
        'home_manager_hook': 0.0,
        'away_bp_pitches_d1': 192,
        'away_bp_pitches_d2': 45,
        'home_bp_pitches_d1': 85,
        'home_bp_pitches_d2': 110
    }
    
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
    return results

if __name__ == "__main__":
    run_simulation()