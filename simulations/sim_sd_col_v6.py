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

from quant_elite_v6_2 import run_v6_2_protocol

AWAY_LINEUP = [
    ('R. Laureano', 'R'), ('F. Tatis', 'R'), ('J. Merrill', 'L'),
    ('M. Machado', 'R'), ('X. Bogaerts', 'R'), ('Gavin Sheets', 'L'),
    ('M. Andujar', 'R'), ('F. Fermin', 'R'), ('J. Cronenworth', 'L'),
]

HOME_LINEUP = [
    ('E. Julien', 'L'), ('M. Moniak', 'L'), ('H. Goodman', 'R'),
    ('TJ Rumfield', 'L'), ('T. Johnston', 'L'), ('E. Tovar', 'R'),
    ('Kyle Karros', 'R'), ('Willi Castro', 'S'), ('B. Doyle', 'R'),
]

if __name__ == '__main__':
    run_v6_2_protocol(
        away_team='SD',
        home_team='COL',
        away_sp_name='Matt Waldron',
        home_sp_name='Ryan Feltner',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=14.73,
        home_era=6.00,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=115, # Coors Field
        is_dome=False,
        temp_f=55,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=0,
        rain_intensity=0.0
    )