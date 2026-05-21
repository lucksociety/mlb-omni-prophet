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

DET_LINEUP = [
    ('Kevin McGonigle', 'L'), ('Gleyber Torres', 'R'), ('Colt Keith', 'L'),
    ('Riley Greene', 'L'), ('Spencer Torkelson', 'R'), ('Kerry Carpenter', 'L'),
    ('Matt Vierling', 'R'), ('Wenceel Perez', 'S'), ('Jake Rogers', 'R')
]

CIN_LINEUP = [
    ('TJ Friedl', 'L'), ('Matt McLain', 'R'), ('Elly De La Cruz', 'S'),
    ('Sal Stewart', 'R'), ('Nathaniel Lowe', 'L'), ('Spencer Steer', 'R'),
    ('JJ Bleday', 'L'), ('Jose Trevino', 'R'), ('Ke\'Bryan Hayes', 'R')
]

if __name__ == '__main__':
    # Great American Ball Park (CIN)
    # Weather: 61F, Overcast, Wind 8 mph out to RF, Humidity 70%, Altitude 500ft
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='DET',
        home_team='CIN',
        away_sp_name='Keider Montero',
        home_sp_name='Rhett Lowder',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.68,
        home_era=3.10,
        away_lineup=DET_LINEUP,
        home_lineup=CIN_LINEUP,
        park_factor=110,
        is_dome=False,
        temp_f=61,
        wind_mph=8,
        wind_ang=45, # Blowing out to RF
        humidity=70,
        altitude=500,
        rain_intensity=0.2
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Keider Montero (DET)', a_k)
    print_k_table('Rhett Lowder (CIN)', h_k)