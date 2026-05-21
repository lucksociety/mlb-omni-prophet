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

from quant_elite_v6_1 import run_v6_1_protocol

# SEA Confirmed Lineup
SEA_LINEUP = [
    ('R. Refsnyder', 'R'), 
    ('Cal Raleigh', 'S'), 
    ('J. Rodriguez', 'R'), 
    ('Josh Naylor', 'L'), 
    ('R. Arozarena', 'R'), 
    ('J. Crawford', 'L'), 
    ('Mitch Garver', 'R'), 
    ('Cole Young', 'L'), 
    ('Will Wilson', 'R')
]

# STL Confirmed Lineup
STL_LINEUP = [
    ('J. Wetherholt', 'L'), 
    ('Ivan Herrera', 'R'), 
    ('A. Burleson', 'L'), 
    ('J. Walker', 'R'), 
    ('Nolan Gorman', 'L'), 
    ('Masyn Winn', 'R'), 
    ('N. Church', 'L'), 
    ('Pedro Pages', 'R'), 
    ('Victor Scott', 'L')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='SEA',
        home_team='STL',
        away_sp_name='Bryan Woo',
        home_sp_name='M. Liberatore',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=2.25,
        home_era=3.67,
        away_lineup=SEA_LINEUP,
        home_lineup=STL_LINEUP,
        park_factor=98, # Busch Stadium is pitcher friendly
        is_dome=False,
        temp_f=73,
        wind_mph=10,
        wind_ang=180, # Blowing in from center
        humidity=46,
        altitude=466,
        rain_intensity=0.0
    )