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

game_data = {
    'away_team': 'NYM',
    'home_team': 'COL',
    'away_sp_name': 'David Peterson',
    'home_sp_name': 'Tomoyuki Sugano',
    'away_sp_hand': 'L',
    'home_sp_hand': 'R',
    'away_sp_era': 6.53,
    'home_sp_era': 2.84,
    'away_lineup_names': [
        'Juan Soto', 'Bo Bichette', 'MJ Melendez', 'Mark Vientos', 
        'Brett Baty', 'Marcus Semien', 'Carson Benge', 'Francisco Alvarez', 'Luis Torrens'
    ],
    'away_lineup_hands': ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'R'],
    'home_lineup_names': [
        'Mickey Moniak', 'Tyler Freeman', 'TJ Rumfield', 'Hunter Goodman', 
        'Willi Castro', 'Jordan Beck', 'Kyle Karros', 'Ezequiel Tovar', 'Brenton Doyle'
    ],
    'home_lineup_hands': ['L', 'R', 'L', 'R', 'S', 'R', 'R', 'R', 'R'],
    
    'away_sp_statcast': {
        'Stuff': 91,
        'VAA': -1.3,
        'K_pct': 20.1,
        'BB_pct': 9.7,
        'IP': 30.1,
        'xERA': 3.42,
        'CSW_L3': 25.17,
        'SwStr_L3': 8.27,
        'VeloTrend': 'Gaining'
    },
    'home_sp_statcast': {
        'Stuff': 98,
        'VAA': -1.5,
        'K_pct': 16.3,
        'BB_pct': 7.0,
        'IP': 31.2,
        'xERA': 4.15,
        'CSW_L3': 28.0,
        'SwStr_L3': 8.0,
        'VeloTrend': 'Stable'
    },
    
    'away_lineup_statcast': [
        {'K_pct': 15.0, 'O_Swing': 20.0, 'Z_Contact': 90.0},
        {'K_pct': 18.0, 'O_Swing': 35.0, 'Z_Contact': 88.0},
        {'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 82.0},
        {'K_pct': 28.0, 'O_Swing': 38.0, 'Z_Contact': 78.0},
        {'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 80.0},
        {'K_pct': 16.0, 'O_Swing': 25.0, 'Z_Contact': 92.0},
        {'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 84.0},
        {'K_pct': 26.0, 'O_Swing': 33.0, 'Z_Contact': 77.0},
        {'K_pct': 24.0, 'O_Swing': 30.0, 'Z_Contact': 80.0}
    ],
    'home_lineup_statcast': [
        {'K_pct': 32.0, 'O_Swing': 40.0, 'Z_Contact': 75.0},
        {'K_pct': 18.0, 'O_Swing': 28.0, 'Z_Contact': 88.0},
        {'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 85.0},
        {'K_pct': 30.0, 'O_Swing': 38.0, 'Z_Contact': 72.0},
        {'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 82.0},
        {'K_pct': 28.0, 'O_Swing': 36.0, 'Z_Contact': 78.0},
        {'K_pct': 25.0, 'O_Swing': 32.0, 'Z_Contact': 80.0},
        {'K_pct': 26.0, 'O_Swing': 34.0, 'Z_Contact': 82.0},
        {'K_pct': 29.0, 'O_Swing': 38.0, 'Z_Contact': 75.0}
    ],
    
    'env': {
        'Weather': {
            'temp': 69,
            'wind_speed': 12,
            'wind_dir': 49, # 49 degrees from CF (Blowing OUT to RF)
            'humidity': 24
        },
        'altitude': 5200,
        'rain_intensity': 0.0,
        'adi': 84.1,
        'Umpire': {
            'name': 'D.J. Reyburn',
            'zone_type': 'neutral',
            'CS_pct': 16.2
        }
    },
    'park_factor': 115,
    'is_dome': False,
    'game_time': '17:40',
    'away_drs': 12,
    'home_drs': -18,
    'away_manager_hook': -0.3, # Mendoza: Aggressive
    'home_manager_hook': 0.3,  # Bud Black: Extended
    'away_bp_pitches_d1': 32,
    'away_bp_pitches_d2': 86,
    'home_bp_pitches_d1': 87,
    'home_bp_pitches_d2': 64,
    'away_catcher': 'Luis Torrens',
    'home_catcher': 'Hunter Goodman'
}

market_odds = {
    'NYM Moneyline': -143,
    'COL Moneyline': 120,
    'Total O/U 10.5': -110
}

if __name__ == '__main__':
    omni = OmniProphetV16()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)