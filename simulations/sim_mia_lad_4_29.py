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
    ('Jakob Marsee', 'L'),
    ('Kyle Stowers', 'L'),
    ('Otto Lopez', 'R'),
    ('Xavier Edwards', 'S'),
    ('Liam Hicks', 'L'),
    ('Connor Norby', 'R'),
    ('Owen Caissie', 'L'),
    ('Graham Pauley', 'L'),
    ('Esteury Ruiz', 'R')
]

HOME_LINEUP = [
    ('Shohei Ohtani', 'L'),
    ('Freddie Freeman', 'L'),
    ('Andy Pages', 'R'),
    ('Kyle Tucker', 'L'),
    ('Max Muncy', 'L'),
    ('Dalton Rushing', 'L'),
    ('Hyeseong Kim', 'L'),
    ('Alex Call', 'R'),
    ('Alex Freeland', 'S')
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='MIA',
        home_team='LAD',
        away_sp_name='Sandy Alcantara',
        home_sp_name='Tyler Glasnow',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.05,
        home_era=2.45,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=100,
        is_dome=False,
        temp_f=70,
        wind_mph=4,
        wind_ang=90,
        humidity=45,
        altitude=250,
        rain_intensity=0.0,
        away_drs=5,          # Alcantara gets good D support
        home_drs=3,          
        away_manager_hook=0.5,  # Sandy stays in long
        home_manager_hook=0.0,
        away_bp_pitches_d1=15,
        away_bp_pitches_d2=10,
        home_bp_pitches_d1=20,
        home_bp_pitches_d2=5,
        umpire_zone='neutral'
    )