
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

from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from omni_prophet_v16 import OmniProphetV18

def run_simulation():
    omni = OmniProphetV18()
    
    # ── GAME DATA: STL @ SD (May 10, 2026) ──────────────────
    # Data source: User Request Intel + Lineup Image
    game_data = {
        'away_team': 'STL',
        'home_team': 'SD',
        'away_sp_name': 'Kyle Leahy',
        'home_sp_name': 'Walker Buehler',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        
        # Pitcher Stats (V19.1 Ingested from User Intel)
        # Kyle Leahy (STL)
        'away_sp_era': 4.93,
        'away_sp_k_pct': 17.5, # 27 K in 34.2 IP
        'away_sp_statcast': {
            'Stuff': 98.2,
            'K_pct': 17.5,
            'BB_pct': 10.5, # High WHIP (1.64) suggests BB risk
            'VAA': -4.3,
            'IP': 34.2,
            'Starts': 6, # Estimated from IP
            'ERA': 4.93,
            'xERA': 4.65,
            'HR_FB': 12.5,
            'LastPitchCount': 88
        },
        
        # Walker Buehler (SD)
        'home_sp_era': 5.64,
        'home_sp_k_pct': 22.8, # 29 K in 30.1 IP
        'home_sp_statcast': {
            'Stuff': 108.5, # "Swing-and-miss stuff remains elite"
            'K_pct': 22.8,
            'BB_pct': 9.2,
            'VAA': -4.6,
            'IP': 30.1,
            'Starts': 6,
            'ERA': 5.64,
            'xERA': 4.10, # Inflated ERA suggests regression toward xERA
            'HR_FB': 15.0, # Prone to the long ball in 2026
            'LastPitchCount': 92
        },
        
        # Lineups (Confirmed from Image)
        'away_lineup_names': ['JJ Wetherholt', 'Ivan Herrera', 'A. Burleson', 'Jordan Walker', 'Nolan Gorman', 'Masyn Winn', 'N. Church', 'T. Saggese', 'Pedro Pages'],
        'away_lineup_hands': ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'R'],
        'away_lineup_statcast': [
            {'Name': 'JJ Wetherholt', 'wOBA': 0.355, 'K_pct': 18.5, 'O_Swing': 24.4}, # Rookie sensation
            {'Name': 'Ivan Herrera', 'wOBA': 0.345, 'K_pct': 15.0, 'O_Swing': 24.7}, # High OBP
            {'Name': 'A. Burleson', 'wOBA': 0.325, 'K_pct': 13.0, 'O_Swing': 27.0},
            {'Name': 'Jordan Walker', 'wOBA': 0.405, 'K_pct': 28.5, 'O_Swing': 32.0}, # MVP Candidate
            {'Name': 'Nolan Gorman', 'wOBA': 0.315, 'K_pct': 29.0, 'O_Swing': 28.0},
            {'Name': 'Masyn Winn', 'wOBA': 0.322, 'K_pct': 21.0, 'O_Swing': 31.0},
            {'Name': 'N. Church', 'wOBA': 0.310, 'K_pct': 25.0, 'O_Swing': 25.0},
            {'Name': 'T. Saggese', 'wOBA': 0.295, 'K_pct': 26.0, 'O_Swing': 26.0},
            {'Name': 'Pedro Pages', 'wOBA': 0.285, 'K_pct': 27.0, 'O_Swing': 26.0},
        ],
        
        'home_lineup_names': ['Jackson Merrill', 'F. Tatis Jr.', 'Manny Machado', 'Gavin Sheets', 'X. Bogaerts', 'M. Andujar', 'Ty France', 'S. Song', 'R. Duran'],
        'home_lineup_hands': ['L', 'R', 'R', 'L', 'R', 'R', 'R', 'L', 'R'],
        'home_lineup_statcast': [
            {'Name': 'Jackson Merrill', 'wOBA': 0.305, 'K_pct': 24.5, 'O_Swing': 26.7},
            {'Name': 'F. Tatis Jr.', 'wOBA': 0.335, 'K_pct': 24.0, 'O_Swing': 34.6},
            {'Name': 'Manny Machado', 'wOBA': 0.298, 'K_pct': 19.5, 'O_Swing': 25.4},
            {'Name': 'Gavin Sheets', 'wOBA': 0.312, 'K_pct': 21.5, 'O_Swing': 26.7},
            {'Name': 'X. Bogaerts', 'wOBA': 0.365, 'K_pct': 21.0, 'O_Swing': 29.8}, # Leading team
            {'Name': 'M. Andujar', 'wOBA': 0.290, 'K_pct': 24.0, 'O_Swing': 24.1},
            {'Name': 'Ty France', 'wOBA': 0.302, 'K_pct': 22.0, 'O_Swing': 28.0},
            {'Name': 'S. Song', 'wOBA': 0.315, 'K_pct': 20.0, 'O_Swing': 20.0},
            {'Name': 'R. Duran', 'wOBA': 0.285, 'K_pct': 25.0, 'O_Swing': 26.0},
        ],
        
        # Environmental Factors
        'location': 'SD',
        'park_factor': 95, # Petco Park (Pitcher Friendly)
        'is_dome': False,
        'env': {
            'Weather': {
                'temp': 65,
                'wind_speed': 8,
                'wind_dir': 0, # 0 = Blowing out
                'humidity': 55
            },
            'altitude': 15,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        },
        
        # Bullpen & Defense
        'away_bp_avg_era': 4.15,
        'home_bp_avg_era': 3.92,
        'away_bp_pitches_d1': 25,
        'away_bp_pitches_d2': 35,
        'home_bp_pitches_d1': 40,
        'home_bp_pitches_d2': 10,
        'away_drs': 2,
        'home_drs': 4,
        'away_catcher': 'Pedro Pages',
        'home_catcher': 'R. Duran',
        'away_manager_hook': 0.85, # Leahy on short-ish leash
        'home_manager_hook': 0.90, # Buehler veteran leash
        'game_time': '16:10'
    }
    
    market_odds = {
        'Cardinals Moneyline': +118,
        'Padres Moneyline': -137,
        'Total Over 8.5': -105,
        'Total Under 8.5': -115,
        'NRFI': -115,
        'YRFI': -115,
        'Walker Buehler Over 5.5 K': -120,
        'Walker Buehler Under 5.5 K': +100,
        'Kyle Leahy Over 4.5 K': -110,
        'Kyle Leahy Under 4.5 K': -110,
    }
    
    # Run Omni Simulation
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
    
    if results:
        print("\nSimulation Complete.")

if __name__ == "__main__":
    run_simulation()