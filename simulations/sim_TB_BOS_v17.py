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

from omni_prophet_v16 import OmniProphetV17

def run_tb_bos_sim():
    # Final Lineup Data for TB @ BOS (May 7, 2026)
    # Stats from MLB Stats file (line 13, 29, etc.) and forensic estimates
    away_lineup = [
        {'Name': 'Yandy Diaz', 'Hand': 'R', 'K_pct': 13.8, 'O_Swing': 22.5, 'Z_Contact': 90.5, 'wRC_plus': 150},
        {'Name': 'Ryan Vilade', 'Hand': 'R', 'K_pct': 21.0, 'O_Swing': 31.0, 'Z_Contact': 85.0, 'wRC_plus': 95},
        {'Name': 'Junior Caminero', 'Hand': 'R', 'K_pct': 19.2, 'O_Swing': 34.2, 'Z_Contact': 82.0, 'wRC_plus': 133},
        {'Name': 'Jonathan Aranda', 'Hand': 'L', 'K_pct': 24.5, 'O_Swing': 29.8, 'Z_Contact': 84.1, 'wRC_plus': 102},
        {'Name': 'Jonny DeLuca', 'Hand': 'R', 'K_pct': 20.8, 'O_Swing': 30.5, 'Z_Contact': 86.2, 'wRC_plus': 100},
        {'Name': 'Ben Williamson', 'Hand': 'R', 'K_pct': 23.2, 'O_Swing': 32.1, 'Z_Contact': 83.4, 'wRC_plus': 90},
        {'Name': 'Nick Fortes', 'Hand': 'R', 'K_pct': 17.5, 'O_Swing': 36.4, 'Z_Contact': 89.8, 'wRC_plus': 85},
        {'Name': 'Cedric Mullins', 'Hand': 'L', 'K_pct': 20.1, 'O_Swing': 28.5, 'Z_Contact': 85.6, 'wRC_plus': 100},
        {'Name': 'Taylor Walls', 'Hand': 'S', 'K_pct': 22.4, 'O_Swing': 21.8, 'Z_Contact': 87.2, 'wRC_plus': 80}
    ]
    
    home_lineup = [
        {'Name': 'Jarren Duran', 'Hand': 'L', 'K_pct': 25.6, 'O_Swing': 33.4, 'Z_Contact': 81.2, 'wRC_plus': 112},
        {'Name': 'Willson Contreras', 'Hand': 'R', 'K_pct': 27.5, 'O_Swing': 28.5, 'Z_Contact': 84.6, 'wRC_plus': 139},
        {'Name': 'Wilyer Abreu', 'Hand': 'L', 'K_pct': 25.4, 'O_Swing': 30.2, 'Z_Contact': 83.5, 'wRC_plus': 110},
        {'Name': 'Trevor Story', 'Hand': 'R', 'K_pct': 26.4, 'O_Swing': 35.1, 'Z_Contact': 78.4, 'wRC_plus': 105},
        {'Name': 'Masataka Yoshida', 'Hand': 'L', 'K_pct': 14.2, 'O_Swing': 24.8, 'Z_Contact': 91.5, 'wRC_plus': 115},
        {'Name': 'Ceddanne Rafaela', 'Hand': 'R', 'K_pct': 20.1, 'O_Swing': 38.6, 'Z_Contact': 82.3, 'wRC_plus': 93},
        {'Name': 'Marcelo Mayer', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 27.5, 'Z_Contact': 85.0, 'wRC_plus': 100},
        {'Name': 'Connor Wong', 'Hand': 'R', 'K_pct': 24.1, 'O_Swing': 36.2, 'Z_Contact': 81.8, 'wRC_plus': 105},
        {'Name': 'Caleb Durbin', 'Hand': 'R', 'K_pct': 11.0, 'O_Swing': 22.4, 'Z_Contact': 92.5, 'wRC_plus': 97}
    ]

    game_data = {
        'away_team': 'TBR',
        'home_team': 'BOS',
        'away_sp_name': 'Jesse Scholtens',
        'home_sp_name': 'Jake Bennett',
        'away_sp_hand': 'R',
        'home_sp_hand': 'L',
        'away_sp_era': 3.18,
        'home_sp_era': 1.80,
        'away_sp_statcast': {
            'Name': 'Jesse Scholtens',
            'Hand': 'R',
            'Stuff': 95,
            'K_pct': 21.8,
            'BB_pct': 7.2,
            'VAA': -4.4,
            'IP': 22.2,
            'xERA': 3.65,
            'LastPitchCount': 88
        },
        'home_sp_statcast': {
            'Name': 'Jake Bennett',
            'Hand': 'L',
            'Stuff': 112,
            'K_pct': 28.4,
            'BB_pct': 10.2,
            'VAA': -4.8,
            'IP': 15,
            'xERA': 2.15,
            'LastPitchCount': 92
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'park_factor': 105, # Fenway
        'is_dome': False,
        'away_drs': 4, # TB generally good defense
        'home_drs': -2, # BOS sometimes shaky
        'away_manager_hook': 0,
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 15,
        'away_bp_pitches_d2': 0,
        'home_bp_pitches_d1': 45, # Red Sox bullpen heavily used lately?
        'home_bp_pitches_d2': 20,
        'away_catcher': 'Nick Fortes',
        'home_catcher': 'Connor Wong',
        'game_time': 19.16, # 7:10 PM ET
        'env': {
            'Weather': {
                'temp': 60, 
                'wind_speed': 11, 
                'wind_dir': 45, # Blowing L-to-R (towards Monster)
                'humidity': 55
            },
            'altitude': 20,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Pat Hoberg', 'zone_type': 'neutral'} # Neutral/Good zone
        }
    }

    market_odds = {
        'TBR Moneyline': -102,
        'BOS Moneyline': -118,
        'Total Under 8.5': -110,
        'NRFI (No Run 1st Inning)': -125,
        'Jake Bennett Over 3.5 K': 130,
        'Griffin Jax Over 3.5 K': -125
    }

    omni = OmniProphetV17()
    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_tb_bos_sim()