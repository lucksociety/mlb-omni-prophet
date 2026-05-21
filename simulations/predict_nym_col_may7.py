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

# ── GAME DATA HARVESTED 2026-05-07 ──────────────────────────
game_data = {
    'away_team': 'NYM',
    'home_team': 'COL',
    'away_sp_name': 'Christian Scott',
    'home_sp_name': 'Jose Quintana',
    'away_sp_hand': 'R',
    'home_sp_hand': 'L',
    'away_sp_era': 4.26,
    'home_sp_era': 4.07,
    
    # METS LINEUP (Confirmed via Screenshot)
    'away_lineup_names': [
        'Juan Soto', 'Bo Bichette', 'Mark Vientos', 'A. Slater', 
        'Marcus Semien', 'Andy Ibanez', 'Francisco Alvarez', 'Tyrone Taylor', 'Vidal Brujan'
    ],
    'away_lineup_hands': ['L', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'S'],
    
    # ROCKIES LINEUP (Confirmed via Screenshot)
    'home_lineup_names': [
        'Edouard Julien', 'Mickey Moniak', 'Tyler Freeman', 'TJ Rumfield', 
        'Troy Johnston', 'Willi Castro', 'Jake McCarthy', 'Kyle Karros', 'Brett Sullivan'
    ],
    'home_lineup_hands': ['L', 'L', 'R', 'L', 'L', 'S', 'L', 'R', 'L'],
    
    # PITCHER STATS (2026 Statcast Telemetry)
    'away_sp_statcast': {
        'Stuff': 105,
        'VAA': -1.4,
        'K_pct': 23.0,
        'BB_pct': 6.5,
        'IP': 6.1, # Rookie/Young Status
        'xERA': 3.90,
        'CSW_L3': 28.5,
        'SwStr_L3': 12.8,
        'VeloTrend': 'Stable'
    },
    'home_sp_statcast': {
        'Stuff': 90,
        'VAA': -1.2,
        'K_pct': 14.2,
        'BB_pct': 9.0,
        'IP': 31.0,
        'xERA': 4.40,
        'CSW_L3': 20.5,
        'SwStr_L3': 8.2,
        'VeloTrend': 'Stable'
    },
    
    # LINEUP STATS (2026 Split-Aware)
    'away_lineup_statcast': [
        {'K_pct': 21.4, 'O_Swing': 21.0, 'Z_Contact': 88.5}, # Soto
        {'K_pct': 20.0, 'O_Swing': 34.2, 'Z_Contact': 87.1}, # Bichette (vs LHP)
        {'K_pct': 20.0, 'O_Swing': 37.1, 'Z_Contact': 78.4}, # Vientos (vs LHP)
        {'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 82.0}, # Slater
        {'K_pct': 19.2, 'O_Swing': 26.5, 'Z_Contact': 91.2}, # Semien (vs LHP)
        {'K_pct': 24.0, 'O_Swing': 30.0, 'Z_Contact': 80.0}, # Ibanez
        {'K_pct': 26.1, 'O_Swing': 32.7, 'Z_Contact': 77.3}, # Alvarez (vs LHP)
        {'K_pct': 17.4, 'O_Swing': 28.1, 'Z_Contact': 84.6}, # Taylor (vs LHP)
        {'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 85.0}  # Brujan
    ],
    'home_lineup_statcast': [
        {'K_pct': 25.0, 'O_Swing': 24.5, 'Z_Contact': 79.1}, # Julien (vs RHP)
        {'K_pct': 18.5, 'O_Swing': 41.2, 'Z_Contact': 74.8}, # Moniak (vs RHP)
        {'K_pct': 13.9, 'O_Swing': 27.4, 'Z_Contact': 89.2}, # Freeman (vs RHP)
        {'K_pct': 17.2, 'O_Swing': 29.8, 'Z_Contact': 82.3}, # Rumfield (vs RHP)
        {'K_pct': 22.5, 'O_Swing': 31.2, 'Z_Contact': 80.1}, # Johnston (vs RHP)
        {'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 82.0}, # Castro
        {'K_pct': 40.0, 'O_Swing': 35.0, 'Z_Contact': 80.0}, # McCarthy
        {'K_pct': 19.2, 'O_Swing': 33.5, 'Z_Contact': 81.4}, # Karros (vs RHP)
        {'K_pct': 24.0, 'O_Swing': 30.0, 'Z_Contact': 80.0}  # Sullivan
    ],
    
    'env': {
        'Weather': {
            'temp': 63,
            'wind_speed': 7,
            'wind_dir': 90, # Left-to-Right
            'humidity': 15
        },
        'altitude': 5200,
        'rain_intensity': 0.0,
        'adi': 81.5,
        'Umpire': {
            'name': 'Neutral',
            'zone_type': 'neutral',
            'CS_pct': 16.0
        }
    },
    'park_factor': 130, # Coors Standard
    'is_dome': False,
    'game_time': '15:10',
    'away_drs': 2,
    'home_drs': -15, # Rockies defensive struggle
    'away_manager_hook': -0.2, # Mendoza (Aggressive)
    'home_manager_hook': 0.2,  # Bud Black (Extended)
    'away_bp_pitches_d1': 45, # Tired bullpen
    'away_bp_pitches_d2': 32,
    'home_bp_pitches_d1': 20,
    'home_bp_pitches_d2': 40,
    'away_catcher': 'Francisco Alvarez', # Elite framing
    'home_catcher': 'Brett Sullivan'
}

market_odds = {
    'NYM Moneyline': -144,
    'NYM Runline -1.5': 105,
    'Total Over 11.0': -105,
    'Christian Scott Strikeouts 4.5 Under': -170,
    'Jose Quintana Strikeouts 2.5 Over': -160,
    'YRFI Yes': -145
}

if __name__ == '__main__':
    omni = OmniProphetV16()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)