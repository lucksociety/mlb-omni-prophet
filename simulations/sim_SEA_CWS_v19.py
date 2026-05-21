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

import os
import statistics
from datetime import datetime

from omni_prophet_v16 import OmniProphetV18

def run_sea_cws_sim():
    # SEA Lineup Data (May 10, 2026) - Confirmed Lineup
    # 6L, 1S, 2R — heavy left-handed lineup vs RHP Davis Martin
    away_lineup = [
        {'Name': 'Brendan Donovan', 'Hand': 'L', 'K_pct': 16.9, 'O_Swing': 24.0, 'Z_Contact': 89.0, 'wOBA': 0.407},   # .346 OBP, .437 OBP pre-injury, elite plate discipline
        {'Name': 'Julio Rodriguez', 'Hand': 'R', 'K_pct': 16.7, 'O_Swing': 29.0, 'Z_Contact': 85.0, 'wOBA': 0.335},    # .272/.339/.430, 29 K in 158 AB = ~16.7%
        {'Name': 'Josh Naylor', 'Hand': 'L', 'K_pct': 18.0, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.270},        # .233 AVG, .645 OPS, grinding thru quad tightness — sub-.600 OPS reference
        {'Name': 'Cal Raleigh', 'Hand': 'S', 'K_pct': 30.6, 'O_Swing': 34.0, 'Z_Contact': 76.0, 'wOBA': 0.267},        # 30.6 K%, struggling offensively
        {'Name': 'Randy Arozarena', 'Hand': 'R', 'K_pct': 21.5, 'O_Swing': 30.0, 'Z_Contact': 83.0, 'wOBA': 0.362},    # Solid, .354-.371 wOBA range
        {'Name': 'Luke Raley', 'Hand': 'L', 'K_pct': 25.5, 'O_Swing': 32.0, 'Z_Contact': 80.0, 'wOBA': 0.415},         # Hot bat, .380-.451 wOBA range
        {'Name': 'JP Crawford', 'Hand': 'L', 'K_pct': 18.5, 'O_Swing': 26.0, 'Z_Contact': 87.0, 'wOBA': 0.342},        # .342 wOBA, contact-oriented
        {'Name': 'Dominic Canzone', 'Hand': 'L', 'K_pct': 21.2, 'O_Swing': 29.0, 'Z_Contact': 84.0, 'wOBA': 0.340},    # .329-.352 wOBA range
        {'Name': 'Cole Young', 'Hand': 'L', 'K_pct': 15.0, 'O_Swing': 23.0, 'Z_Contact': 90.0, 'wOBA': 0.334},         # .266 AVG, elite plate discipline for 22yo, top AL 2B
    ]
    
    # CWS Lineup Data (May 10, 2026) - Confirmed Lineup
    # 5L, 1S, 3R — Murakami the gravitational center
    home_lineup = [
        {'Name': 'Sam Antonacci', 'Hand': 'L', 'K_pct': 20.0, 'O_Swing': 28.0, 'Z_Contact': 84.0, 'wOBA': 0.340},     # .277 AVG, .800 OPS, ~.340 wOBA estimate — rookie with 21 games
        {'Name': 'Munetaka Murakami', 'Hand': 'L', 'K_pct': 34.4, 'O_Swing': 36.0, 'Z_Contact': 72.0, 'wOBA': 0.420},  # .237 AVG, .703 SLG, 15 HR in 38G, 22.1% barrel rate — ELITE power
        {'Name': 'Miguel Vargas', 'Hand': 'R', 'K_pct': 18.9, 'O_Swing': 29.0, 'Z_Contact': 85.0, 'wOBA': 0.351},      # 3 HR in last 7 games, hot streak
        {'Name': 'Colson Montgomery', 'Hand': 'L', 'K_pct': 28.8, 'O_Swing': 32.0, 'Z_Contact': 78.0, 'wOBA': 0.360},  # .360 wOBA, 28.8 K% — high-upside young SS
        {'Name': 'Chase Meidroth', 'Hand': 'R', 'K_pct': 24.8, 'O_Swing': 30.0, 'Z_Contact': 82.0, 'wOBA': 0.331},     # 2B, solid contact
        {'Name': 'Jarred Kelenic', 'Hand': 'L', 'K_pct': 12.0, 'O_Swing': 25.0, 'Z_Contact': 88.0, 'wOBA': 0.329},     # 12% K rate — massive K rate improvement, facing former team
        {'Name': 'Tristan Peters', 'Hand': 'L', 'K_pct': 23.7, 'O_Swing': 31.0, 'Z_Contact': 81.0, 'wOBA': 0.297},     # CF, below-avg bat
        {'Name': 'Randal Grichuk', 'Hand': 'R', 'K_pct': 25.6, 'O_Swing': 35.0, 'Z_Contact': 78.0, 'wOBA': 0.272},     # DH, limited PA, vet presence but declining
        {'Name': 'Drew Romo', 'Hand': 'S', 'K_pct': 20.7, 'O_Swing': 28.0, 'Z_Contact': 84.0, 'wOBA': 0.534},          # .534 wOBA — SMALL SAMPLE ALERT, likely to regress
    ]

    game_data = {
        'away_team': 'SEA',
        'home_team': 'CWS',
        'away_sp_name': 'Logan Gilbert',
        'home_sp_name': 'Davis Martin',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': 4.30,
        'home_sp_era': 1.64,
        'away_sp_statcast': {
            'Name': 'Logan Gilbert',
            'Hand': 'R',
            'Stuff': 108,       # Gilbert has elite Stuff+ — historically top-tier arsenal (slider/splitter)
            'K_pct': 23.2,      # 2026: 23.2% K rate — 43 K in 44.0 IP
            'BB_pct': 5.4,      # 2026: 5.4% BB rate — still elite walk rate
            'VAA': -4.2,        # Elite vertical approach angle on fastball
            'IP': 44.0,         # 8 starts, 44.0 IP — established veteran
            'Starts': 8,
            'ERA': 4.30,
            'xERA': 3.85,       # xFIP-based estimate — ERA likely inflated by HR/FB variance
            'HR/FB%': 14.0,     # Elevated HR/FB% driving ERA up
            'LastPitchCount': 95  # Full-game workload expected
        },
        'home_sp_statcast': {
            'Name': 'Davis Martin',
            'Hand': 'R',
            'Stuff': 97,        # Martin is NOT an overpowering arm — command/tunneling pitcher. Below 100 Stuff+
            'K_pct': 25.4,      # 2026: 25.4% K rate — 43 K in 44.0 IP (identical K total to Gilbert)
            'BB_pct': 4.7,      # 2026: 4.7% BB rate — elite command
            'VAA': -4.5,
            'IP': 44.0,         # 8 starts, 44.0 IP — established for 2026
            'Starts': 8,        # NOT a rookie — TJ recovery but has MLB experience
            'ERA': 1.64,
            'xERA': 2.65,       # FIP 2.45, but xERA likely higher due to BABIP regression pending
            'HR/FB%': 6.0,      # Unsustainably low HR/FB% — BABIP/HR regression signal
            'LastPitchCount': 95  # Full game workload
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'away_lineup_k_pct': statistics.mean([b['K_pct'] for b in away_lineup]),
        'home_lineup_k_pct': statistics.mean([b['K_pct'] for b in home_lineup]),
        'park_factor': 103,     # Rate Field: HR-friendly but neutral overall. 103 is fair composite.
        'is_dome': False,
        'away_drs': 2,          # SEA is solid defensively
        'home_drs': -2,         # CWS below-average defense, young lineup
        'away_manager_hook': 0,
        'home_manager_hook': 0,
        'away_bp_pitches_d1': 15,
        'away_bp_pitches_d2': 10,
        'home_bp_pitches_d1': 15,
        'home_bp_pitches_d2': 10,
        'away_catcher': 'Cal Raleigh',    # Elite framer
        'home_catcher': 'Drew Romo',
        'game_time_decimal': 14.17,  # 2:10 PM ET
        'game_time': '14:10',
        'location': 'CWS',
        'away_bp_avg_era': 3.75,  # SEA bullpen — strong
        'home_bp_avg_era': 4.40,  # CWS bullpen — below avg
        'env': {
            'Weather': {
                'temp': 57,           # 57°F — cooler, slightly suppresses fly balls
                'wind_speed': 10,     # 10 mph wind blowing Left-to-Right — cross wind
                'wind_dir': 90,       # Left to Right = cross field (90 degrees)
                'humidity': 50
            },
            'altitude': 597,          # Chicago elevation
            'rain_intensity': 0.0,    # 0% precip chance
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}  # Umpire not announced
        }
    }

    market_odds = {
        'SEA Moneyline': -141,
        'CWS Moneyline': 110,
        'Total Over 8.0': -110,
        'Total Under 8.0': -110,
        'Logan Gilbert Over 5.5 K': -120,
        'Logan Gilbert Under 5.5 K': -100,
        'Davis Martin Over 5.5 K': -115,
        'Davis Martin Under 5.5 K': -105
    }

    omni = OmniProphetV18()
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_sea_cws_sim()