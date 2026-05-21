
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

# Setup path for imports

from omni_prophet_v16 import OmniProphetV18

def run_nym_ari_ev_analysis():
    # Final Lineups from User Prompt
    away_lineup = [
        {'Name': 'Juan Soto', 'Hand': 'L', 'K_pct': 18.5, 'O_Swing': 22.0, 'Z_Contact': 85.0, 'wOBA': 0.346},
        {'Name': 'Bo Bichette', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 35.0, 'Z_Contact': 84.0, 'wOBA': 0.226},
        {'Name': 'A. Slater', 'Hand': 'R', 'K_pct': 24.0, 'O_Swing': 28.0, 'Z_Contact': 82.0, 'wOBA': 0.320},
        {'Name': 'Mark Vientos', 'Hand': 'R', 'K_pct': 26.0, 'O_Swing': 32.0, 'Z_Contact': 78.0, 'wOBA': 0.330},
        {'Name': 'Marcus Semien', 'Hand': 'R', 'K_pct': 16.0, 'O_Swing': 25.0, 'Z_Contact': 88.0, 'wOBA': 0.230},
        {'Name': 'Andy Ibanez', 'Hand': 'R', 'K_pct': 21.0, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'wOBA': 0.310},
        {'Name': 'T. Taylor', 'Hand': 'R', 'K_pct': 23.0, 'O_Swing': 32.0, 'Z_Contact': 80.0, 'wOBA': 0.290},
        {'Name': 'Carson Benge', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 80.0, 'wOBA': 0.280},
        {'Name': 'Luis Torrens', 'Hand': 'R', 'K_pct': 24.0, 'O_Swing': 31.0, 'Z_Contact': 82.0, 'wOBA': 0.270},
    ]
    
    home_lineup = [
        {'Name': 'Ketel Marte', 'Hand': 'S', 'K_pct': 18.0, 'O_Swing': 28.0, 'Z_Contact': 86.0, 'wOBA': 0.330},
        {'Name': 'Corbin Carroll', 'Hand': 'L', 'K_pct': 20.0, 'O_Swing': 26.0, 'Z_Contact': 84.0, 'wOBA': 0.340},
        {'Name': 'G. Perdomo', 'Hand': 'S', 'K_pct': 16.0, 'O_Swing': 24.0, 'Z_Contact': 90.0, 'wOBA': 0.310},
        {'Name': 'A. Del Castillo', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.320},
        {'Name': 'I. Vargas', 'Hand': 'S', 'K_pct': 18.0, 'O_Swing': 25.0, 'Z_Contact': 88.0, 'wOBA': 0.300},
        {'Name': 'Nolan Arenado', 'Hand': 'R', 'K_pct': 15.0, 'O_Swing': 28.0, 'Z_Contact': 87.0, 'wOBA': 0.335},
        {'Name': 'James McCann', 'Hand': 'R', 'K_pct': 25.0, 'O_Swing': 34.0, 'Z_Contact': 80.0, 'wOBA': 0.260},
        {'Name': 'J. Barrosa', 'Hand': 'S', 'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.290},
        {'Name': 'R. Waldschmidt', 'Hand': 'R', 'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 80.0, 'wOBA': 0.280},
    ]

    game_data = {
        'away_team': 'NYM', 'home_team': 'ARI',
        'away_sp_name': 'David Peterson', 'home_sp_name': 'Eduardo Rodriguez',
        'away_sp_hand': 'L', 'home_sp_hand': 'L',
        'away_sp_era': 6.29, 'home_sp_era': 2.50,
        'away_sp_statcast': {
            'Name': 'David Peterson', 'Hand': 'L', 'Stuff': 94, 'K_pct': 21.0, 'BB_pct': 10.5, 'VAA': -4.3,
            'IP': 28.2, 'Starts': 6, 'ERA': 6.29, 'xERA': 5.45, 'LastPitchCount': 85
        },
        'home_sp_statcast': {
            'Name': 'Eduardo Rodriguez', 'Hand': 'L', 'Stuff': 102, 'K_pct': 23.5, 'BB_pct': 6.5, 'VAA': -4.5,
            'IP': 39.2, 'Starts': 6, 'ERA': 2.50, 'xERA': 3.15, 'WHIP': 1.29, 'LastPitchCount': 102
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_statcast': home_lineup,
        'park_factor': 100, 'is_dome': True,
        'away_drs': -2, 'home_drs': 3,
        'away_manager_hook': 1, 'home_manager_hook': 0,
        'away_bp_pitches_d1': 25, 'away_bp_pitches_d2': 15,
        'home_bp_pitches_d1': 20, 'home_bp_pitches_d2': 25,
        'away_catcher': 'Luis Torrens', 'home_catcher': 'James McCann',
        'game_time': '16:10', 'location': 'ARI',
        'away_bp_avg_era': 4.50, 'home_bp_avg_era': 4.20,
        'env': {
            'Weather': {'temp': 72, 'wind_speed': 0, 'wind_dir': 0, 'humidity': 50},
            'altitude': 1082, 'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        }
    }

    market_odds = {
        # Core Markets
        'ARI ML': -116,
        'NYM ML': -104,
        'Total Over 8.5': -120,
        'Total Under 8.5': 100, # EVEN
        'NYM Runline +1.5': -210,
        'ARI Runline -1.5': 175,
        
        # Alternate Totals
        'Total Over 7.5': -170,
        'Total Over 8.0': -150,
        'Total Over 9.0': 100, # EVEN
        'Total Over 9.5': 125,
        'Total Over 10.0': 150,
        
        # Team Totals
        'ARI Team Total Over 4.5': 110,
        'NYM Team Total Over 4.5': 110,
        
        # Prop Markets
        'E. Rodriguez Over 4.5 K': 125,
        'E. Rodriguez Under 4.5 K': -165,
        'David Peterson Under 4.5 K': -110,
        'Yes Run in 1st Inning': -120,
        'No Run in 1st Inning': -110
    }

    omni = OmniProphetV18()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_nym_ari_ev_analysis()