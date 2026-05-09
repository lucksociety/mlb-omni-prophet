import sys
import os

# Add the workspace to sys.path to import OmniProphet
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV16

def run_simulation():
    omni = OmniProphetV16()
    
    # Research Data
    away_lineup = [
        {'name': 'G. Mitchell', 'hand': 'L', 'K_pct': 31.0, 'O_Swing': 32.0, 'Z_Contact': 78.0},
        {'name': 'J. Chourio', 'hand': 'R', 'K_pct': 24.0, 'O_Swing': 35.0, 'Z_Contact': 82.0},
        {'name': 'Brice Turang', 'hand': 'L', 'K_pct': 19.0, 'O_Swing': 28.0, 'Z_Contact': 88.0},
        {'name': 'W. Contreras', 'hand': 'R', 'K_pct': 12.0, 'O_Swing': 24.0, 'Z_Contact': 92.0},
        {'name': 'Jake Bauers', 'hand': 'L', 'K_pct': 28.0, 'O_Swing': 30.0, 'Z_Contact': 75.0},
        {'name': 'Andrew Vaughn', 'hand': 'R', 'K_pct': 18.0, 'O_Swing': 29.0, 'Z_Contact': 85.0},
        {'name': 'Sal Frelick', 'hand': 'L', 'K_pct': 15.0, 'O_Swing': 26.0, 'Z_Contact': 90.0},
        {'name': 'Luis Rengifo', 'hand': 'S', 'K_pct': 17.0, 'O_Swing': 31.0, 'Z_Contact': 84.0},
        {'name': 'David Hamilton', 'hand': 'L', 'K_pct': 20.0, 'O_Swing': 33.0, 'Z_Contact': 80.0},
    ]
    
    home_lineup = [
        {'name': 'JJ Wetherholt', 'hand': 'L', 'K_pct': 16.0, 'O_Swing': 22.0, 'Z_Contact': 91.0},
        {'name': 'Ivan Herrera', 'hand': 'R', 'K_pct': 17.0, 'O_Swing': 24.0, 'Z_Contact': 89.0},
        {'name': 'A. Burleson', 'hand': 'L', 'K_pct': 14.0, 'O_Swing': 25.0, 'Z_Contact': 90.0},
        {'name': 'Jordan Walker', 'hand': 'R', 'K_pct': 22.0, 'O_Swing': 33.0, 'Z_Contact': 81.0},
        {'name': 'Nolan Gorman', 'hand': 'L', 'K_pct': 32.0, 'O_Swing': 36.0, 'Z_Contact': 72.0},
        {'name': 'Masyn Winn', 'hand': 'R', 'K_pct': 16.0, 'O_Swing': 27.0, 'Z_Contact': 87.0},
        {'name': 'N. Church', 'hand': 'L', 'K_pct': 21.0, 'O_Swing': 29.0, 'Z_Contact': 83.0},
        {'name': 'Pedro Pages', 'hand': 'R', 'K_pct': 23.0, 'O_Swing': 31.0, 'Z_Contact': 79.0},
        {'name': 'Victor Scott', 'hand': 'L', 'K_pct': 22.0, 'O_Swing': 34.0, 'Z_Contact': 76.0},
    ]

    game_data = {
        'away_team': 'MIL',
        'home_team': 'STL',
        'away_sp_name': 'Chad Patrick',
        'home_sp_name': 'Kyle Leahy',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': 2.57,
        'home_sp_era': 5.52,
        'away_lineup_names': [b['name'] for b in away_lineup],
        'away_lineup_hands': [b['hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['name'] for b in home_lineup],
        'home_lineup_hands': [b['hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'away_sp_statcast': {
            'Stuff': 105,
            'VAA': -4.8,
            'K_pct': 14.1,
            'BB_pct': 4.2,
            'IP': 28.0,
            'xERA': 3.82,
            'L3_CSW': 25.8,
            'L3_SwStr': 8.1,
            'Velo_Trend': 'Stable'
        },
        'home_sp_statcast': {
            'Stuff': 98,
            'VAA': -4.5,
            'K_pct': 16.9,
            'BB_pct': 8.5,
            'IP': 29.1,
            'xERA': 4.48,
            'L3_CSW': 28.0,
            'L3_SwStr': 7.7,
            'Velo_Trend': 'Stable'
        },
        'env': {
            'Weather': {
                'temp': 79,
                'wind_speed': 14,
                'wind_dir': 0,
                'humidity': 55
            },
            'altitude': 436,
            'rain_intensity': 0.24,
            'Umpire': {
                'name': 'Emil Jimenez',
                'CS_pct': 18.2,
                'zone_type': 'wide'
            }
        },
        'park_factor': 98,
        'is_dome': False,
        'game_time': '19:45',
        'away_catcher': 'William Contreras',
        'home_catcher': 'Pedro Pages',
        'away_drs': 15,
        'home_drs': -5,
        'away_manager_hook': 0.0,
        'home_manager_hook': -0.3,
        'away_bp_pitches_d1': 45,
        'away_bp_pitches_d2': 60,
        'home_bp_pitches_d1': 50,
        'home_bp_pitches_d2': 55
    }
    
    market_odds = {
        'MIL Moneyline': -126,
        'STL Moneyline': 106,
        'Total Over 9.0': -110,
        'Chad Patrick Over 3.5 K': -130,
        'Kyle Leahy Over 4.5 K': -115
    }
    
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
    # print(results)

if __name__ == "__main__":
    run_simulation()
