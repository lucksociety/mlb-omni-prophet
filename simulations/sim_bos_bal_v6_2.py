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

BOS_LINEUP = [
    ('Roman Anthony', 'L'), ('William Contreras', 'R'), ('Wilyer Abreu', 'L'),
    ('Trevor Story', 'R'), ('Jarren Duran', 'L'), ('Ceddanne Rafaela', 'R'),
    ('Marcelo Mayer', 'L'), ('Caleb Durbin', 'R'), ('Carlos Narvaez', 'R')
]

BAL_LINEUP = [
    ('Taylor Ward', 'R'), ('Gunnar Henderson', 'L'), ('Adley Rutschman', 'S'),
    ('Pete Alonso', 'R'), ('Jace Jackson', 'R'), ('Weston Wilson', 'R'),
    ('Leody Taveras', 'S'), ('Coby Mayo', 'R'), ('Blaze Alexander', 'R')
]

if __name__ == '__main__':
    # Camden Yards (BAL)
    # Weather: 59F, NE 12 mph (Blowing In/Across), High Humidity (70%)
    # NE wind at Camden (CF faces NNE) is a strong headwind/crosswind.
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='BOS',
        home_team='BAL',
        away_sp_name='Connelly Early',
        home_sp_name='Kyle Bradish',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=2.88,
        home_era=3.96,
        away_lineup=BOS_LINEUP,
        home_lineup=BAL_LINEUP,
        park_factor=101,
        is_dome=False,
        temp_f=59,
        wind_mph=12,
        wind_ang=180, # Blowing in from CF
        humidity=70,
        altitude=30,
        rain_intensity=0.1
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Connelly Early (BOS)', a_k)
    print_k_table('Kyle Bradish (BAL)', h_k)