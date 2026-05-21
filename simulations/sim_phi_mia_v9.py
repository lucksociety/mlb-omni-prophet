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

from quant_elite_v9 import run_v9_protocol, ARCHETYPES

# Update Archetypes for the audit
ARCHETYPES['Andrew Painter'] = 'North-South'
ARCHETYPES['Max Meyer'] = 'Unicorn'

AWAY_LINEUP = [
    ('Trea Turner', 'R'), ('K. Schwarber', 'L'), ('Bryce Harper', 'L'),
    ('A. Garcia', 'R'), ('B. Marsh', 'L'), ('Bryson Stott', 'L'),
    ('Alec Bohm', 'R'), ('J. Crawford', 'L'), ('R. Marchan', 'S'),
]

HOME_LINEUP = [
    ('Jakob Marsee', 'L'), ('Kyle Stowers', 'L'), ('Otto Lopez', 'R'),
    ('X. Edwards', 'S'), ('Liam Hicks', 'L'), ('A. Ramirez', 'R'),
    ('Owen Caissie', 'L'), ('G. Pauley', 'L'), ('Connor Norby', 'R'),
]

if __name__ == '__main__':
    run_v9_protocol(
        away_team='PHI',
        home_team='MIA',
        away_sp_name='Andrew Painter',
        home_sp_name='Max Meyer',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=5.25,
        home_era=4.66,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=97,
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=0,
        rain_intensity=0.0,
        away_drs=3,
        home_drs=5,
        away_manager_hook=0.2,
        home_manager_hook=0.0,
        away_bp_pitches_d1=40, # Bowlan/Alvarado/Keller
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=25, # Gibson
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='Rafael Marchan',
        home_catcher='Liam Hicks',
        game_time='16:10',
        is_game_1=False
    )