import sys
import os

# Add the path to the workspace
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV16

def run_simulation():
    omni = OmniProphetV16()
    
    game_data = {
        'away_team': 'BOS',
        'home_team': 'DET',
        'away_sp_name': 'Payton Tolle',
        'home_sp_name': 'Ty Madden',
        'away_sp_hand': 'L',
        'home_sp_hand': 'R',
        'away_sp_era': 3.38,
        'home_sp_era': 3.99, # Using FIP/xERA floor for Madden since 0.00 is too low
        'park_factor': 100,
        'is_dome': False,
        
        'away_sp_statcast': {
            'Stuff': 115,
            'K_pct': 34.8,
            'VAA': -3.9,
            'IP': 10.2,
            'xERA': 2.80,
            'CSW': 39.8,
            'SwStr': 19.4,
            'BB_pct': 9.3
        },
        'home_sp_statcast': {
            'Stuff': 105,
            'K_pct': 16.8,
            'VAA': -4.5,
            'IP': 21.0,
            'xERA': 3.99,
            'CSW': 28.0,
            'SwStr': 11.0,
            'BB_pct': 7.9
        },
        
        'away_lineup_names': ['Jarren Duran', 'Willson Contreras', 'Roman Anthony', 'Trevor Story', 'Wilyer Abreu', 'Ceddanne Rafaela', 'Marcelo Mayer', 'Carlos Narvaez', 'Andruw Monasterio'],
        'away_lineup_hands': ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'R'],
        'away_lineup_statcast': [
            {'K_pct': 22.1, 'O_Swing': 28.4, 'Z_Contact': 85.2},
            {'K_pct': 24.5, 'O_Swing': 29.1, 'Z_Contact': 82.3},
            {'K_pct': 26.8, 'O_Swing': 27.5, 'Z_Contact': 80.1},
            {'K_pct': 29.4, 'O_Swing': 31.2, 'Z_Contact': 78.5},
            {'K_pct': 27.2, 'O_Swing': 26.9, 'Z_Contact': 81.4},
            {'K_pct': 28.5, 'O_Swing': 35.1, 'Z_Contact': 79.2},
            {'K_pct': 25.1, 'O_Swing': 28.0, 'Z_Contact': 82.0},
            {'K_pct': 23.4, 'O_Swing': 25.5, 'Z_Contact': 84.1},
            {'K_pct': 21.0, 'O_Swing': 24.0, 'Z_Contact': 86.5},
        ],
        
        'home_lineup_names': ['Jahmai Jones', 'Matt Vierling', 'Dillon Dingler', 'Riley Greene', 'Spencer Torkelson', 'Wenceel Perez', 'Hao-Yu Lee', 'Colt Keith', 'Zack Short'],
        'home_lineup_hands': ['R', 'R', 'R', 'L', 'R', 'S', 'R', 'L', 'R'],
        'home_lineup_statcast': [
            {'K_pct': 25.6, 'O_Swing': 28.0, 'Z_Contact': 82.5},
            {'K_pct': 20.2, 'O_Swing': 30.5, 'Z_Contact': 86.1},
            {'K_pct': 28.4, 'O_Swing': 33.2, 'Z_Contact': 77.8},
            {'K_pct': 24.1, 'O_Swing': 27.2, 'Z_Contact': 83.4},
            {'K_pct': 23.8, 'O_Swing': 29.5, 'Z_Contact': 81.9},
            {'K_pct': 21.5, 'O_Swing': 26.1, 'Z_Contact': 85.0},
            {'K_pct': 24.0, 'O_Swing': 28.5, 'Z_Contact': 82.2},
            {'K_pct': 22.8, 'O_Swing': 29.0, 'Z_Contact': 84.5},
            {'K_pct': 27.5, 'O_Swing': 32.1, 'Z_Contact': 79.8},
        ],
        
        'env': {
            'Weather': {
                'temp': 69,
                'wind_speed': 18,
                'wind_dir': 45, # Adjusting to degrees from CF: 0=out, 180=in. 45 is blowing out toward RF.
                'humidity': 55
            },
            'altitude': 602,
            'rain_intensity': 0.04,
            'Umpire': {
                'name': 'Dan Iassogna',
                'CS_pct': 16.2,
                'zone_type': 'neutral'
            }
        },
        
        'away_catcher': 'Carlos Narvaez',
        'home_catcher': 'Dillon Dingler',
        'away_drs': 12,
        'home_drs': -5,
        'away_manager_hook': 0.0,
        'home_manager_hook': -0.3,
        'away_bp_pitches_d1': 45,
        'away_bp_pitches_d2': 30,
        'home_bp_pitches_d1': 85,
        'home_bp_pitches_d2': 12,
        'game_time': '18:10'
    }
    
    market_odds = {
        'Away Moneyline': -118,
        'Total Over 8.0': -110
    }
    
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
    print(results)

if __name__ == "__main__":
    run_simulation()
