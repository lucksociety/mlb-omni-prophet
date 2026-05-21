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

PHI_LINEUP = [
    ('Kyle Schwarber', 'L'), ('Trea Turner', 'R'), ('Bryce Harper', 'L'),
    ('Felix Reyes', 'R'), ('Adolis Garcia', 'R'), ('Alec Bohm', 'R'),
    ('Edmundo Sosa', 'R'), ('Brandon Marsh', 'L'), ('Rafael Marchan', 'S')
]

ATL_LINEUP = [
    ('Ronald Acuna', 'R'), ('Drake Baldwin', 'L'), ('Matt Olson', 'L'),
    ('Austin Riley', 'R'), ('Ozzie Albies', 'S'), ('Michael Harris', 'L'),
    ('Dominic Smith', 'L'), ('Mauricio Dubon', 'R'), ('Mike Yastrzemski', 'L')
]

if __name__ == '__main__':
    # Truist Park (ATL)
    # Weather: 77F, Light Wind (5 mph), Humidity 50%, Altitude 1050ft
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='PHI',
        home_team='ATL',
        away_sp_name='Aaron Nola',
        home_sp_name='Chris Sale',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=5.06,
        home_era=2.79,
        away_lineup=PHI_LINEUP,
        home_lineup=ATL_LINEUP,
        park_factor=105,
        is_dome=False,
        temp_f=77,
        wind_mph=5,
        wind_ang=90, # Neutral
        humidity=50,
        altitude=1050,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Aaron Nola (PHI)', a_k)
    print_k_table('Chris Sale (ATL)', h_k)