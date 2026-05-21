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
    ('Ronald Acuna', 'R'), ('D. Baldwin', 'L'), ('Matt Olson', 'L'),
    ('Austin Riley', 'R'), ('Ozzie Albies', 'S'), ('M. Harris', 'L'),
    ('D. Smith', 'L'), ('M. Dubon', 'R'), ('M. Yastrzemski', 'L'),
]

HOME_LINEUP = [
    ('James Wood', 'L'), ('Luis Garcia', 'L'), ('Jose Tena', 'L'),
    ('CJ Abrams', 'L'), ('Jacob Young', 'R'), ('Daylen Lile', 'L'),
    ('Nasim Nunez', 'S'), ('Jorbit Vivas', 'L'), ('Keibert Ruiz', 'S'),
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='ATL',
        home_team='WSH',
        away_sp_name='JR Ritchie',
        home_sp_name='Cade Cavalli',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=0.00,
        home_era=4.12,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=101,
        is_dome=False,
        temp_f=69,
        wind_mph=13,
        wind_ang=90,
        humidity=50,
        altitude=0,
        rain_intensity=0.0,
        away_drs=8,          # Elite defense dampens WSH runs
        home_drs=-2,         # Poor defense boosts ATL runs
        away_manager_hook=0.5,  # ATL let starters go longer
        home_manager_hook=-0.5, # WSH pulls early
        away_bp_pitches_d1=35, # Tired bullpen
        away_bp_pitches_d2=20,
        home_bp_pitches_d1=10, # Fresh bullpen
        home_bp_pitches_d2=15,
        umpire_zone='tight'    # High walks, low Ks
    )