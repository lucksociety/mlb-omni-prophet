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
import statistics
from datetime import datetime

# Add workspace to path



from omni_prophet_v16 import OmniProphetV18

def run_custom_sim():
    # 1. SETUP GAME DATA
    game_data = {
        'away_team': 'Nationals',
        'home_team': 'Reds',
        'away_sp_name': 'Miles Mikolas',
        'home_sp_name': 'Brady Singer',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': 7.44,
        'home_sp_era': 5.63,
        'location': 'Cincinnati',
        'park_factor': 118,  # Great American Ball Park is high offense
        'is_dome': False,
        'game_time': '18:40',
        'game_time_decimal': 18.67,
        'away_bp_pitches_d1': 45, # Estimate based on Varland/others usage
        'away_bp_pitches_d2': 20,
        'home_bp_pitches_d1': 0,  # Fully rested
        'home_bp_pitches_d2': 0,
        'away_drs': -2, # Nationals defense usually poor
        'home_drs': 3,
        'away_manager_hook': 0.1,
        'home_manager_hook': -0.1,
        'away_catcher': 'Keibert Ruiz',
        'home_catcher': 'Tyler Stephenson',
        'away_lineup_k_pct': 24.1, # Estimated average
        'home_lineup_k_pct': 22.5,
        'env': {
            'Weather': {
                'temp': 76,
                'wind_speed': 6,
                'wind_dir': 0, # 0 = Blowing out to CF
                'humidity': 36
            },
            'altitude': 480, # Cincinnati elevation
            'rain_intensity': 0.0,
            'Umpire': {
                'name': 'Dan Bellino',
                'CS_pct': 17.7, # 16.5 baseline + 1.2% wide
                'zone_type': 'wide'
            }
        },
        # V18 Calibration Fields
        'away_lineup_woba_rank_14d': 12,
        'home_lineup_woba_rank_14d': 8,
        'away_sp_blowup_21d': True, # ERA 7.44 indicates recent blowups
        'home_sp_blowup_21d': False,
        'away_sp_era_split_diff': 0.8,
        'home_sp_era_split_diff': 0.3,
        'away_lineup_contact_rank': 18,
        'home_lineup_contact_rank': 10,
        'away_sp_rest_days': 5,
        'home_sp_rest_days': 5,
        'away_sp_recent_whip_4start': 1.65,
        'home_sp_recent_whip_4start': 1.42,
        'away_sp_strong_home_start': False,
        'home_sp_strong_home_start': True,
        'away_sp_1st_era': 6.20, # High 1st inning ERA
        'home_sp_1st_era': 4.10,
        'away_team_1st_rank_30d': 22,
        'home_team_1st_rank_30d': 5, # Reds good at home 1st
        'away_lineup_1st_pct_recent': 0.28,
        'home_lineup_1st_pct_recent': 0.42
    }

    # 2. PITCHER STATCAST INJECTION
    game_data['away_sp_statcast'] = {
        'Name': 'Miles Mikolas',
        'Stuff': 92,
        'VAA': -4.9,
        'K_pct': 16.5,
        'BB_pct': 8.3,
        'ERA': 7.44,
        'xERA': 5.34,
        'IP': 38.0,
        'Starts': 7,
        'CSW': 24.1,
        'SwStr': 9.2,
        'Hand': 'R'
    }
    
    game_data['home_sp_statcast'] = {
        'Name': 'Brady Singer',
        'Stuff': 104,
        'VAA': -4.7,
        'K_pct': 14.6,
        'BB_pct': 5.6,
        'ERA': 5.63,
        'xERA': 4.92,
        'IP': 42.0,
        'Starts': 7,
        'CSW': 27.8,
        'SwStr': 11.4,
        'Hand': 'R'
    }

    # 3. LINEUP STATCAST INJECTION
    # WSH Lineup
    game_data['away_lineup_names'] = ['James Wood', 'Luis Garcia Jr.', 'Brady House', 'CJ Abrams', 'Jacob Young', 'Daylen Lile', 'Nasim Nunez', 'Jose Tena', 'Keibert Ruiz']
    game_data['away_lineup_hands'] = ['L', 'L', 'R', 'L', 'R', 'L', 'S', 'L', 'S']
    game_data['away_lineup_statcast'] = [
        {'Name': 'James Wood', 'K_pct': 32.4, 'O_Swing': 22.3, 'Z_Contact': 76.5, 'wOBA': 0.412, 'Hand': 'L'},
        {'Name': 'Luis Garcia Jr.', 'K_pct': 18.2, 'O_Swing': 34.1, 'Z_Contact': 88.2, 'wOBA': 0.328, 'Hand': 'L'},
        {'Name': 'Brady House', 'K_pct': 28.5, 'O_Swing': 29.0, 'Z_Contact': 79.1, 'wOBA': 0.315, 'Hand': 'R'},
        {'Name': 'CJ Abrams', 'K_pct': 21.0, 'O_Swing': 31.5, 'Z_Contact': 84.6, 'wOBA': 0.342, 'Hand': 'L'},
        {'Name': 'Jacob Young', 'K_pct': 19.5, 'O_Swing': 26.2, 'Z_Contact': 89.0, 'wOBA': 0.294, 'Hand': 'R'},
        {'Name': 'Daylen Lile', 'K_pct': 24.0, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.310, 'Hand': 'L'},
        {'Name': 'Nasim Nunez', 'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.280, 'Hand': 'S'},
        {'Name': 'Jose Tena', 'K_pct': 26.0, 'O_Swing': 32.0, 'Z_Contact': 80.0, 'wOBA': 0.300, 'Hand': 'L'},
        {'Name': 'Keibert Ruiz', 'K_pct': 15.0, 'O_Swing': 35.0, 'Z_Contact': 90.0, 'wOBA': 0.310, 'Hand': 'S'}
    ]

    # CIN Lineup
    game_data['home_lineup_names'] = ['TJ Friedl', 'Spencer Steer', 'Elly De La Cruz', 'Sal Stewart', 'Matt McLain', 'Will Benson', 'Tyler Stephenson', 'Ke\'Bryan Hayes', 'JJ Bleday']
    game_data['home_lineup_hands'] = ['L', 'R', 'S', 'R', 'R', 'L', 'R', 'R', 'L']
    game_data['home_lineup_statcast'] = [
        {'Name': 'TJ Friedl', 'K_pct': 16.8, 'O_Swing': 24.5, 'Z_Contact': 91.2, 'wOBA': 0.310, 'Hand': 'L'},
        {'Name': 'Spencer Steer', 'K_pct': 20.1, 'O_Swing': 27.8, 'Z_Contact': 85.5, 'wOBA': 0.335, 'Hand': 'R'}, # 108 wRC+ -> ~0.335 wOBA
        {'Name': 'Elly De La Cruz', 'K_pct': 29.8, 'O_Swing': 28.1, 'Z_Contact': 74.2, 'wOBA': 0.380, 'Hand': 'S'}, # 140 wRC+ -> ~0.380 wOBA
        {'Name': 'Sal Stewart', 'K_pct': 22.4, 'O_Swing': 25.0, 'Z_Contact': 82.0, 'wOBA': 0.345, 'Hand': 'R'}, # 115 wRC+
        {'Name': 'Matt McLain', 'K_pct': 24.2, 'O_Swing': 29.4, 'Z_Contact': 81.3, 'wOBA': 0.340, 'Hand': 'R'}, # 112 wRC+
        {'Name': 'Will Benson', 'K_pct': 30.0, 'O_Swing': 26.0, 'Z_Contact': 78.0, 'wOBA': 0.320, 'Hand': 'L'},
        {'Name': 'Tyler Stephenson', 'K_pct': 21.0, 'O_Swing': 32.0, 'Z_Contact': 84.0, 'wOBA': 0.325, 'Hand': 'R'},
        {'Name': 'Ke\'Bryan Hayes', 'K_pct': 19.0, 'O_Swing': 30.0, 'Z_Contact': 86.0, 'wOBA': 0.315, 'Hand': 'R'},
        {'Name': 'JJ Bleday', 'K_pct': 22.0, 'O_Swing': 25.0, 'Z_Contact': 83.0, 'wOBA': 0.330, 'Hand': 'L'}
    ]

    # 4. RUN SIMULATION
    omni = OmniProphetV18()
    
    # Market Odds for EV Calculation
    market_odds = {
        'CIN ML': -149,
        'WSH ML': +125,
        'Total Over 9.5': -110,
        'Total Under 9.5': -110,
        'Brady Singer Over 5.5 K': +110,
        'Miles Mikolas Under 4.5 K': -125
    }

    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == "__main__":
    run_custom_sim()