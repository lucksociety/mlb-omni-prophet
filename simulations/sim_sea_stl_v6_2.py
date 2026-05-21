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

SEA_LINEUP = [
    ('J.P. Crawford', 'L'), ('Cal Raleigh', 'S'), ('Julio Rodriguez', 'R'),
    ('Josh Naylor', 'L'), ('Randy Arozarena', 'R'), ('Luke Raley', 'L'),
    ('Dominic Canzone', 'L'), ('Cole Young', 'L'), ('Leo Rivas', 'S')
]

STL_LINEUP = [
    ('J.J. Wetherholt', 'L'), ('Ivan Herrera', 'R'), ('Alec Burleson', 'L'),
    ('Jordan Walker', 'R'), ('Nolan Gorman', 'L'), ('Masyn Winn', 'R'),
    ('Nathan Church', 'L'), ('Pedro Pages', 'R'), ('Victor Scott II', 'L')
]

if __name__ == '__main__':
    # Busch Stadium (STL)
    # Weather: 76F, Wind 10 mph Out to Left, Humidity 55%, Altitude 450ft
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='SEA',
        home_team='STL',
        away_sp_name='Emerson Hancock',
        home_sp_name='Michael McGreevy',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.83,
        home_era=3.29,
        away_lineup=SEA_LINEUP,
        home_lineup=STL_LINEUP,
        park_factor=98,
        is_dome=False,
        temp_f=76,
        wind_mph=10,
        wind_ang=315, # Blowing out to Left
        humidity=55,
        altitude=450,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Emerson Hancock (SEA)', a_k)
    print_k_table('Michael McGreevy (STL)', h_k)