
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
    
    # ── GAME DATA: DET @ KC (May 10, 2026) ──────────────────
    game_data = {
        'away_team': 'DET',
        'home_team': 'KC',
        'away_sp_name': 'Drew Anderson',
        'home_sp_name': 'Noah Cameron',
        'away_sp_hand': 'R',
        'home_sp_hand': 'L',
        
        # Pitcher Stats (V19.1 Adjusted)
        'away_sp_era': 4.79,
        'away_sp_k_pct': 25.8,
        'away_sp_statcast': {
            'Stuff': 94.0,
            'K_pct': 25.8,
            'BB_pct': 12.1,
            'VAA': -4.4,
            'IP': 28.0, # Rookie/Low sample
            'Starts': 4,
            'ERA': 4.79,
            'xERA': 3.67,
            'HR_FB': 13.6,
            'LastPitchCount': 88
        },
        
        'home_sp_era': 5.40,
        'home_sp_k_pct': 20.0,
        'home_sp_statcast': {
            'Stuff': 102.0,
            'K_pct': 20.0,
            'BB_pct': 8.0,
            'VAA': -4.5,
            'IP': 32.0,
            'Starts': 5,
            'ERA': 5.40,
            'xERA': 4.34,
            'HR_FB': 11.0,
            'LastPitchCount': 92
        },
        
        # Lineups
        'away_lineup_names': ['Vierling', 'McGonigle', 'J. Jones', 'Dingler', 'Greene', 'Perez', 'Torkelson', 'McKinstry', 'Lee'],
        'away_lineup_hands': ['R', 'L', 'R', 'R', 'L', 'S', 'R', 'L', 'R'],
        'away_lineup_statcast': [
            {'wOBA': 0.320, 'K_pct': 22.7, 'O_Swing': 30.0}, # Vierling
            {'wOBA': 0.345, 'K_pct': 18.0, 'O_Swing': 26.0}, # McGonigle
            {'wOBA': 0.310, 'K_pct': 25.0, 'O_Swing': 32.0}, # Jones
            {'wOBA': 0.330, 'K_pct': 20.5, 'O_Swing': 28.0}, # Dingler
            {'wOBA': 0.405, 'K_pct': 29.7, 'O_Swing': 27.0}, # Greene
            {'wOBA': 0.325, 'K_pct': 22.0, 'O_Swing': 31.0}, # Perez
            {'wOBA': 0.335, 'K_pct': 28.4, 'O_Swing': 25.0}, # Torkelson
            {'wOBA': 0.290, 'K_pct': 24.0, 'O_Swing': 33.0}, # McKinstry
            {'wOBA': 0.280, 'K_pct': 22.7, 'O_Swing': 30.0}, # Lee
        ],
        
        'home_lineup_names': ['Garcia', 'Witt Jr', 'Pasquantino', 'Collins', 'Jensen', 'Loftin', 'Caglianone', 'Diaz', 'Isbel'],
        'home_lineup_hands': ['R', 'R', 'L', 'S', 'L', 'R', 'L', 'R', 'L'],
        'home_lineup_statcast': [
            {'wOBA': 0.330, 'K_pct': 12.6, 'O_Swing': 22.0}, # Garcia
            {'wOBA': 0.385, 'K_pct': 18.1, 'O_Swing': 24.0}, # Witt Jr
            {'wOBA': 0.340, 'K_pct': 16.6, 'O_Swing': 22.0}, # Pasquantino
            {'wOBA': 0.320, 'K_pct': 22.2, 'O_Swing': 30.0}, # Collins
            {'wOBA': 0.310, 'K_pct': 22.7, 'O_Swing': 28.0}, # Jensen
            {'wOBA': 0.335, 'K_pct': 22.7, 'O_Swing': 26.0}, # Loftin
            {'wOBA': 0.345, 'K_pct': 22.7, 'O_Swing': 29.0}, # Caglianone
            {'wOBA': 0.335, 'K_pct': 20.0, 'O_Swing': 28.0}, # Diaz
            {'wOBA': 0.300, 'K_pct': 22.7, 'O_Swing': 32.0}, # Isbel
        ],
        
        # Environmental Factors
        'location': 'KC',
        'park_factor': 98,
        'is_dome': False,
        'env': {
            'Weather': {
                'temp': 68,
                'wind_speed': 7,
                'wind_dir': 180, # 180 = Blowing IN
                'humidity': 55
            },
            'altitude': 277,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Neutral', 'zone_type': 'neutral'}
        },
        
        # Bullpen & Defense
        'away_bp_avg_era': 4.20, # Tigers BP
        'home_bp_avg_era': 4.35, # Royals BP
        'away_bp_pitches_d1': 60, # Heavily utilized per prompt
        'away_bp_pitches_d2': 40,
        'home_bp_pitches_d1': 20,
        'home_bp_pitches_d2': 15,
        'away_drs': 2,
        'home_drs': -1,
        'away_catcher': 'Dillon Dingler',
        'home_catcher': 'Elias Diaz',
        'away_manager_hook': 1.1, # Short leash due to bullpen utilization? Actually no, Anderson needs to provide length.
        'home_manager_hook': 0.9,
        'game_time': '19:00',
        'bullpen_burn': 0.4 # Higher for Detroit
    }
    
    market_odds = {
        'Tigers Moneyline': +103,
        'Royals Moneyline': -123,
        'Total Over 8.5': -110,
        'Total Under 8.5': -110,
        'Detroit Tigers +1.5 Runline': -200,
        'Kansas City Royals -1.5 Runline': +170,
        'First 5 Tigers Moneyline': -105,
        'First 5 Royals Moneyline': -125,
        'First 5 Over 4.5': -115,
        'First 5 Under 4.5': -115,
        'Noah Cameron Over 4.5 K': -135,
        'Noah Cameron Under 4.5 K': +105,
        'Drew Anderson Over 4.5 K': -110,
        'Drew Anderson Under 4.5 K': -120,
        'NRFI (No Run 1st Inning)': -120,
        'YRFI (Yes Run 1st Inning)': -110,
        'Riley Greene Home Run': +625,
        'Bobby Witt Jr Home Run': +500,
        'Spencer Torkelson Home Run': +500,
        'Vinnie Pasquantino Home Run': +500,
        'Jac Caglianone Home Run': +500,
        'Elias Diaz Home Run': +700
    }
    
    # Run Omni Simulation
    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == "__main__":
    run_simulation()