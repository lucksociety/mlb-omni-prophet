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

# CLE Confirmed Lineup
CLE_LINEUP = [
    ('A. Martinez', 'S'), 
    ('C. DeLauter', 'L'), 
    ('Jose Ramirez', 'S'), 
    ('Rhys Hoskins', 'R'), 
    ('G. Valera', 'L'), 
    ('David Fry', 'R'), 
    ('Juan Brito', 'S'), 
    ('Bo Naylor', 'L'), 
    ('B. Rocchio', 'S')
]

# TOR Confirmed Lineup
TOR_LINEUP = [
    ('Myles Straw', 'R'), 
    ('E. Clement', 'R'), 
    ('V. Guerrero', 'R'), 
    ('K. Okamoto', 'R'), 
    ('Eloy Jimenez', 'R'), 
    ('D. Varsho', 'L'), 
    ('D. Schneider', 'R'), 
    ('A. Gimenez', 'L'), 
    ('T. Heineman', 'S')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='CLE',
        home_team='TOR',
        away_sp_name='Joey Cantillo',
        home_sp_name='Kevin Gausman',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=3.20,
        home_era=2.54,
        away_lineup=CLE_LINEUP,
        home_lineup=TOR_LINEUP,
        park_factor=101, # Rogers Centre
        is_dome=True, # Roof Closed
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=249,
        rain_intensity=0.0
    )