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

ATH_LINEUP = [
    ('Nick Kurtz', 'L'), ('Shea Langeliers', 'R'), ('Carlos Cortes', 'L'),
    ('Tyler Soderstrom', 'L'), ('Jacob Wilson', 'R'), ('Jeff McNeil', 'L'),
    ('Max Muncy', 'R'), ('Lawrence Butler', 'L'), ('Zack Gelof', 'R')
]

TEX_LINEUP = [
    ('Brandon Nimmo', 'L'), ('Corey Seager', 'L'), ('Jake Burger', 'R'),
    ('Joc Pederson', 'L'), ('Josh Jung', 'R'), ('Evan Carter', 'L'),
    ('Kyle Higashioka', 'R'), ('Josh Smith', 'L'), ('Alejandro Osuna', 'L')
]

if __name__ == '__main__':
    # Globe Life Field (TEX)
    # Weather: Roof CLOSED
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='ATH',
        home_team='TEX',
        away_sp_name='J.T. Ginn',
        home_sp_name='Kumar Rocker',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.74,
        home_era=3.48,
        away_lineup=ATH_LINEUP,
        home_lineup=TEX_LINEUP,
        park_factor=98,
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=600,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('J.T. Ginn (ATH)', a_k)
    print_k_table('Kumar Rocker (TEX)', h_k)