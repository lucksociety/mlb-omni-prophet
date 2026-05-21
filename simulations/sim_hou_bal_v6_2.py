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

def run_sim():
    # HOU Lineup from screenshot
    hou_lineup = [
        ('C. Correa', 'R'),
        ('Y. Alvarez', 'L'),
        ('I. Paredes', 'R'),
        ('Jose Altuve', 'R'),
        ('C. Walker', 'R'),
        ('Cam Smith', 'R'),
        ('D. Harris', 'L'),
        ('Yainer Diaz', 'R'),
        ('B. Matthews', 'R')
    ]
    
    # BAL Lineup from screenshot
    bal_lineup = [
        ('G. Henderson', 'L'),
        ('Taylor Ward', 'R'),
        ('A. Rutschman', 'S'),
        ('Pete Alonso', 'R'),
        ('D. Beavers', 'L'),
        ('S. Basallo', 'L'),
        ('L. Taveras', 'S'),
        ('Coby Mayo', 'R'),
        ('J. Jackson', 'R')
    ]
    
    # Game 2: HOU @ BAL
    # HOU SP: Kai-Wei Teng (R), 2.16 ERA
    # BAL SP: Shane Baz (R), 5.08 ERA
    # Weather: Assuming 68F, 5mph (Camden Yards)
    
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='HOU',
        home_team='BAL',
        away_sp_name='Kai-Wei Teng',
        home_sp_name='Shane Baz',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.16,
        home_era=5.08,
        away_lineup=hou_lineup,
        home_lineup=bal_lineup,
        park_factor=104, # Camden Yards
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=30,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Kai-Wei Teng (HOU)', a_k)
    print_k_table('Shane Baz (BAL)', h_k)

if __name__ == '__main__':
    run_sim()