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

# Add the directory to sys.path
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV16

def run_simulation():
    omni = OmniProphetV16()
    
    # CALIBRATION MODIFIERS from Phase 0
    calibration_total_adj = -0.43
    calibration_k_factor = 1.032

    game_data = {
        'away_team': 'TOR',
        'home_team': 'TB',
        'away_sp_name': 'Eric Lauer',
        'away_sp_hand': 'L',
        'away_sp_era': 6.00,
        'away_sp_statcast': {
            'Stuff': 100,
            'K_pct': 16.4,
            'VAA': -4.5,
            'BB_pct': 10.7,
            'IP': 22.1,
            'xERA': 6.48
        },
        
        'home_sp_name': 'Nick Martinez',
        'home_sp_hand': 'R',
        'home_sp_era': 1.70,
        'home_sp_statcast': {
            'Stuff': 118,
            'K_pct': 16.4,
            'VAA': -4.5,
            'BB_pct': 6.1,
            'IP': 22.0,
            'xERA': 3.70
        },
        
        'away_lineup_names': ['Y. Pinango', 'K. Okamoto', 'V. Guerrero', 'J. Sanchez', 'E. Clement', 'D. Varsho', 'Myles Straw', 'A. Gimenez', 'B. Valenzuela'],
        'away_lineup_hands': ['L', 'R', 'R', 'L', 'R', 'L', 'R', 'L', 'S'],
        'away_lineup_statcast': [
            {'name': 'Y. Pinango', 'hand': 'L', 'K_pct': 20.0, 'O_Swing': 30.0, 'Z_Contact': 85.0},
            {'name': 'K. Okamoto', 'hand': 'R', 'K_pct': 19.2, 'O_Swing': 32.0, 'Z_Contact': 82.0},
            {'name': 'V. Guerrero', 'hand': 'R', 'K_pct': 7.7, 'O_Swing': 25.0, 'Z_Contact': 90.0},
            {'name': 'J. Sanchez', 'hand': 'L', 'K_pct': 19.5, 'O_Swing': 33.0, 'Z_Contact': 80.0},
            {'name': 'E. Clement', 'hand': 'R', 'K_pct': 3.6, 'O_Swing': 20.0, 'Z_Contact': 95.0},
            {'name': 'D. Varsho', 'hand': 'L', 'K_pct': 12.0, 'O_Swing': 28.0, 'Z_Contact': 88.0},
            {'name': 'Myles Straw', 'hand': 'R', 'K_pct': 12.5, 'O_Swing': 22.0, 'Z_Contact': 92.0},
            {'name': 'A. Gimenez', 'hand': 'L', 'K_pct': 16.0, 'O_Swing': 26.0, 'Z_Contact': 87.0},
            {'name': 'B. Valenzuela', 'hand': 'S', 'K_pct': 22.0, 'O_Swing': 31.0, 'Z_Contact': 83.0}
        ],
        
        'home_lineup_names': ['C. Simpson', 'J. Caminero', 'Ryan Vilade', 'Yandy Diaz', 'J. Aranda', 'Jonny DeLuca', 'B. Williamson', 'Nick Fortes', 'Taylor Walls'],
        'home_lineup_hands': ['L', 'R', 'R', 'R', 'L', 'R', 'R', 'R', 'S'],
        'home_lineup_statcast': [
            {'name': 'C. Simpson', 'hand': 'L', 'K_pct': 8.1, 'O_Swing': 24.0, 'Z_Contact': 91.0},
            {'name': 'J. Caminero', 'hand': 'R', 'K_pct': 19.4, 'O_Swing': 33.0, 'Z_Contact': 84.0},
            {'name': 'Ryan Vilade', 'hand': 'R', 'K_pct': 20.0, 'O_Swing': 32.0, 'Z_Contact': 82.0},
            {'name': 'Yandy Diaz', 'hand': 'R', 'K_pct': 9.3, 'O_Swing': 21.0, 'Z_Contact': 94.0},
            {'name': 'J. Aranda', 'hand': 'L', 'K_pct': 20.2, 'O_Swing': 28.0, 'Z_Contact': 85.0},
            {'name': 'Jonny DeLuca', 'hand': 'R', 'K_pct': 22.2, 'O_Swing': 35.0, 'Z_Contact': 81.0},
            {'name': 'B. Williamson', 'hand': 'R', 'K_pct': 23.5, 'O_Swing': 34.0, 'Z_Contact': 80.0},
            {'name': 'Nick Fortes', 'hand': 'R', 'K_pct': 13.9, 'O_Swing': 26.0, 'Z_Contact': 89.0},
            {'name': 'Taylor Walls', 'hand': 'S', 'K_pct': 25.0, 'O_Swing': 22.0, 'Z_Contact': 85.0}
        ],
        
        'env': {
            'Weather': {
                'temp': 72,
                'wind_speed': 0,
                'wind_dir': 0,
                'humidity': 50
            },
            'altitude': 0,
            'rain_intensity': 0.0,
            'is_dome': True,
            'Umpire': {
                'name': 'Neutral Ump',
                'CS_pct': 16.5,
                'zone_type': 'neutral'
            }
        },
        
        'park_factor': 96,
        'game_time': '18:40',
        'away_catcher': 'Brandon Valenzuela',
        'home_catcher': 'Nick Fortes',
        'away_drs': 15,
        'home_drs': 0,
        'away_manager_hook': 0.0,
        'home_manager_hook': -0.3,
        'away_bp_pitches_d1': 60,
        'away_bp_pitches_d2': 20,
        'home_bp_pitches_d1': 95,
        'home_bp_pitches_d2': 85,
        'is_dome': True,
        
        'market_odds': {
            'away_ml': 115,
            'home_ml': -126,
            'total': 8.0
        }
    }

    # Run the simulation
    results = omni.run_omni_simulation(game_data)
    return results

if __name__ == "__main__":
    run_simulation()