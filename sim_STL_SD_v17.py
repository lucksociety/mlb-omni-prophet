import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from omni_prophet_v16 import OmniProphetV17

def run_stl_sd_sim():
    # Final Lineup Data for STL @ SD (May 7, 2026)
    # Using a blend of Statcast and User-provided "Rookie Sensation" Intel
    away_lineup = [
        {'Name': 'JJ Wetherholt', 'Hand': 'L', 'K_pct': 18.0, 'O_Swing': 24.4, 'Z_Contact': 88.0, 'wRC_plus': 140}, # User: .423 OBP
        {'Name': 'Ivan Herrera', 'Hand': 'R', 'K_pct': 14.8, 'O_Swing': 24.7, 'Z_Contact': 86.0, 'wRC_plus': 130},
        {'Name': 'A. Burleson', 'Hand': 'L', 'K_pct': 12.5, 'O_Swing': 27.0, 'Z_Contact': 90.0, 'wRC_plus': 115}, # Adjusted for L/R
        {'Name': 'Jordan Walker', 'Hand': 'R', 'K_pct': 32.2, 'O_Swing': 35.1, 'Z_Contact': 78.0, 'wRC_plus': 153}, # Finding groove
        {'Name': 'Nolan Gorman', 'Hand': 'L', 'K_pct': 28.2, 'O_Swing': 27.9, 'Z_Contact': 75.0, 'wRC_plus': 85},
        {'Name': 'Masyn Winn', 'Hand': 'R', 'K_pct': 21.2, 'O_Swing': 31.8, 'Z_Contact': 85.0, 'wRC_plus': 102},
        {'Name': 'N. Church', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 25.0, 'Z_Contact': 82.0, 'wRC_plus': 121},
        {'Name': 'Pedro Pages', 'Hand': 'R', 'K_pct': 26.9, 'O_Swing': 26.9, 'Z_Contact': 80.0, 'wRC_plus': 77},
        {'Name': 'Victor Scott II', 'Hand': 'L', 'K_pct': 12.5, 'O_Swing': 12.5, 'Z_Contact': 92.0, 'wRC_plus': 120} # Speed factor
    ]
    
    home_lineup = [
        {'Name': 'R. Laureano', 'Hand': 'R', 'K_pct': 27.8, 'O_Swing': 32.4, 'Z_Contact': 82.0, 'wRC_plus': 117},
        {'Name': 'F. Tatis Jr.', 'Hand': 'R', 'K_pct': 24.4, 'O_Swing': 34.6, 'Z_Contact': 80.0, 'wRC_plus': 140}, # Crushes LHP
        {'Name': 'Jackson Merrill', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 26.7, 'Z_Contact': 85.0, 'wRC_plus': 115}, # Surge real
        {'Name': 'Manny Machado', 'Hand': 'R', 'K_pct': 19.3, 'O_Swing': 25.4, 'Z_Contact': 88.0, 'wRC_plus': 130}, # Threat vs LHP
        {'Name': 'X. Bogaerts', 'Hand': 'R', 'K_pct': 21.0, 'O_Swing': 29.8, 'Z_Contact': 87.0, 'wRC_plus': 115}, # Threat vs LHP
        {'Name': 'Gavin Sheets', 'Hand': 'L', 'K_pct': 21.6, 'O_Swing': 26.7, 'Z_Contact': 82.0, 'wRC_plus': 102},
        {'Name': 'M. Andujar', 'Hand': 'R', 'K_pct': 24.1, 'O_Swing': 24.1, 'Z_Contact': 80.0, 'wRC_plus': 75},
        {'Name': 'L. Campusano', 'Hand': 'R', 'K_pct': 21.9, 'O_Swing': 29.8, 'Z_Contact': 85.0, 'wRC_plus': 94},
        {'Name': 'S. Song', 'Hand': 'L', 'K_pct': 20.0, 'O_Swing': 20.0, 'Z_Contact': 90.0, 'wRC_plus': 110} # .333 surge
    ]

    game_data = {
        'away_team': 'STL',
        'home_team': 'SD',
        'away_sp_name': 'Matthew Liberatore',
        'home_sp_name': 'Michael King',
        'away_sp_hand': 'L',
        'home_sp_hand': 'R',
        'away_sp_era': 4.50,
        'home_sp_era': 2.95,
        'away_sp_statcast': {
            'Name': 'Matthew Liberatore',
            'Hand': 'L',
            'Stuff': 95,
            'K_pct': 14.1,
            'BB_pct': 8.1,
            'VAA': -4.5,
            'IP': 36,
            'xERA': 5.01,
            'HardHit_pct': 44.3
        },
        'home_sp_statcast': {
            'Name': 'Michael King',
            'Hand': 'R',
            'Stuff': 107,
            'K_pct': 25.4,
            'BB_pct': 11.2,
            'VAA': -4.7,
            'IP': 39.2,
            'xERA': 4.26
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'park_factor': 95, # Petco Park
        'is_dome': False,
        'away_drs': 0,
        'home_drs': 5,
        'away_manager_hook': 0,
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 0,
        'away_bp_pitches_d2': 0,
        'home_bp_pitches_d1': 0,
        'home_bp_pitches_d2': 0,
        'away_catcher': 'Pedro Pages',
        'home_catcher': 'L. Campusano',
        'game_time': "22:10", # 10:10 PM ET
        'env': {
            'Weather': {
                'temp': 66, 
                'wind_speed': 7, 
                'wind_dir': 45, # Blowing out to San Diego Bay
                'humidity': 60
            },
            'altitude': 15,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        }
    }

    market_odds = {
        'SD Moneyline': -162,
        'STL Moneyline': 136,
        'Total Over 8.0': -110,
        'Total Under 8.0': -110,
        'Matthew Liberatore Over 3.5 K': -145,
        'Matthew Liberatore Under 3.5 K': 110,
        'Michael King Over 5.5 K': -125,
        'Michael King Under 5.5 K': -105,
        'YRFI': 105,
        'NRFI': -135
    }

    # Clear canonical run for the update
    omni = OmniProphetV17()
    omni.clear_canonical(f"STL_SD_{datetime.now().strftime('%Y-%m-%d')}")
    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_stl_sd_sim()
