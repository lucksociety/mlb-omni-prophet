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
    # KC Lineup from screenshot
    kc_lineup = [
        ('M. Garcia', 'R'),
        ('Bobby Witt', 'R'),
        ('V. Pasquantino', 'L'),
        ('S. Perez', 'R'),
        ('C. Jensen', 'L'),
        ('M. Massey', 'L'),
        ('J. Caglianone', 'L'),
        ('I. Collins', 'S'),
        ('Kyle Isbel', 'L')
    ]
    
    # ATH Lineup from screenshot
    ath_lineup = [
        ('S. Langeliers', 'R'),
        ('Nick Kurtz', 'L'),
        ('Brent Rooker', 'R'),
        ('T. Soderstrom', 'L'),
        ('Colby Thomas', 'R'),
        ('Jacob Wilson', 'R'),
        ('Max Muncy', 'R'),
        ('D. Hernaiz', 'R'),
        ('Zack Gelof', 'R')
    ]
    
    # Game 13: KC @ ATH
    # KC SP: Kris Bubic (L), 4.08 ERA
    # ATH SP: Aaron Civale (R), 3.86 ERA
    # Weather: Assuming 62F, 10mph OUT (Oakland Coliseum)
    
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='KCR',
        home_team='ATH',
        away_sp_name='Kris Bubic',
        home_sp_name='Aaron Civale',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=4.08,
        home_era=3.86,
        away_lineup=kc_lineup,
        home_lineup=ath_lineup,
        park_factor=94, # Oakland Coliseum
        is_dome=False,
        temp_f=62,
        wind_mph=10,
        wind_ang=0, # Blowing Out
        humidity=60,
        altitude=10,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Kris Bubic (KC)', a_k)
    print_k_table('Aaron Civale (ATH)', h_k)

if __name__ == '__main__':
    run_sim()