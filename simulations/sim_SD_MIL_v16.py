
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
        'away_team': 'SD',
        'home_team': 'MIL',
        'away_sp_name': 'Matt Waldron',
        'home_sp_name': 'Brandon Sproat',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': 7.71,
        'home_sp_era': 5.87,
        'location': 'MIL',
        'park_factor': 105,  # American Family Field
        'is_dome': True,
        'game_time': '19:40',
        'game_time_decimal': 19.67,
        'away_bp_pitches_d1': 20, 
        'away_bp_pitches_d2': 25,
        'home_bp_pitches_d1': 10,
        'home_bp_pitches_d2': 10,
        'away_drs': 4, 
        'home_drs': 3,
        'away_manager_hook': -0.5, # Waldron on short leash
        'home_manager_hook': 0.0,
        'away_catcher': 'Freddy Fermin',
        'home_catcher': 'William Contreras',
        'away_lineup_k_pct': 23.3, # Calculated from stats below
        'home_lineup_k_pct': 22.1,
        'env': {
            'Weather': {
                'temp': 72,
                'wind_speed': 0,
                'wind_dir': 0,
                'humidity': 50
            },
            'altitude': 600,
            'rain_intensity': 0.0,
            'Umpire': {
                'name': 'Unknown',
                'zone_type': 'neutral'
            }
        },
        'away_lineup_woba_rank_14d': 15,
        'home_lineup_woba_rank_14d': 10,
        'away_sp_blowup_21d': True,
        'home_sp_blowup_21d': False,
        'away_sp_era_split_diff': 0.5,
        'home_sp_era_split_diff': 0.2,
        'away_lineup_contact_rank': 15,
        'home_lineup_contact_rank': 12,
        'away_sp_rest_days': 5,
        'home_sp_rest_days': 5,
        'away_sp_recent_whip_4start': 1.65,
        'home_sp_recent_whip_4start': 1.45,
        'away_sp_strong_home_start': False,
        'home_sp_strong_home_start': False,
        'away_sp_1st_era': 6.50,
        'home_sp_1st_era': 4.80,
        'away_team_1st_rank_30d': 20,
        'home_team_1st_rank_30d': 12
    }

    # 2. PITCHER STATCAST INJECTION (from overrides.json)
    game_data['away_sp_statcast'] = {
        'Name': 'Matt Waldron',
        'Stuff': 82,
        'VAA': -4.5,
        'K_pct': 16.8,
        'BB_pct': 11.2,
        'ERA': 7.71,
        'xERA': 6.80,
        'IP': 30.0,
        'Starts': 6,
        'Hand': 'R',
        'ShortLeash': True,
        'Volatility': True
    }
    
    game_data['home_sp_statcast'] = {
        'Name': 'Brandon Sproat',
        'Stuff': 110,
        'VAA': -4.7,
        'K_pct': 24.2,
        'BB_pct': 10.2,
        'ERA': 5.87,
        'xERA': 4.80, # Estimated from override context
        'IP': 25.0,
        'Starts': 5,
        'Hand': 'R',
        'Volatility': True
    }

    # 3. LINEUP STATCAST INJECTION
    # SD Lineup
    game_data['away_lineup_names'] = ['Jackson Merrill', 'F. Tatis Jr.', 'Manny Machado', 'Miguel Andujar', 'X. Bogaerts', 'Gavin Sheets', 'Nick Castellanos', 'Ramón Laureano', 'Freddy Fermin']
    game_data['away_lineup_hands'] = ['L', 'R', 'R', 'R', 'R', 'L', 'R', 'L', 'R']
    game_data['away_lineup_statcast'] = [
        {'Name': 'Jackson Merrill', 'K_pct': 24.5, 'O_Swing': 26.7, 'Z_Contact': 80.0, 'wOBA': 0.305, 'Hand': 'L'},
        {'Name': 'F. Tatis Jr.', 'K_pct': 24.0, 'O_Swing': 34.6, 'Z_Contact': 82.0, 'wOBA': 0.335, 'Hand': 'R'},
        {'Name': 'Manny Machado', 'K_pct': 19.5, 'O_Swing': 25.4, 'Z_Contact': 85.0, 'wOBA': 0.298, 'Hand': 'R'},
        {'Name': 'Miguel Andujar', 'K_pct': 24.0, 'O_Swing': 24.1, 'Z_Contact': 88.0, 'wOBA': 0.290, 'Hand': 'R'},
        {'Name': 'X. Bogaerts', 'K_pct': 21.0, 'O_Swing': 29.8, 'Z_Contact': 86.0, 'wOBA': 0.365, 'Hand': 'R'},
        {'Name': 'Gavin Sheets', 'K_pct': 21.5, 'O_Swing': 26.7, 'Z_Contact': 82.0, 'wOBA': 0.312, 'Hand': 'L'},
        {'Name': 'Nick Castellanos', 'K_pct': 26.2, 'O_Swing': 35.0, 'Z_Contact': 78.0, 'wOBA': 0.310, 'Hand': 'R'},
        {'Name': 'Ramón Laureano', 'K_pct': 27.8, 'O_Swing': 30.0, 'Z_Contact': 80.0, 'wOBA': 0.338, 'Hand': 'L'},
        {'Name': 'Freddy Fermin', 'K_pct': 21.0, 'O_Swing': 30.0, 'Z_Contact': 84.0, 'wOBA': 0.280, 'Hand': 'R'}
    ]

    # MIL Lineup
    game_data['home_lineup_names'] = ['Brice Turang', 'Jackson Chourio', 'Christian Yelich', 'William Contreras', 'Jake Bauers', 'Garrett Mitchell', 'Sal Frelick', 'David Hamilton', 'Joey Ortiz']
    game_data['home_lineup_hands'] = ['L', 'R', 'L', 'R', 'L', 'L', 'L', 'L', 'R']
    game_data['home_lineup_statcast'] = [
        {'Name': 'Brice Turang', 'K_pct': 23.8, 'O_Swing': 26.0, 'Z_Contact': 87.0, 'wOBA': 0.360, 'Hand': 'L'},
        {'Name': 'Jackson Chourio', 'K_pct': 22.5, 'O_Swing': 33.0, 'Z_Contact': 83.0, 'wOBA': 0.380, 'Hand': 'R'},
        {'Name': 'Christian Yelich', 'K_pct': 25.7, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.320, 'Hand': 'L'},
        {'Name': 'William Contreras', 'K_pct': 16.2, 'O_Swing': 29.0, 'Z_Contact': 85.0, 'wOBA': 0.350, 'Hand': 'R'},
        {'Name': 'Jake Bauers', 'K_pct': 21.1, 'O_Swing': 30.0, 'Z_Contact': 75.0, 'wOBA': 0.340, 'Hand': 'L'},
        {'Name': 'Garrett Mitchell', 'K_pct': 28.0, 'O_Swing': 32.0, 'Z_Contact': 80.0, 'wOBA': 0.300, 'Hand': 'L'},
        {'Name': 'Sal Frelick', 'K_pct': 13.3, 'O_Swing': 26.0, 'Z_Contact': 90.0, 'wOBA': 0.262, 'Hand': 'L'},
        {'Name': 'David Hamilton', 'K_pct': 20.0, 'O_Swing': 33.0, 'Z_Contact': 80.0, 'wOBA': 0.320, 'Hand': 'L'},
        {'Name': 'Joey Ortiz', 'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.315, 'Hand': 'R'}
    ]

    # 4. RUN SIMULATION
    omni = OmniProphetV18()
    
    # Market Odds for EV Calculation
    market_odds = {
        'MIL Moneyline': -149,
        'SD Moneyline': +125,
        'Total Over 9.0': -110,
        'Total Under 9.0': -110,
        'Brandon Sproat Over 5.5 K': -115,
        'Matt Waldron Under 4.5 K': -130
    }

    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == "__main__":
    run_custom_sim()