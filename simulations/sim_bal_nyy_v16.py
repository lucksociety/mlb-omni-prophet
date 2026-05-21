
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

# ── RESEARCHED GAME DATA ──────────────────────────────────────────
game_data = {
    'away_team': 'BAL',
    'home_team': 'NYY',
    'away_sp_name': 'Shane Baz',
    'away_sp_hand': 'R',
    'away_sp_era': 4.50,
    'away_sp_statcast': {
        'Stuff': 112,
        'VAA': -4.2,
        'K_pct': 19.3,
        'BB_pct': 7.3,
        'IP': 34.0,
        'xERA': 3.80,
        'CSW_L3': 25.5,
        'SwStr_L3': 11.5
    },
    'home_sp_name': 'Cam Schlittler',
    'home_sp_hand': 'R',
    'home_sp_era': 1.51,
    'home_sp_statcast': {
        'Stuff': 125,
        'VAA': -3.8,
        'K_pct': 31.4,
        'BB_pct': 3.8,
        'IP': 41.2,
        'xERA': 2.40,
        'CSW_L3': 34.5,
        'SwStr_L3': 15.2
    },
    'away_lineup_names': [
        'G. Henderson', 'A. Rutschman', 'D. Beavers', 
        'Pete Alonso', 'S. Basallo', 'L. Taveras', 
        'C. Cowser', 'J. Jackson', 'B. Alexander'
    ],
    'away_lineup_hands': ['L', 'S', 'L', 'R', 'L', 'S', 'L', 'R', 'R'],
    'away_lineup_statcast': [
        {'K_pct': 31.0, 'O_Swing': 32.0, 'Z_Contact': 82.0},
        {'K_pct': 15.2, 'O_Swing': 24.0, 'Z_Contact': 89.0},
        {'K_pct': 28.0, 'O_Swing': 30.0, 'Z_Contact': 80.0},
        {'K_pct': 22.1, 'O_Swing': 31.0, 'Z_Contact': 83.0},
        {'K_pct': 24.0, 'O_Swing': 29.0, 'Z_Contact': 81.0},
        {'K_pct': 21.0, 'O_Swing': 28.0, 'Z_Contact': 85.0},
        {'K_pct': 29.7, 'O_Swing': 33.0, 'Z_Contact': 79.0},
        {'K_pct': 26.0, 'O_Swing': 30.0, 'Z_Contact': 82.0},
        {'K_pct': 25.0, 'O_Swing': 31.0, 'Z_Contact': 81.0},
    ],
    'home_lineup_names': [
        'T. Grisham', 'Aaron Judge', 'C. Bellinger', 
        'J. Dominguez', 'J. Chisholm', 'P. Goldschmidt', 
        'Austin Wells', 'Ryan McMahon', 'J. Caballero'
    ],
    'home_lineup_hands': ['L', 'R', 'L', 'S', 'L', 'R', 'L', 'L', 'R'],
    'home_lineup_statcast': [
        {'K_pct': 24.0, 'O_Swing': 22.0, 'Z_Contact': 84.0},
        {'K_pct': 28.0, 'O_Swing': 25.0, 'Z_Contact': 78.0},
        {'K_pct': 19.0, 'O_Swing': 28.0, 'Z_Contact': 86.0},
        {'K_pct': 22.0, 'O_Swing': 26.0, 'Z_Contact': 83.0},
        {'K_pct': 24.0, 'O_Swing': 29.0, 'Z_Contact': 82.0},
        {'K_pct': 22.0, 'O_Swing': 26.0, 'Z_Contact': 84.0},
        {'K_pct': 25.0, 'O_Swing': 24.0, 'Z_Contact': 85.0},
        {'K_pct': 31.1, 'O_Swing': 27.0, 'Z_Contact': 79.0},
        {'K_pct': 21.0, 'O_Swing': 24.0, 'Z_Contact': 86.0},
    ],
    'env': {
        'Weather': {
            'temp': 70.0,
            'wind_speed': 13.0,
            'wind_dir': 120.0, # Blowing R-L
            'humidity': 38.0
        },
        'Umpire': {
            'name': 'Marvin Hudson',
            'CS_pct': 16.5,
            'zone_type': 'neutral'
        },
        'altitude': 23.0,
        'rain_intensity': 0.0
    },
    'park_factor': 104,
    'is_dome': False,
    'away_catcher': 'Adley Rutschman',
    'home_catcher': 'Austin Wells',
    'game_time': '19:05',
    'away_drs': -5,
    'home_drs': 4,
    'away_manager_hook': 0.0,
    'home_manager_hook': -0.3,
    'away_bp_pitches_d1': 85,  # High usage
    'away_bp_pitches_d2': 60,
    'home_bp_pitches_d1': 40,  # Lower usage
    'home_bp_pitches_d2': 25
}

market_odds = {
    'NYY Moneyline': -219,
    'BAL Moneyline': 180,
    'Total Over 8.5': -110,
    'Total Under 8.5': -110
}

# ── EXECUTION ─────────────────────────────────────────────────────
omni = OmniProphetV16()
omni.run_omni_simulation(game_data, market_odds=market_odds)