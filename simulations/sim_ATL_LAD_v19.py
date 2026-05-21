
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
    
    # ── GAME DATA: ATL @ LAD (May 10, 2026) ──────────────────
    # Data source: ingest_user_pitching_v2.py & ingest_user_batting_v2.py
    game_data = {
        'away_team': 'ATL',
        'home_team': 'LAD',
        'away_sp_name': 'Bryce Elder',
        'home_sp_name': 'Justin Wrobleski',
        'away_sp_hand': 'R',
        'home_sp_hand': 'L',
        
        # Pitcher Stats (V19.1 Ingested)
        # Bryce Elder (ATL)
        'away_sp_era': 1.88,
        'away_sp_k_pct': 23.2, # 7.53 K/9
        'away_sp_statcast': {
            'Stuff': 92.7,
            'K_pct': 23.2,
            'BB_pct': 8.4,
            'VAA': -4.4,
            'IP': 43.0,
            'Starts': 7,
            'ERA': 1.88,
            'xERA': 3.12, # xFIP from DB
            'HR_FB': 4.5,
            'LastPitchCount': 90
        },
        
        # Justin Wrobleski (LAD)
        'home_sp_era': 1.25,
        'home_sp_k_pct': 11.5, # 3.75 K/9 (from DB index 9)
        'home_sp_statcast': {
            'Stuff': 93.8,
            'K_pct': 11.5,
            'BB_pct': 7.7,
            'VAA': -4.5,
            'IP': 36.0,
            'Starts': 6,
            'ERA': 1.25,
            'xERA': 3.23, # xFIP from DB
            'HR_FB': 0.0,
            'LastPitchCount': 95
        },
        
        # Lineups
        'away_lineup_names': ['Dubon', 'Baldwin', 'Albies', 'Olson', 'Riley', 'Harris II', 'White', 'Murphy', 'Mateo'],
        'away_lineup_hands': ['R', 'L', 'S', 'L', 'R', 'L', 'R', 'R', 'R'],
        'away_lineup_statcast': [
            {'wOBA': 0.322, 'K_pct': 16.3, 'O_Swing': 32.0}, # Dubon
            {'wOBA': 0.405, 'K_pct': 19.3, 'O_Swing': 28.0}, # Baldwin
            {'wOBA': 0.407, 'K_pct': 11.6, 'O_Swing': 24.0}, # Albies
            {'wOBA': 0.440, 'K_pct': 22.2, 'O_Swing': 25.0}, # Olson
            {'wOBA': 0.296, 'K_pct': 25.7, 'O_Swing': 33.0}, # Riley
            {'wOBA': 0.392, 'K_pct': 18.4, 'O_Swing': 36.0}, # Harris II
            {'wOBA': 0.275, 'K_pct': 19.3, 'O_Swing': 31.0}, # White
            {'wOBA': 0.300, 'K_pct': 22.0, 'O_Swing': 28.0}, # Murphy (Regressed from PA=3)
            {'wOBA': 0.346, 'K_pct': 36.2, 'O_Swing': 38.0}, # Mateo
        ],
        
        'home_lineup_names': ['Ohtani', 'Freeman', 'Pages', 'Tucker', 'Muncy', 'Call', 'Rushing', 'Kim', 'Freeland'],
        'home_lineup_hands': ['L', 'L', 'R', 'L', 'L', 'R', 'L', 'R', 'S'],
        'home_lineup_statcast': [
            {'wOBA': 0.354, 'K_pct': 22.8, 'O_Swing': 26.0}, # Ohtani
            {'wOBA': 0.334, 'K_pct': 13.7, 'O_Swing': 22.0}, # Freeman
            {'wOBA': 0.372, 'K_pct': 22.9, 'O_Swing': 30.0}, # Pages
            {'wOBA': 0.319, 'K_pct': 19.9, 'O_Swing': 24.0}, # Tucker
            {'wOBA': 0.420, 'K_pct': 23.5, 'O_Swing': 27.0}, # Muncy
            {'wOBA': 0.396, 'K_pct': 10.3, 'O_Swing': 21.0}, # Call
            {'wOBA': 0.515, 'K_pct': 26.3, 'O_Swing': 29.0}, # Rushing
            {'wOBA': 0.347, 'K_pct': 17.8, 'O_Swing': 28.0}, # Kim
            {'wOBA': 0.309, 'K_pct': 27.8, 'O_Swing': 32.0}, # Freeland
        ],
        
        # Environmental Factors
        'location': 'LAD',
        'park_factor': 102,
        'is_dome': False,
        'env': {
            'Weather': {
                'temp': 79,
                'wind_speed': 5,
                'wind_dir': 0, # 0 = Blowing out
                'humidity': 45
            },
            'altitude': 267,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Edwin Moscoso', 'zone_type': 'neutral'}
        },
        
        # Bullpen & Defense
        'away_bp_avg_era': 3.85,
        'home_bp_avg_era': 4.10,
        'away_bp_pitches_d1': 45,
        'away_bp_pitches_d2': 20,
        'home_bp_pitches_d1': 30,
        'home_bp_pitches_d2': 15,
        'away_drs': 5,
        'home_drs': -2,
        'away_catcher': 'Sean Murphy',
        'home_catcher': 'Dalton Rushing',
        'away_manager_hook': 0.9, # Standard
        'home_manager_hook': 0.9,
        'game_time': '19:00'
    }
    
    market_odds = {
        'Braves Moneyline': +120,
        'Dodgers Moneyline': -143,
        'Total Over 9.5': 100, # EVEN
        'Total Under 9.5': -120,
        'NRFI (1st Inning No)': 100, # EVEN
        'YRFI (1st Inning Yes)': -130,
        'Justin Wrobleski Under 4.5 K': -165,
        'Justin Wrobleski Over 4.5 K': +125,
        'Bryce Elder Under 4.5 K': -115,
        'Bryce Elder Over 4.5 K': -115,
        'Wrobleski Under 17.5 Outs': -110,
        'Wrobleski Over 17.5 Outs': -130,
        'Elder Under 15.5 Outs': -110,
        'Elder Over 15.5 Outs': -130,
        'Wrobleski Under 1.5 Walks': -150,
        'Wrobleski Over 1.5 Walks': +110,
        'Elder Under 2.5 Walks': -190,
        'Elder Over 2.5 Walks': +145
    }
    
    # Run Omni Simulation
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
    
    if results:
        print("\nSimulation Complete.")

if __name__ == "__main__":
    run_simulation()