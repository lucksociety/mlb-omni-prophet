
import sys
import os

# Add the directory to sys.path to import the module
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV16

def run_simulation():
    omni = OmniProphetV16()
    
    # Corrected game_data structure for V16.0 engine
    game_data = {
        'away_team': 'ATL',
        'home_team': 'SEA',
        'game_time': '21:40',
        'is_dome': True,
        'park_factor': 94,
        'away_sp_name': 'JR Ritchie',
        'away_sp_hand': 'R',
        'away_sp_era': 2.92,
        'away_sp_statcast': {
            'Stuff': 108,
            'VAA': -4.2,
            'K_pct': 21.6,
            'BB_pct': 11.8,
            'IP': 12.1,
            'xERA': 4.63,
            'L3_CSW': 25.8,
            'L3_SwStr': 8.1,
            'Velo_Trend': 'Stable'
        },
        'home_sp_name': 'Logan Gilbert',
        'home_sp_hand': 'R',
        'home_sp_era': 4.03,
        'home_sp_statcast': {
            'Stuff': 112,
            'VAA': -4.5,
            'K_pct': 24.4,
            'BB_pct': 5.0,
            'IP': 38.0,
            'xERA': 3.85,
            'L3_CSW': 27.8,
            'L3_SwStr': 11.7,
            'Velo_Trend': 'Stable'
        },
        'away_lineup_names': ['D. Baldwin', 'Ozzie Albies', 'Matt Olson', 'M. Dubon', 'Austin Riley', 'M. Yastrzemski', 'Sean Murphy', 'Eli White', 'Jorge Mateo'],
        'away_lineup_hands': ['L', 'S', 'L', 'R', 'R', 'L', 'R', 'R', 'R'],
        'away_lineup_statcast': [
            {'K_pct': 24.5, 'O_Swing': 32.1, 'Z_Contact': 84.5},
            {'K_pct': 18.2, 'O_Swing': 38.4, 'Z_Contact': 88.1},
            {'K_pct': 25.4, 'O_Swing': 28.5, 'Z_Contact': 78.4},
            {'K_pct': 14.2, 'O_Swing': 35.1, 'Z_Contact': 92.4},
            {'K_pct': 22.8, 'O_Swing': 33.4, 'Z_Contact': 81.2},
            {'K_pct': 26.5, 'O_Swing': 24.2, 'Z_Contact': 82.1},
            {'K_pct': 23.1, 'O_Swing': 26.4, 'Z_Contact': 80.5},
            {'K_pct': 31.4, 'O_Swing': 34.5, 'Z_Contact': 74.2},
            {'K_pct': 29.8, 'O_Swing': 36.2, 'Z_Contact': 72.8}
        ],
        'home_lineup_names': ['J. Crawford', 'J. Rodriguez', 'Josh Naylor', 'R. Arozarena', 'D. Canzone', 'Luke Raley', 'Cole Young', 'Mitch Garver', 'Leo Rivas'],
        'home_lineup_hands': ['L', 'R', 'L', 'R', 'L', 'L', 'L', 'R', 'S'],
        'home_lineup_statcast': [
            {'K_pct': 19.5, 'O_Swing': 22.4, 'Z_Contact': 88.4},
            {'K_pct': 26.2, 'O_Swing': 34.2, 'Z_Contact': 81.5},
            {'K_pct': 16.4, 'O_Swing': 30.1, 'Z_Contact': 89.2},
            {'K_pct': 24.1, 'O_Swing': 31.2, 'Z_Contact': 80.4},
            {'K_pct': 22.8, 'O_Swing': 32.4, 'Z_Contact': 82.1},
            {'K_pct': 28.5, 'O_Swing': 34.1, 'Z_Contact': 76.2},
            {'K_pct': 21.4, 'O_Swing': 24.5, 'Z_Contact': 86.4},
            {'K_pct': 27.2, 'O_Swing': 25.1, 'Z_Contact': 78.1},
            {'K_pct': 23.4, 'O_Swing': 26.2, 'Z_Contact': 84.1}
        ],
        'env': {
            'Weather': {
                'temp': 76,
                'wind_speed': 3.4,
                'wind_dir': 0,
                'humidity': 44
            },
            'altitude': 10,
            'rain_intensity': 0.0,
            'Umpire': {
                'name': 'Neutral/Clint Vondrak',
                'CS_pct': 16.5,
                'zone_type': 'neutral'
            }
        },
        'away_catcher': 'Sean Murphy',
        'home_catcher': 'Mitch Garver',
        'away_drs': 8,
        'home_drs': 2,
        'away_manager_hook': 0.0,
        'home_manager_hook': -0.3,
        'away_bp_pitches_d1': 45,
        'away_bp_pitches_d2': 30,
        'home_bp_pitches_d1': 35,
        'home_bp_pitches_d2': 50,
        'market_odds': {
            'Total Over 8.0': -110,
            'SEA ML': -143,
            'ATL ML': 120
        }
    }
    
    # Run the simulation
    omni.run_omni_simulation(game_data, market_odds=game_data['market_odds'])

if __name__ == "__main__":
    run_simulation()
