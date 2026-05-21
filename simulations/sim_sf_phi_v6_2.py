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
    # SF Lineup from screenshot
    sf_lineup = [
        ('Willy Adames', 'R'),
        ('Matt Chapman', 'R'),
        ('Luis Arraez', 'L'),
        ('Heliot Ramos', 'R'),
        ('R. Devers', 'L'),
        ('C. Schmitt', 'R'),
        ('J. Encarnacion', 'R'),
        ('Jung Hoo Lee', 'L'),
        ('P. Bailey', 'S')
    ]
    
    # PHI Lineup from screenshot
    phi_lineup = [
        ('Trea Turner', 'R'),
        ('K. Schwarber', 'L'),
        ('Bryce Harper', 'L'),
        ('A. Garcia', 'R'),
        ('B. Marsh', 'L'),
        ('Bryson Stott', 'L'),
        ('Alec Bohm', 'R'),
        ('J. Crawford', 'L'),
        ('R. Marchan', 'S')
    ]
    
    # Game 4: SF @ PHI
    # SF SP: Tyler Mahle (R), 5.26 ERA
    # PHI SP: Jesus Luzardo (L), 6.91 ERA
    # Weather: Assuming 68F, 5mph (Citizens Bank Park)
    
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='SFG',
        home_team='PHI',
        away_sp_name='Tyler Mahle',
        home_sp_name='Jesus Luzardo',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=5.26,
        home_era=6.91,
        away_lineup=sf_lineup,
        home_lineup=phi_lineup,
        park_factor=103, # Citizens Bank Park
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=50,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Tyler Mahle (SF)', a_k)
    print_k_table('Jesus Luzardo (PHI)', h_k)

if __name__ == '__main__':
    run_sim()