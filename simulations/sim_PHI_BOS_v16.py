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
    # 1. Start with the confirmed 2026 Statcast data provided by the user
    # Zack Wheeler (PHI)
    away_sp_sc = {
        'Name': 'Zack Wheeler',
        'Stuff': 118,
        'Location': 106,
        'VAA': -4.91,
        'K_pct': 26.5,
        'BB_pct': 6.2,
        'ERA': 3.12,
        'xERA': 3.28,
        'xFIP': 3.41,
        'CSW': 30.1,
        'SwStr': 14.2,
        'IP': 45.0, # Estimated from 7 starts
        'Starts': 7,
        'Hand': 'R'
    }

    # Brayan Bello (BOS) - Bulk Pitcher
    home_sp_sc = {
        'Name': 'Brayan Bello',
        'Stuff': 94,
        'Location': 98,
        'VAA': -4.45,
        'K_pct': 13.0,
        'BB_pct': 11.3,
        'ERA': 7.44,
        'xERA': 5.82,
        'xFIP': 5.12,
        'CSW': 24.5,
        'SwStr': 9.8,
        'IP': 40.0,
        'Starts': 7,
        'Hand': 'R',
        'ShortLeash': True # Opener Morán is pitching first
    }

    # 2. Lineup Forensics
    # PHI Lineup (Away)
    away_lineup_statcast = [
        {'Name': 'Trea Turner', 'K_pct': 18.2, 'wOBA': 0.312, 'O_Swing': 31.4, 'Z_Contact': 88.5, 'Hand': 'R'},
        {'Name': 'Kyle Schwarber', 'K_pct': 27.5, 'wOBA': 0.405, 'O_Swing': 22.1, 'Z_Contact': 74.2, 'Hand': 'L'},
        {'Name': 'Bryce Harper', 'K_pct': 20.1, 'wOBA': 0.388, 'O_Swing': 25.6, 'Z_Contact': 85.1, 'Hand': 'L'},
        {'Name': 'Adolis Garcia', 'K_pct': 29.4, 'wOBA': 0.290, 'O_Swing': 36.8, 'Z_Contact': 80.4, 'Hand': 'R'},
        {'Name': 'Brandon Marsh', 'K_pct': 24.6, 'wOBA': 0.366, 'O_Swing': 29.0, 'Z_Contact': 82.3, 'Hand': 'L'},
        {'Name': 'Bryson Stott', 'K_pct': 16.5, 'wOBA': 0.245, 'O_Swing': 24.3, 'Z_Contact': 91.0, 'Hand': 'L'},
        {'Name': 'Alec Bohm', 'K_pct': 17.5, 'wOBA': 0.310, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'Hand': 'R'},
        {'Name': 'J.T. Realmuto', 'K_pct': 22.0, 'wOBA': 0.305, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'Hand': 'R'},
        {'Name': 'Justin Crawford', 'K_pct': 25.0, 'wOBA': 0.280, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'Hand': 'L'}
    ]

    # BOS Lineup (Home) - Defaults for missing stats
    home_lineup_statcast = [
        {'Name': 'Jarren Duran', 'K_pct': 25.2, 'wOBA': 0.320, 'O_Swing': 28.0, 'Z_Contact': 80.0, 'Hand': 'L'},
        {'Name': 'Mickey Gasper', 'K_pct': 22.0, 'wOBA': 0.300, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'Hand': 'S'},
        {'Name': 'Wilyer Abreu', 'K_pct': 26.0, 'wOBA': 0.330, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'Hand': 'L'},
        {'Name': 'Masataka Yoshida', 'K_pct': 14.0, 'wOBA': 0.340, 'O_Swing': 25.0, 'Z_Contact': 90.0, 'Hand': 'L'},
        {'Name': 'Trevor Story', 'K_pct': 28.0, 'wOBA': 0.290, 'O_Swing': 32.0, 'Z_Contact': 78.0, 'Hand': 'R'},
        {'Name': 'Ceddanne Rafaela', 'K_pct': 24.0, 'wOBA': 0.285, 'O_Swing': 35.0, 'Z_Contact': 82.0, 'Hand': 'R'},
        {'Name': 'Marcelo Mayer', 'K_pct': 23.0, 'wOBA': 0.310, 'O_Swing': 30.0, 'Z_Contact': 84.0, 'Hand': 'L'},
        {'Name': 'Carlos Narvaez', 'K_pct': 20.0, 'wOBA': 0.295, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'Hand': 'R'},
        {'Name': 'Caleb Durbin', 'K_pct': 15.0, 'wOBA': 0.305, 'O_Swing': 22.0, 'Z_Contact': 92.0, 'Hand': 'R'}
    ]

    # 3. Environment
    game_data = {
        'away_team': 'Phillies',
        'home_team': 'Red Sox',
        'away_sp_name': 'Zack Wheeler',
        'home_sp_name': 'Brayan Bello',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': away_sp_sc['ERA'],
        'home_sp_era': home_sp_sc['ERA'],
        'away_sp_statcast': away_sp_sc,
        'home_sp_statcast': home_sp_sc,
        'away_lineup_names': [b['Name'] for b in away_lineup_statcast],
        'home_lineup_names': [b['Name'] for b in home_lineup_statcast],
        'away_lineup_hands': [b['Hand'] for b in away_lineup_statcast],
        'home_lineup_hands': [b['Hand'] for b in home_lineup_statcast],
        'away_lineup_statcast': away_lineup_statcast,
        'home_lineup_statcast': home_lineup_statcast,
        'park_factor': 105, # Fenway is neutral-to-hitter friendly
        'is_dome': False,
        'location': 'BOS',
        'game_time': '19:10',
        'game_time_decimal': 19.16,
        'env': {
            'Weather': {'temp': 61, 'wind_speed': 7, 'wind_dir': 45, 'humidity': 55}, # 7mph L-R
            'altitude': 20,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Alan Porter', 'CS_pct': 16.0, 'zone_type': 'neutral'} # User said slightly hitter friendly
        },
        'away_drs': 5, # PHI generally good defense
        'home_drs': -2,
        'away_manager_hook': 0.0,
        'home_manager_hook': 0.2, # Bello on short leash with opener
        'away_bp_pitches_d1': 20,
        'away_bp_pitches_d2': 0,
        'home_bp_pitches_d1': 45, # User said heavy usage
        'home_bp_pitches_d2': 30,
        'away_catcher': 'J.T. Realmuto',
        'home_catcher': 'Carlos Narvaez',
        'away_bp_avg_era': 3.80,
        'home_bp_avg_era': 4.50,
        'away_lineup_k_pct': statistics.mean([b['K_pct'] for b in away_lineup_statcast]),
        'home_lineup_k_pct': statistics.mean([b['K_pct'] for b in home_lineup_statcast]),
        'away_lineup_woba_rank_14d': 29, # Team rank 29th
        'home_lineup_woba_rank_14d': 15,
        'away_sp_rest_days': 5,
        'home_sp_rest_days': 7,
        'away_sp_recent_whip_4start': 0.98,
        'home_sp_recent_whip_4start': 1.65,
        'away_sp_strong_home_start': False,
        'home_sp_strong_home_start': True, # User said Bello had quality start May 5
    }

    market_odds = {
        'PHI ML': -143,
        'BOS ML': 120,
        'Total Over 8.0': -110,
        'Total Under 8.0': -110,
        'Zack Wheeler Over 6.5 K': -120,
        'Brayan Bello Under 4.5 K': -130
    }

    omni = OmniProphetV18()
    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == "__main__":
    run_custom_sim()