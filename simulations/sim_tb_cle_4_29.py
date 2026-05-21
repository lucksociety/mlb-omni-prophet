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

from quant_elite_v6_4 import run_v6_4_protocol

AWAY_LINEUP = [
    ('Chandler Simpson', 'L'), ('Junior Caminero', 'R'), ('Jonathan Aranda', 'L'),
    ('Yandy Diaz', 'R'), ('Jake Fraley', 'L'), ('Cedric Mullins', 'L'),
    ('Richie Palacios', 'L'), ('Hunter Feduccia', 'L'), ('Taylor Walls', 'S')
]

HOME_LINEUP = [
    ('Steven Kwan', 'L'), ('Chase DeLauter', 'L'), ('Jose Ramirez', 'S'),
    ('Kyle Manzardo', 'L'), ('Daniel Schneemann', 'L'), ('Angel Martinez', 'S'),
    ('Travis Bazzana', 'L'), ('Bo Naylor', 'L'), ('Brayan Rocchio', 'S')
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='TBR',
        home_team='CLE',
        away_sp_name='Drew Rasmussen',
        home_sp_name='Gavin Williams',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.45,
        home_era=3.28,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=95,
        is_dome=False,
        temp_f=56,
        wind_mph=11,
        wind_ang=45, # Diagonal
        humidity=65,
        altitude=600,
        rain_intensity=0.2, # Light rain/risk
        away_drs=2,
        home_drs=4,
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=10,
        away_bp_pitches_d2=5,
        home_bp_pitches_d1=15,
        home_bp_pitches_d2=0,
        umpire_zone='neutral'
    )