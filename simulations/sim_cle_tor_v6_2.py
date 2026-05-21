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

CLE_LINEUP = [
    ('Steven Kwan', 'L'), ('Angel Martinez', 'S'), ('Jose Ramirez', 'S'),
    ('Rhys Hoskins', 'R'), ('David Fry', 'R'), ('Daniel Schneemann', 'L'),
    ('Juan Brito', 'S'), ('Austin Hedges', 'R'), ('Brayan Rocchio', 'S')
]

TOR_LINEUP = [
    ('Myles Straw', 'R'), ('Ernie Clement', 'R'), ('Vladimir Guerrero Jr.', 'R'),
    ('Jesus Sanchez', 'L'), ('Eloy Jimenez', 'R'), ('Daulton Varsho', 'L'),
    ('K. Okamoto', 'R'), ('Andres Gimenez', 'L'), ('Tyler Heineman', 'S')
]

if __name__ == '__main__':
    # Rogers Centre (TOR)
    # Weather: Dome CLOSED (54F outside)
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='CLE',
        home_team='TOR',
        away_sp_name='Slade Cecconi',
        home_sp_name='Patrick Corbin',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=6.20,
        home_era=3.68,
        away_lineup=CLE_LINEUP,
        home_lineup=TOR_LINEUP,
        park_factor=102,
        is_dome=True,
        temp_f=72, # Standard dome temp
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=250,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Slade Cecconi (CLE)', a_k)
    print_k_table('Patrick Corbin (TOR)', h_k)