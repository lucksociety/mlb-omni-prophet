
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

# Add the current directory to path so we can import the engines
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV15

def run_tex_det_sim():
    omni = OmniProphetV15()
    
    # Lineups (Name, Hand)
    away_lineup_names = [
        "Brandon Nimmo", "Andrew McCutchen", "Corey Seager", "Josh Jung", 
        "Jake Burger", "Evan Carter", "Ezequiel Duran", "Josh Smith", "Kyle Higashioka"
    ]
    away_lineup_hands = ["L", "R", "L", "R", "R", "L", "R", "L", "R"]
    
    home_lineup_names = [
        "Kevin McGonigle", "Matt Vierling", "Colt Keith", "Riley Greene", 
        "Spencer Torkelson", "Kerry Carpenter", "Wenceel Perez", "Hao-Yu Lee", "Jake Rogers"
    ]
    home_lineup_hands = ["L", "R", "L", "L", "R", "L", "S", "R", "R"]

    # Lineup Statcast (for Ace Trap / K-Prophet)
    # Estimates based on 2026 data gathered
    away_lineup_statcast = [
        {'Name': 'Brandon Nimmo', 'Hand': 'L', 'K_pct': 18.7, 'O_Swing': 26.0, 'Z_Contact': 85.0},
        {'Name': 'Andrew McCutchen', 'Hand': 'R', 'K_pct': 22.2, 'O_Swing': 24.0, 'Z_Contact': 80.0},
        {'Name': 'Corey Seager', 'Hand': 'L', 'K_pct': 21.2, 'O_Swing': 30.0, 'Z_Contact': 88.0},
        {'Name': 'Josh Jung', 'Hand': 'R', 'K_pct': 17.1, 'O_Swing': 28.0, 'Z_Contact': 85.0},
        {'Name': 'Jake Burger', 'Hand': 'R', 'K_pct': 28.6, 'O_Swing': 35.0, 'Z_Contact': 75.0},
        {'Name': 'Evan Carter', 'Hand': 'L', 'K_pct': 22.7, 'O_Swing': 22.0, 'Z_Contact': 82.0},
        {'Name': 'Ezequiel Duran', 'Hand': 'R', 'K_pct': 21.0, 'O_Swing': 32.0, 'Z_Contact': 80.0},
        {'Name': 'Josh Smith', 'Hand': 'L', 'K_pct': 18.6, 'O_Swing': 25.0, 'Z_Contact': 85.0},
        {'Name': 'Kyle Higashioka', 'Hand': 'R', 'K_pct': 22.2, 'O_Swing': 30.0, 'Z_Contact': 80.0},
    ]

    home_lineup_statcast = [
        {'Name': 'Kevin McGonigle', 'Hand': 'L', 'K_pct': 12.8, 'O_Swing': 18.0, 'Z_Contact': 90.0},
        {'Name': 'Matt Vierling', 'Hand': 'R', 'K_pct': 18.6, 'O_Swing': 30.0, 'Z_Contact': 85.0},
        {'Name': 'Colt Keith', 'Hand': 'L', 'K_pct': 22.2, 'O_Swing': 32.0, 'Z_Contact': 82.0},
        {'Name': 'Riley Greene', 'Hand': 'L', 'K_pct': 29.7, 'O_Swing': 28.0, 'Z_Contact': 78.0},
        {'Name': 'Spencer Torkelson', 'Hand': 'R', 'K_pct': 28.4, 'O_Swing': 32.0, 'Z_Contact': 75.0},
        {'Name': 'Kerry Carpenter', 'Hand': 'L', 'K_pct': 21.2, 'O_Swing': 25.0, 'Z_Contact': 82.0},
        {'Name': 'Wenceel Perez', 'Hand': 'S', 'K_pct': 21.8, 'O_Swing': 30.0, 'Z_Contact': 82.0},
        {'Name': 'Hao-Yu Lee', 'Hand': 'R', 'K_pct': 22.2, 'O_Swing': 30.0, 'Z_Contact': 80.0},
        {'Name': 'Jake Rogers', 'Hand': 'R', 'K_pct': 25.0, 'O_Swing': 32.0, 'Z_Contact': 78.0},
    ]

    game_data = {
        'away_team': 'TEX',
        'home_team': 'DET',
        'away_sp_name': 'Jack Leiter',
        'home_sp_name': 'Brant Hurter',
        'away_sp_hand': 'R',
        'home_sp_hand': 'L',
        'away_sp_era': 5.17,
        'home_sp_era': 1.84,
        'away_sp_statcast': {
            'Stuff': 104, 
            'K_pct': 23.9, 
            'VAA': -4.8, 
            'IP': 15.0, 
            'xERA': 4.50, 
            'BB_pct': 8.7
        },
        'home_sp_statcast': {
            'Stuff': 90, 
            'K_pct': 16.3, 
            'VAA': -6.0, 
            'IP': 22.0, 
            'xERA': 3.50, 
            'BB_pct': 7.0
        },
        'away_lineup_names': away_lineup_names,
        'away_lineup_hands': away_lineup_hands,
        'home_lineup_names': home_lineup_names,
        'home_lineup_hands': home_lineup_hands,
        'away_lineup_statcast': away_lineup_statcast,
        'home_lineup_statcast': home_lineup_statcast,
        'park_factor': 98,
        'is_dome': False,
        'env': {
            'Weather': {'temp': 57, 'wind_speed': 20, 'wind_dir': 90, 'humidity': 52},
            'altitude': 600,
            'rain_intensity': 0.01,
            'Umpire': {'name': 'Brennan Miller', 'zone_type': 'tight'}
        },
        'away_drs': 0,
        'home_drs': 5, # DET has elite defense
        'away_manager_hook': 0.5, # Aggressive
        'home_manager_hook': 0.0, # Neutral
        'away_bp_pitches_d1': 45, # Depleted
        'away_bp_pitches_d2': 30,
        'home_bp_pitches_d1': 10, # Stable
        'home_bp_pitches_d2': 15,
        'away_catcher': 'Kyle Higashioka',
        'home_catcher': 'Jake Rogers',
        'game_time': '19:20'
    }

    market_odds = {
        'DET Moneyline': -122,
        'TEX Moneyline': 105,
        'Total Over 8.5': -110,
        'Total Under 8.5': -110
    }

    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == "__main__":
    run_tex_det_sim()