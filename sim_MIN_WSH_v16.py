import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from omni_prophet_v16 import OmniProphetV16

game_data = {
    'away_team': 'MIN',
    'home_team': 'WSH',
    'away_sp_name': 'Simeon Woods Richardson',
    'home_sp_name': 'Jake Irvin',
    'away_sp_hand': 'R',
    'home_sp_hand': 'R',
    'away_sp_era': 6.49,
    'home_sp_era': 4.93,
    'away_lineup_names': [
        'Byron Buxton', 'Trevor Larnach', 'Austin Martin', 'Ryan Jeffers', 
        'Matt Wallner', 'Luke Keaschall', 'Kody Clemens', 'Brooks Lee', 'Tristan Gray'
    ],
    'away_lineup_hands': ['R', 'L', 'R', 'R', 'L', 'R', 'L', 'S', 'L'],
    'home_lineup_names': [
        'James Wood', 'Daylen Lile', 'Curtis Mead', 'CJ Abrams', 
        'Brady House', 'Jose Tena', 'Jacob Young', 'Keibert Ruiz', 'Nasim Nuñez'
    ],
    'home_lineup_hands': ['L', 'L', 'R', 'L', 'R', 'L', 'R', 'S', 'S'],
    
    'away_sp_statcast': {
        'Stuff': 88,
        'VAA': -1.5,
        'K_pct': 11.0,
        'BB_pct': 9.6,
        'IP': 34.2,
        'xERA': 5.78,
        'CSW_L3': 24.5,
        'SwStr_L3': 8.5,
        'VeloTrend': 'Stable'
    },
    'home_sp_statcast': {
        'Stuff': 102,
        'VAA': -1.3,
        'K_pct': 26.4,
        'BB_pct': 8.5,
        'IP': 34.2,
        'xERA': 4.10,
        'CSW_L3': 28.5,
        'SwStr_L3': 11.2,
        'VeloTrend': 'Stable'
    },
    
    'away_lineup_statcast': [
        {'K_pct': 27.6, 'O_Swing': 32.0, 'Z_Contact': 80.0},
        {'K_pct': 25.0, 'O_Swing': 33.0, 'Z_Contact': 82.0},
        {'K_pct': 13.7, 'O_Swing': 25.0, 'Z_Contact': 90.0},
        {'K_pct': 25.0, 'O_Swing': 34.0, 'Z_Contact': 84.0},
        {'K_pct': 36.8, 'O_Swing': 38.0, 'Z_Contact': 70.0},
        {'K_pct': 14.0, 'O_Swing': 28.0, 'Z_Contact': 88.0},
        {'K_pct': 26.0, 'O_Swing': 32.0, 'Z_Contact': 82.0},
        {'K_pct': 16.2, 'O_Swing': 30.0, 'Z_Contact': 85.0},
        {'K_pct': 28.0, 'O_Swing': 35.0, 'Z_Contact': 78.0}
    ],
    'home_lineup_statcast': [
        {'K_pct': 36.7, 'O_Swing': 42.0, 'Z_Contact': 70.0},
        {'K_pct': 15.8, 'O_Swing': 28.0, 'Z_Contact': 90.0},
        {'K_pct': 18.2, 'O_Swing': 30.0, 'Z_Contact': 85.0},
        {'K_pct': 20.0, 'O_Swing': 32.0, 'Z_Contact': 82.0},
        {'K_pct': 31.8, 'O_Swing': 35.0, 'Z_Contact': 75.0},
        {'K_pct': 22.0, 'O_Swing': 32.0, 'Z_Contact': 80.0},
        {'K_pct': 15.6, 'O_Swing': 25.0, 'Z_Contact': 92.0},
        {'K_pct': 15.0, 'O_Swing': 30.0, 'Z_Contact': 88.0},
        {'K_pct': 20.2, 'O_Swing': 30.0, 'Z_Contact': 88.0}
    ],
    
    'env': {
        'Weather': {
            'temp': 59,
            'wind_speed': 3,
            'wind_dir': 0, # Minimal
            'humidity': 45
        },
        'altitude': 25,
        'rain_intensity': 0.05,
        'adi': 100.0,
        'Umpire': {
            'name': 'TBD',
            'zone_type': 'neutral',
            'CS_pct': 16.0
        }
    },
    'park_factor': 100,
    'is_dome': False,
    'game_time': '13:05',
    'away_drs': 0,
    'home_drs': 0,
    'away_manager_hook': 0.0,
    'home_manager_hook': 0.0,
    'away_bp_pitches_d1': 0,
    'away_bp_pitches_d2': 0,
    'home_bp_pitches_d1': 0,
    'home_bp_pitches_d2': 0,
    'away_catcher': 'Ryan Jeffers',
    'home_catcher': 'Keibert Ruiz'
}

market_odds = {
    'Nationals Moneyline': -126,
    'Twins Moneyline': 106,
    'Total O/U 9.0': -110
}

if __name__ == '__main__':
    omni = OmniProphetV16()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
