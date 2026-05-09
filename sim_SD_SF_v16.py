
import sys
import os

# Add the directory to sys.path to import the module
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV16

def run_simulation():
    omni = OmniProphetV16()
    
    # Research Data for SD @ SF (2026-05-04)
    game_data = {
        'away_team': 'SD',
        'home_team': 'SF',
        'game_time': '21:45',
        'is_dome': False,
        'park_factor': 96, # Oracle Park
        'away_sp_name': 'Randy Vasquez',
        'away_sp_hand': 'R',
        'away_sp_era': 2.94,
        'away_sp_statcast': {
            'Stuff': 105,
            'VAA': -4.2,
            'K_pct': 24.8,
            'BB_pct': 8.0,
            'IP': 33.2,
            'xERA': 3.43,
            'L3_CSW': 27.9,
            'L3_SwStr': 13.1,
            'Velo_Trend': 'Gaining' # 93.7 -> 94.8
        },
        'home_sp_name': 'Trevor McDonald',
        'home_sp_hand': 'R',
        'home_sp_era': 0.00, # Per Screenshot
        'home_sp_statcast': {
            'Stuff': 116,
            'VAA': -4.5,
            'K_pct': 21.0, # Est from AAA 12K in 15IP
            'BB_pct': 11.0, # Est from AAA 15BB in 15IP
            'IP': 3.0,
            'xERA': 3.80,
            'L3_CSW': 24.5,
            'L3_SwStr': 9.2,
            'Velo_Trend': 'Gaining',
            'PitchLimit': 50,
            'ShortLeash': True
        },
        'away_lineup_names': ['R. Laureano', 'F. Tatis', 'J. Merrill', 'M. Machado', 'X. Bogaerts', 'Gavin Sheets', 'M. Andujar', 'F. Fermin', 'J. Cronenworth'],
        'away_lineup_hands': ['R', 'R', 'L', 'R', 'R', 'L', 'R', 'R', 'L'],
        'away_lineup_statcast': [
            {'K_pct': 22.6, 'O_Swing': 32.5, 'Z_Contact': 81.2},
            {'K_pct': 20.8, 'O_Swing': 28.1, 'Z_Contact': 84.5},
            {'K_pct': 22.8, 'O_Swing': 33.2, 'Z_Contact': 79.8},
            {'K_pct': 22.2, 'O_Swing': 34.5, 'Z_Contact': 80.1},
            {'K_pct': 21.1, 'O_Swing': 29.4, 'Z_Contact': 83.2},
            {'K_pct': 19.3, 'O_Swing': 26.8, 'Z_Contact': 86.4},
            {'K_pct': 17.1, 'O_Swing': 35.2, 'Z_Contact': 89.1},
            {'K_pct': 18.8, 'O_Swing': 30.5, 'Z_Contact': 85.6},
            {'K_pct': 21.1, 'O_Swing': 27.4, 'Z_Contact': 84.8}
        ],
        'home_lineup_names': ['Jung Hoo Lee', 'C. Schmitt', 'Luis Arraez', 'Heliot Ramos', 'R. Devers', 'Willy Adames', 'B. Eldridge', 'J. Rodriguez', 'Drew Gilbert'],
        'home_lineup_hands': ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'L'],
        'home_lineup_statcast': [
            {'K_pct': 13.1, 'O_Swing': 22.4, 'Z_Contact': 91.2},
            {'K_pct': 21.6, 'O_Swing': 33.4, 'Z_Contact': 82.1},
            {'K_pct': 4.2,  'O_Swing': 21.5, 'Z_Contact': 94.8},
            {'K_pct': 23.7, 'O_Swing': 35.1, 'Z_Contact': 79.4},
            {'K_pct': 28.5, 'O_Swing': 30.2, 'Z_Contact': 76.5},
            {'K_pct': 26.0, 'O_Swing': 31.8, 'Z_Contact': 78.2},
            {'K_pct': 27.5, 'O_Swing': 36.4, 'Z_Contact': 74.1},
            {'K_pct': 23.0, 'O_Swing': 32.1, 'Z_Contact': 80.5},
            {'K_pct': 21.6, 'O_Swing': 28.4, 'Z_Contact': 82.8}
        ],
        'env': {
            'Weather': {
                'temp': 60,
                'wind_speed': 10.0,
                'wind_dir': 0, # Out
                'humidity': 65
            },
            'altitude': 0,
            'rain_intensity': 0.0,
            'Umpire': {
                'name': 'Neutral Assignment',
                'CS_pct': 16.5,
                'zone_type': 'neutral'
            }
        },
        'away_catcher': 'F. Fermin',
        'home_catcher': 'J. Rodriguez',
        'away_drs': 4, # Padres defensive rank
        'home_drs': -2, # Giants defensive rank
        'away_manager_hook': 0.0,
        'home_manager_hook': 0.0,
        'away_bp_pitches_d1': 30,
        'away_bp_pitches_d2': 20,
        'home_bp_pitches_d1': 40,
        'home_bp_pitches_d2': 35,
        'market_odds': {
            'Total Over 8.0': -110,
            'SD ML': -130,
            'SF ML': 110
        }
    }
    
    # Run the simulation
    omni.run_omni_simulation(game_data, market_odds=game_data['market_odds'])

if __name__ == "__main__":
    run_simulation()
