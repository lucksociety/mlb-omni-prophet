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

COL_LINEUP = [
    ('Edouard Julien', 'L'), ('Mickey Moniak', 'L'), ('Hunter Goodman', 'R'),
    ('TJ Rumfield', 'L'), ('Troy Johnston', 'L'), ('Ezequiel Tovar', 'R'),
    ('Kyle Karros', 'R'), ('Willi Castro', 'S'), ('Brenton Doyle', 'R')
]

NYM_LINEUP = [
    ('Bo Bichette', 'R'), ('Juan Soto', 'L'), ('Francisco Alvarez', 'R'),
    ('Luis Robert Jr.', 'R'), ('Brett Baty', 'L'), ('Mark Vientos', 'R'),
    ('Marcus Semien', 'R'), ('Ronny Mauricio', 'S'), ('Carson Benge', 'L')
]

if __name__ == '__main__':
    # Citi Field (NYM)
    # Weather: 73F, Wind NE 10 mph (Across from RF), Humidity 60%, Altitude 0ft
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='COL',
        home_team='NYM',
        away_sp_name='Jose Quintana',
        home_sp_name='Nolan McLean',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=6.23,
        home_era=2.67,
        away_lineup=COL_LINEUP,
        home_lineup=NYM_LINEUP,
        park_factor=96,
        is_dome=False,
        temp_f=73,
        wind_mph=10,
        wind_ang=135, # Blowing across from RF
        humidity=60,
        altitude=0,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Jose Quintana (COL)', a_k)
    print_k_table('Nolan McLean (NYM)', h_k)