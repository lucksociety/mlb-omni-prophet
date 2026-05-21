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
    ('Nico Hoerner', 'R'),
    ('Moises Ballesteros', 'L'),
    ('Alex Bregman', 'R'),
    ('Ian Happ', 'S'),
    ('Michael Busch', 'L'),
    ('Michael Conforto', 'L'),
    ('Matt Shaw', 'R'),
    ('Pete Crow-Armstrong', 'L'),
    ('Miguel Amaya', 'R')
]

HOME_LINEUP = [
    ('Jackson Merrill', 'L'),
    ('Fernando Tatis Jr.', 'R'),
    ('Manny Machado', 'R'),
    ('Xander Bogaerts', 'R'),
    ('Ty France', 'R'),
    ('Miguel Andujar', 'R'),
    ('Jake Cronenworth', 'L'),
    ('Nick Castellanos', 'R'),
    ('Luis Campusano', 'R')
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='CHC',
        home_team='SD',
        away_sp_name='Jameson Taillon',
        home_sp_name='Matt Waldron',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=4.55,
        home_era=12.46,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=96,      # Petco Park (Pitcher Friendly)
        is_dome=False,
        temp_f=68,
        wind_mph=8,
        wind_ang=45,         # Cross/In
        humidity=65,
        altitude=20,
        rain_intensity=0.0,
        away_drs=4,          # CHC solid D
        home_drs=6,          # SD elite D
        away_manager_hook=-0.5, # CHC quick to bullpen
        home_manager_hook=-1.0, # Waldron on short leash with 12.46 ERA
        away_bp_pitches_d1=10,
        away_bp_pitches_d2=5,
        home_bp_pitches_d1=20,
        home_bp_pitches_d2=25, # SD bullpen a bit tired
        umpire_zone='neutral'
    )