
import sys, os
sys.path.append("/Users/danielreiss/Desktop/Antigravity/MLB")
from omni_prophet_v16 import OmniProphetV16

# ── RESEARCHED GAME DATA (TEX @ NYY | 2026-05-07) ──────────────────
game_data = {
    'away_team': 'TEX',
    'home_team': 'NYY',
    'away_sp_name': 'MacKenzie Gore',
    'away_sp_hand': 'L',
    'away_sp_era': 4.67,
    'away_sp_statcast': {
        'Stuff': 115,
        'VAA': -4.0, # North-South
        'K_pct': 31.6,
        'BB_pct': 11.3,
        'IP': 34.2,
        'xERA': 3.22,
        'CSW_L3': 29.8,
        'SwStr_L3': 13.8
    },
    'home_sp_name': 'Paul Blackburn',
    'home_sp_hand': 'R',
    'home_sp_era': 3.21,
    'home_sp_statcast': {
        'Stuff': 98,
        'VAA': -4.8, # East-West / Sinker
        'K_pct': 14.3,
        'BB_pct': 6.1,
        'IP': 14.0,
        'xERA': 4.25,
        'CSW_L3': 24.2,
        'SwStr_L3': 8.2
    },
    'away_lineup_names': [
        'B. Nimmo', 'E. Duran', 'Corey Seager', 
        'Josh Jung', 'Joc Pederson', 'Jake Burger', 
        'Evan Carter', 'Danny Jansen', 'J. Foscue'
    ],
    'away_lineup_hands': ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'R'],
    'away_lineup_statcast': [
        {'K_pct': 19.7, 'O_Swing': 28.0, 'Z_Contact': 85.0}, # Nimmo
        {'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 80.0}, # Duran
        {'K_pct': 25.6, 'O_Swing': 30.0, 'Z_Contact': 82.0}, # Seager
        {'K_pct': 16.3, 'O_Swing': 31.0, 'Z_Contact': 84.0}, # Jung
        {'K_pct': 25.3, 'O_Swing': 25.0, 'Z_Contact': 80.0}, # Pederson
        {'K_pct': 29.8, 'O_Swing': 35.0, 'Z_Contact': 78.0}, # Burger
        {'K_pct': 24.0, 'O_Swing': 28.0, 'Z_Contact': 83.0}, # Carter
        {'K_pct': 22.0, 'O_Swing': 26.0, 'Z_Contact': 84.0}, # Jansen
        {'K_pct': 20.0, 'O_Swing': 28.0, 'Z_Contact': 85.0}, # Foscue
    ],
    'home_lineup_names': [
        'P. Goldschmidt', 'Aaron Judge', 'C. Bellinger', 
        'Amed Rosario', 'J. Chisholm', 'J. Dominguez', 
        'T. Grisham', 'M. Schuemann', 'J.C. Escarra'
    ],
    'home_lineup_hands': ['R', 'R', 'L', 'R', 'L', 'S', 'L', 'R', 'L'],
    'home_lineup_statcast': [
        {'K_pct': 22.0, 'O_Swing': 26.0, 'Z_Contact': 84.0}, # Goldschmidt
        {'K_pct': 26.8, 'O_Swing': 25.0, 'Z_Contact': 78.0}, # Judge
        {'K_pct': 13.3, 'O_Swing': 28.0, 'Z_Contact': 86.0}, # Bellinger
        {'K_pct': 10.0, 'O_Swing': 30.0, 'Z_Contact': 88.0}, # Rosario
        {'K_pct': 29.2, 'O_Swing': 29.0, 'Z_Contact': 82.0}, # Chisholm
        {'K_pct': 22.0, 'O_Swing': 26.0, 'Z_Contact': 83.0}, # Dominguez
        {'K_pct': 18.9, 'O_Swing': 22.0, 'Z_Contact': 84.0}, # Grisham
        {'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 80.0}, # Schuemann
        {'K_pct': 25.0, 'O_Swing': 28.0, 'Z_Contact': 82.0}, # Escarra
    ],
    'env': {
        'Weather': {
            'temp': 60.0,
            'wind_speed': 9.0,
            'wind_dir': 45.0, # Blowing toward RF "Short Porch"
            'humidity': 45.0
        },
        'Umpire': {
            'name': 'TBD',
            'CS_pct': 16.0,
            'zone_type': 'neutral'
        },
        'altitude': 54.0, # Yankee Stadium elevation
        'rain_intensity': 0.02 # 2% precipitation
    },
    'park_factor': 105,
    'is_dome': False,
    'away_catcher': 'Danny Jansen',
    'home_catcher': 'J.C. Escarra', # Spot start at catcher?
    'game_time': '12:35',
    'away_drs': 2,
    'home_drs': 5,
    'away_manager_hook': 0.2, # Gore can be high stress
    'home_manager_hook': -0.1, # Blackburn is spot starter, maybe shorter leash?
    'away_bp_pitches_d1': 35,
    'away_bp_pitches_d2': 20,
    'home_bp_pitches_d1': 25,
    'home_bp_pitches_d2': 40
}

market_odds = {
    'NYY Moneyline': -158,
    'TEX Moneyline': 135,
    'Total Over 8.5': -110,
    'Total Under 8.5': -110
}

# ── EXECUTION ─────────────────────────────────────────────────────
omni = OmniProphetV16()
omni.run_omni_simulation(game_data, market_odds=market_odds)
