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
import statistics
from datetime import datetime

# Add current directory to sys.path to find omni_prophet_v16

from omni_prophet_v16 import OmniProphetV18

def run_nyy_mil_sim():
    # NYY Lineup Data (May 10, 2026) - Confirmed Lineup
    # Based on USER prompt and MLB Stats
    away_lineup = [
        {'Name': 'T. Grisham', 'Hand': 'L', 'K_pct': 21.8, 'O_Swing': 22.0, 'Z_Contact': 88.0, 'wOBA': 0.307},  # .307 OBP lead-off specialist
        {'Name': 'Ben Rice', 'Hand': 'L', 'K_pct': 18.3, 'O_Swing': 25.0, 'Z_Contact': 85.0, 'wOBA': 0.440},    # 1.128 OPS, 12 HR - Elite
        {'Name': 'Aaron Judge', 'Hand': 'R', 'K_pct': 22.9, 'O_Swing': 20.0, 'Z_Contact': 82.0, 'wOBA': 0.415},  # .398 OBP
        {'Name': 'C. Bellinger', 'Hand': 'L', 'K_pct': 12.7, 'O_Swing': 28.0, 'Z_Contact': 90.0, 'wOBA': 0.352}, # .289 AVG
        {'Name': 'J. Chisholm', 'Hand': 'L', 'K_pct': 28.2, 'O_Swing': 32.0, 'Z_Contact': 80.0, 'wOBA': 0.284}, # .284 OBP
        {'Name': 'Ryan McMahon', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.270}, # .227 AVG
        {'Name': 'J. Caballero', 'Hand': 'R', 'K_pct': 27.8, 'O_Swing': 34.0, 'Z_Contact': 78.0, 'wOBA': 0.300},
        {'Name': 'Spencer Jones', 'Hand': 'L', 'K_pct': 32.0, 'O_Swing': 35.0, 'Z_Contact': 75.0, 'wOBA': 0.310}, # Power prospect
        {'Name': 'J.C. Escarra', 'Hand': 'L', 'K_pct': 24.0, 'O_Swing': 28.0, 'Z_Contact': 84.0, 'wOBA': 0.285},
    ]
    
    # MIL Lineup Data (May 10, 2026) - Confirmed Lineup
    home_lineup = [
        {'Name': 'Jackson Chourio', 'Hand': 'R', 'K_pct': 22.5, 'O_Swing': 33.0, 'Z_Contact': 83.0, 'wOBA': 0.380}, # .444 recent hot streak
        {'Name': 'Brice Turang', 'Hand': 'L', 'K_pct': 23.8, 'O_Swing': 26.0, 'Z_Contact': 87.0, 'wOBA': 0.360},    # wRC+ 146
        {'Name': 'W. Contreras', 'Hand': 'R', 'K_pct': 16.2, 'O_Swing': 29.0, 'Z_Contact': 85.0, 'wOBA': 0.350},   # wRC+ 129
        {'Name': 'Gary Sanchez', 'Hand': 'R', 'K_pct': 28.5, 'O_Swing': 35.0, 'Z_Contact': 76.0, 'wOBA': 0.320},   # Revenge narrative
        {'Name': 'Andrew Vaughn', 'Hand': 'R', 'K_pct': 21.0, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.310},
        {'Name': 'Luis Rengifo', 'Hand': 'S', 'K_pct': 20.3, 'O_Swing': 31.0, 'Z_Contact': 84.0, 'wOBA': 0.280},
        {'Name': 'G. Mitchell', 'Hand': 'L', 'K_pct': 28.0, 'O_Swing': 32.0, 'Z_Contact': 80.0, 'wOBA': 0.300},
        {'Name': 'Blake Perkins', 'Hand': 'S', 'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.290},
        {'Name': 'Joey Ortiz', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.315},
    ]

    game_data = {
        'away_team': 'NYY',
        'home_team': 'MIL',
        'away_sp_name': 'Carlos Rodon',
        'home_sp_name': 'Logan Henderson',
        'away_sp_hand': 'L',
        'home_sp_hand': 'R',
        'away_sp_era': 0.00,  # 2026: 0.00 ERA
        'home_sp_era': 4.50,  # 2026: 4.50 ERA
        'away_sp_statcast': {
            'Name': 'Carlos Rodon',
            'Hand': 'L',
            'Stuff': 106,       # Veteran, returns from MiLB. Stuff+ estimated solid.
            'K_pct': 27.1,      # Career rate
            'BB_pct': 8.0,
            'VAA': -4.5,
            'IP': 12.0,         # Estimated small sample for 2026
            'Starts': 2,
            'ERA': 0.00,
            'xERA': 3.50,
            'HR/FB%': 10.0,
            'LastPitchCount': 85  # Building back up
        },
        'home_sp_statcast': {
            'Name': 'Logan Henderson',
            'Hand': 'R',
            'Stuff': 104,       # Best changeup in org, 11 K in 8 IP.
            'K_pct': 31.0,      # 11 K in 8 IP
            'BB_pct': 4.0,      # 0.88 WHIP
            'VAA': -4.8,
            'IP': 8.0,          # Rookie sample
            'Starts': 2,
            'ERA': 4.50,
            'xERA': 3.10,       # Elite metrics despite ERA
            'HR/FB%': 15.0,
            'LastPitchCount': 80
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'away_lineup_k_pct': statistics.mean([b['K_pct'] for b in away_lineup]),
        'home_lineup_k_pct': statistics.mean([b['K_pct'] for b in home_lineup]),
        'park_factor': 105,     # American Family Field - HR friendly
        'is_dome': True,
        'away_drs': 5,          # Yankees good defense
        'home_drs': 3,          # Brewers good defense
        'away_manager_hook': 0,
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 20,
        'away_bp_pitches_d2': 15,
        'home_bp_pitches_d1': 10,
        'home_bp_pitches_d2': 10,
        'away_catcher': 'J.C. Escarra',
        'home_catcher': 'Gary Sanchez',
        'game_time_decimal': 14.17,
        'game_time': '14:10',
        'location': 'MIL',
        'away_bp_avg_era': 4.46,
        'home_bp_avg_era': 4.01,
        'env': {
            'Weather': {
                'temp': 72,           # Controlled dome
                'wind_speed': 0,
                'wind_dir': 0,
                'humidity': 50
            },
            'altitude': 600,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        }
    }

    market_odds = {
        'NYY Moneyline': 100,  # Brewers are slight favorites -120
        'MIL Moneyline': -120,
        'Total Over 8.0': -110,
        'Total Under 8.0': -110,
        'Carlos Rodon Over 5.5 K': -115,
        'Carlos Rodon Under 5.5 K': -105,
        'Logan Henderson Over 5.5 K': -110,
        'Logan Henderson Under 5.5 K': -110
    }

    omni = OmniProphetV18()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_nyy_mil_sim()