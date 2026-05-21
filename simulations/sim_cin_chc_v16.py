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
from omni_prophet_v16 import OmniProphetV16

# OMNI-PROPHET V16.0 SIMULATION: CIN @ CHC
# DATE: 2026-05-04

game_data = {
    'away_team': 'CIN',
    'home_team': 'CHC',
    'game_time': '19:10',
    'is_dome': False,
    'park_factor': 102,
    
    # Starting Pitchers
    'away_sp_name': 'Chase Petty',
    'home_sp_name': 'Edward Cabrera',
    'away_sp_hand': 'R',
    'home_sp_hand': 'R',
    'away_sp_era': 4.38,
    'home_sp_era': 3.06,
    
    'away_sp_statcast': {
        'Full Name': 'Chase Petty',
        'Hand': 'R',
        'ERA': 4.38,
        'Stuff': 105,
        'VAA': -4.8,
        'K_pct': 27.5,
        'BB_pct': 10.5,
        'IP': 24.2,
        'xERA': 4.25,
    },
    
    'home_sp_statcast': {
        'Full Name': 'Edward Cabrera',
        'Hand': 'R',
        'ERA': 3.06,
        'Stuff': 118,
        'VAA': -4.2,
        'K_pct': 20.1,
        'BB_pct': 8.3,
        'IP': 35.1,
        'xERA': 3.45,
    },
    
    'away_lineup_names': ['TJ Friedl', 'JJ Bleday', 'Elly De La Cruz', 'Sal Stewart', 'Nathaniel Lowe', 'Spencer Steer', 'Tyler Stephenson', 'Will Benson', 'Ke\'Bryan Hayes'],
    'away_lineup_hands': ['L', 'L', 'S', 'R', 'L', 'R', 'R', 'L', 'R'],
    'away_lineup_statcast': [
        {'K_pct': 24.6, 'O_Swing': 31.0, 'Z_Contact': 82.0},
        {'K_pct': 13.3, 'O_Swing': 24.0, 'Z_Contact': 88.0},
        {'K_pct': 32.3, 'O_Swing': 38.0, 'Z_Contact': 72.0},
        {'K_pct': 20.5, 'O_Swing': 28.0, 'Z_Contact': 85.0},
        {'K_pct': 21.3, 'O_Swing': 26.0, 'Z_Contact': 86.0},
        {'K_pct': 22.1, 'O_Swing': 29.0, 'Z_Contact': 84.0},
        {'K_pct': 24.8, 'O_Swing': 32.0, 'Z_Contact': 81.0},
        {'K_pct': 31.5, 'O_Swing': 34.0, 'Z_Contact': 75.0},
        {'K_pct': 19.8, 'O_Swing': 30.0, 'Z_Contact': 87.0}
    ],
    
    'home_lineup_names': ['Nico Hoerner', 'Moises Ballesteros', 'Alex Bregman', 'Ian Happ', 'Seiya Suzuki', 'Michael Busch', 'Carson Kelly', 'Pete Crow-Armstrong', 'Dansby Swanson'],
    'home_lineup_hands': ['R', 'L', 'R', 'S', 'R', 'L', 'R', 'L', 'R'],
    'home_lineup_statcast': [
        {'K_pct': 14.2, 'O_Swing': 22.0, 'Z_Contact': 92.0},
        {'K_pct': 21.5, 'O_Swing': 33.0, 'Z_Contact': 83.0},
        {'K_pct': 13.8, 'O_Swing': 23.0, 'Z_Contact': 90.0},
        {'K_pct': 22.4, 'O_Swing': 28.0, 'Z_Contact': 84.0},
        {'K_pct': 23.5, 'O_Swing': 30.0, 'Z_Contact': 82.0},
        {'K_pct': 25.8, 'O_Swing': 33.0, 'Z_Contact': 79.0},
        {'K_pct': 24.2, 'O_Swing': 31.0, 'Z_Contact': 81.0},
        {'K_pct': 28.5, 'O_Swing': 35.0, 'Z_Contact': 77.0},
        {'K_pct': 26.5, 'O_Swing': 32.0, 'Z_Contact': 80.0}
    ],
    
    'env': {
        'Weather': {'temp': 74, 'wind_speed': 17, 'wind_dir': 0, 'humidity': 58},
        'altitude': 600,
        'rain_intensity': 0.19,
        'Umpire': {'name': 'Bill Miller', 'CS_pct': 16.5, 'zone_type': 'neutral'}
    },
    
    'away_drs': -2,
    'home_drs': 5,
    'away_manager_hook': 0.0,
    'home_manager_hook': 0.3,
    'away_bp_pitches_d1': 45,
    'away_bp_pitches_d2': 30,
    'home_bp_pitches_d1': 55,
    'home_bp_pitches_d2': 25,
    'away_catcher': 'Tyler Stephenson',
    'home_catcher': 'Carson Kelly',
}

market_odds = {
    'CHC ML': -219,
    'CIN ML': 185,
    'Total Over 11.5': -110,
    'Total Under 11.5': -110,
    'Petty Over 4.5 K': -110,
    'Cabrera Over 5.5 K': -110,
}

if __name__ == "__main__":
    omni = OmniProphetV16()
    omni.run_omni_simulation(game_data, market_odds=market_odds)