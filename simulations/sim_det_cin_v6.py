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
from quant_elite_v6_2 import run_v6_2_protocol

# DET @ CIN - April 24, 2026
# DET Away, CIN Home
# DET SP: Framber Valdez (L)
# CIN SP: Andrew Abbott (L)

DET_LINEUP = [
    ('Jahmai Jones', 'R'),
    ('Gleyber Torres', 'R'),
    ('Kevin McGonigle', 'L'),
    ('Matt Vierling', 'R'),
    ('Dillon Dingler', 'R'),
    ('Riley Greene', 'L'),
    ('Spencer Torkelson', 'R'),
    ('Hao-Yu Lee', 'R'),
    ('Javier Baez', 'R')
]

CIN_LINEUP = [
    ('Dane Myers', 'R'),
    ('Matt McLain', 'R'),
    ('Elly De La Cruz', 'S'),
    ('Sal Stewart', 'R'),
    ('Eugenio Suarez', 'R'),
    ('Spencer Steer', 'R'),
    ('Tyler Stephenson', 'R'),
    ('Rece Hinds', 'R'),
    ('Ke\'Bryan Hayes', 'R')
]

# Environmental Data
# Temp: 81F, Wind: 10mph Right-to-Left (90deg), Park Factor: 122 (GABP)
# is_dome = False

if __name__ == '__main__':
    run_v6_2_protocol(
        away_team='DET',
        home_team='CIN',
        away_sp_name='Framber Valdez',
        home_sp_name='Andrew Abbott',
        away_sp_hand='L',
        home_sp_hand='L',
        away_era=3.30,
        home_era=5.84,
        away_lineup=DET_LINEUP,
        home_lineup=CIN_LINEUP,
        park_factor=122,
        is_dome=False,
        temp_f=81,
        wind_mph=10,
        wind_ang=90, # R-to-L across field
        humidity=50,
        altitude=0,
        rain_intensity=0.0
    )