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

from datetime import datetime

# Add workspace to path
sys.path.append("/Users/danielreiss/Desktop/Antigravity/MLB")
from omni_prophet_v16 import OmniProphetV16

# ── GAME DATA HARVESTED 2026-05-06 ──────────────────────────
game_data = {
    'away_team': 'NYM',
    'home_team': 'COL',
    'away_sp_name': 'Freddy Peralta',
    'home_sp_name': 'Michael Lorenzen',
    'away_sp_hand': 'R',
    'home_sp_hand': 'R',
    'away_sp_era': 3.52,
    'home_sp_era': 6.09,
    
    # METS LINEUP (Confirmed)
    'away_lineup_names': [
        'Juan Soto', 'Bo Bichette', 'MJ Melendez', 'Mark Vientos', 
        'Brett Baty', 'Marcus Semien', 'Carson Benge', 'Francisco Alvarez', 'Luis Torrens'
    ],
    'away_lineup_hands': ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'R'],
    
    # ROCKIES LINEUP (Confirmed)
    'home_lineup_names': [
        'Edouard Julien', 'Mickey Moniak', 'Hunter Goodman', 'TJ Rumfield', 
        'Tyler Freeman', 'Troy Johnston', 'Kyle Karros', 'Ezequiel Tovar', 'Jake McCarthy'
    ],
    'home_lineup_hands': ['L', 'L', 'R', 'L', 'R', 'L', 'R', 'R', 'L'],
    
    # PITCHER STATS (Statcast Telemetry)
    'away_sp_statcast': {
        'Stuff': 98,
        'VAA': -4.2,
        'K_pct': 25.9,
        'BB_pct': 9.4,
        'IP': 26.2,
        'xERA': 3.72,
        'CSW_L3': 27.5,
        'SwStr_L3': 11.2,
        'VeloTrend': 'Stable'
    },
    'home_sp_statcast': {
        'Stuff': 90,
        'VAA': -4.8,
        'K_pct': 16.7,
        'BB_pct': 6.2,
        'IP': 35.0,
        'xERA': 6.35,
        'CSW_L3': 24.1,
        'SwStr_L3': 8.5,
        'VeloTrend': 'Stable'
    },
    
    # LINEUP STATS (Projected & Historical Blend)
    'away_lineup_statcast': [
        {'K_pct': 21.4, 'O_Swing': 21.0, 'Z_Contact': 88.5}, # Soto
        {'K_pct': 15.3, 'O_Swing': 34.2, 'Z_Contact': 87.1}, # Bichette
        {'K_pct': 25.0, 'O_Swing': 29.5, 'Z_Contact': 81.2}, # Melendez
        {'K_pct': 28.0, 'O_Swing': 37.1, 'Z_Contact': 78.4}, # Vientos
        {'K_pct': 26.0, 'O_Swing': 31.8, 'Z_Contact': 80.5}, # Baty
        {'K_pct': 16.0, 'O_Swing': 26.5, 'Z_Contact': 91.2}, # Semien
        {'K_pct': 22.0, 'O_Swing': 28.1, 'Z_Contact': 84.6}, # Benge
        {'K_pct': 25.0, 'O_Swing': 32.7, 'Z_Contact': 77.3}, # Alvarez
        {'K_pct': 22.0, 'O_Swing': 29.8, 'Z_Contact': 79.5}  # Torrens
    ],
    'home_lineup_statcast': [
        {'K_pct': 28.0, 'O_Swing': 24.5, 'Z_Contact': 79.1}, # Julien
        {'K_pct': 32.0, 'O_Swing': 41.2, 'Z_Contact': 74.8}, # Moniak
        {'K_pct': 29.1, 'O_Swing': 37.5, 'Z_Contact': 72.4}, # Goodman
        {'K_pct': 22.0, 'O_Swing': 29.8, 'Z_Contact': 82.3}, # Rumfield
        {'K_pct': 13.9, 'O_Swing': 27.4, 'Z_Contact': 89.2}, # Freeman
        {'K_pct': 25.0, 'O_Swing': 31.2, 'Z_Contact': 80.1}, # Johnston
        {'K_pct': 24.0, 'O_Swing': 33.5, 'Z_Contact': 81.4}, # Karros
        {'K_pct': 27.6, 'O_Swing': 34.1, 'Z_Contact': 81.8}, # Tovar
        {'K_pct': 20.0, 'O_Swing': 30.5, 'Z_Contact': 85.2}  # McCarthy
    ],
    
    'env': {
        'Weather': {
            'temp': 40,
            'wind_speed': 6,
            'wind_dir': 0, # Straight out to CF
            'humidity': 30
        },
        'altitude': 5200,
        'rain_intensity': 0.0,
        'adi': 82.5,
        'Umpire': {
            'name': 'Neutral Umpire',
            'zone_type': 'neutral',
            'CS_pct': 16.0
        }
    },
    'park_factor': 118, # Adjusted Coors for cold (Normally 130)
    'is_dome': False,
    'game_time': '21:20',
    'away_drs': 5,  # Mets defense slightly positive
    'home_drs': -12, # Rockies defense struggle
    'away_manager_hook': -0.2, # Mendoza
    'home_manager_hook': 0.2,  # Bud Black
    'away_bp_pitches_d1': 15,
    'away_bp_pitches_d2': 45,
    'home_bp_pitches_d1': 20,
    'home_bp_pitches_d2': 50,
    'away_catcher': 'Luis Torrens',
    'home_catcher': 'Hunter Goodman'
}

market_odds = {
    'NYM Moneyline': -161,
    'COL Moneyline': 140,
    'Total O/U 9.5': -110,
    'Freddy Peralta Strikeouts 5.5': -115,
    'Michael Lorenzen Strikeouts 4.5': +105
}

if __name__ == '__main__':
    omni = OmniProphetV16()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)