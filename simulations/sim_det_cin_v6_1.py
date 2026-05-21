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

# DET Expected Lineup
DET_LINEUP = [
    ('K. McGonigle', 'L'), 
    ('G. Torres', 'R'), 
    ('Colt Keith', 'L'), 
    ('Riley Greene', 'L'), 
    ('D. Dingler', 'R'), 
    ('K. Carpenter', 'L'), 
    ('S. Torkelson', 'R'), 
    ('W. Perez', 'S'), 
    ('Javier Baez', 'R')
]

# CIN Expected Lineup
CIN_LINEUP = [
    ('TJ Friedl', 'L'), 
    ('Matt McLain', 'R'), 
    ('E. De La Cruz', 'S'), 
    ('Sal Stewart', 'R'), 
    ('N. Lowe', 'L'), 
    ('S. Steer', 'R'), 
    ('T. Stephenson', 'R'), 
    ('Rece Hinds', 'R'), 
    ('K. Hayes', 'R')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='DET',
        home_team='CIN',
        away_sp_name='Jack Flaherty',
        home_sp_name='Brady Singer',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.47,
        home_era=5.32,
        away_lineup=DET_LINEUP,
        home_lineup=CIN_LINEUP,
        park_factor=110, # Great American Ball Park
        is_dome=False,
        temp_f=63,
        wind_mph=10,
        wind_ang=180, # Blowing somewhat in from SW
        humidity=65,
        altitude=482,
        rain_intensity=0.0
    )