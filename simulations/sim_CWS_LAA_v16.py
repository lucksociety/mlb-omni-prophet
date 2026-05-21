
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
from omni_prophet_v16 import OmniProphetV16

def run_simulation():
    omni = OmniProphetV16()
    
    # Research Data from Phase 1
    game_data = {
        'away_team': 'CWS',
        'home_team': 'LAA',
        'away_sp_name': 'Davis Martin',
        'home_sp_name': 'Jose Soriano',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': 1.95,
        'home_sp_era': 0.84,
        'away_lineup_names': ['S. Antonacci', 'M. Murakami', 'M. Vargas', 'C. Montgomery', 'C. Meidroth', 'A. Benintendi', 'J. Kelenic', 'T. Peters', 'Drew Romo'],
        'away_lineup_hands': ['L', 'L', 'R', 'L', 'R', 'L', 'L', 'L', 'S'],
        'home_lineup_names': ['Zach Neto', 'Mike Trout', 'N. Schanuel', 'Jorge Soler', 'Yoan Moncada', 'Jo Adell', 'Josh Lowe', 'T. d\'Arnaud', 'Adam Frazier'],
        'home_lineup_hands': ['R', 'R', 'L', 'R', 'S', 'R', 'L', 'R', 'L'],
        'away_sp_statcast': {
            'Stuff': 104,
            'K_pct': 22.9,
            'BB_pct': 5.6,
            'IP': 37.0,
            'VAA': -4.5,
            'xERA': 3.42,
            'CSW_pct': 27.8,
            'SwStr_pct': 11.7
        },
        'home_sp_statcast': {
            'Stuff': 128,
            'K_pct': 30.1,
            'BB_pct': 9.8,
            'IP': 42.2,
            'VAA': -4.2,
            'xERA': 2.89,
            'CSW_pct': 29.5, # Estimated
            'SwStr_pct': 13.2 # Estimated
        },
        'away_lineup_statcast': [
            {'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 85.0}, # Antonacci
            {'K_pct': 26.5, 'O_Swing': 30.5, 'Z_Contact': 82.0}, # Murakami
            {'K_pct': 21.0, 'O_Swing': 28.0, 'Z_Contact': 88.0}, # Vargas
            {'K_pct': 27.0, 'O_Swing': 33.0, 'Z_Contact': 81.0}, # Montgomery
            {'K_pct': 23.5, 'O_Swing': 29.0, 'Z_Contact': 86.0}, # Meidroth
            {'K_pct': 20.0, 'O_Swing': 26.0, 'Z_Contact': 89.0}, # Benintendi
            {'K_pct': 28.5, 'O_Swing': 35.0, 'Z_Contact': 79.0}, # Kelenic
            {'K_pct': 27.0, 'O_Swing': 31.0, 'Z_Contact': 83.0}, # Peters
            {'K_pct': 25.0, 'O_Swing': 34.0, 'Z_Contact': 80.0}, # Romo
        ],
        'home_lineup_statcast': [
            {'K_pct': 32.7, 'O_Swing': 30.6, 'Z_Contact': 81.0}, # Neto
            {'K_pct': 25.0, 'O_Swing': 28.0, 'Z_Contact': 84.0}, # Trout
            {'K_pct': 19.0, 'O_Swing': 24.0, 'Z_Contact': 91.0}, # Schanuel
            {'K_pct': 26.0, 'O_Swing': 32.0, 'Z_Contact': 80.0}, # Soler
            {'K_pct': 14.6, 'O_Swing': 25.0, 'Z_Contact': 82.3}, # Moncada
            {'K_pct': 29.0, 'O_Swing': 36.0, 'Z_Contact': 78.0}, # Adell
            {'K_pct': 28.6, 'O_Swing': 33.0, 'Z_Contact': 78.4}, # Lowe
            {'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 85.0}, # d'Arnaud
            {'K_pct': 18.0, 'O_Swing': 23.0, 'Z_Contact': 92.0}, # Frazier
        ],
        'env': {
            'Weather': {
                'temp': 64,
                'wind_speed': 10,
                'wind_dir': 0, # Blowing out
                'humidity': 65
            },
            'altitude': 160,
            'rain_intensity': 0.0,
            'Umpire': {
                'name': 'Not announced yet',
                'zone_type': 'neutral',
                'CS_pct': 16.5
            }
        },
        'park_factor': 100,
        'is_dome': False,
        'away_drs': -10,
        'home_drs': 5,
        'away_manager_hook': -0.2,
        'home_manager_hook': 0.2,
        'away_bp_pitches_d1': 65,
        'away_bp_pitches_d2': 80,
        'home_bp_pitches_d1': 45,
        'home_bp_pitches_d2': 70,
        'away_catcher': 'Drew Romo',
        'home_catcher': 'Travis d\'Arnaud',
        'game_time': '21:38'
    }
    
    market_odds = {
        'LAA ML': -161,
        'CWS ML': 140,
        'Total O 7.5': -110,
        'Total U 7.5': -110
    }
    
    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == "__main__":
    run_simulation()