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

from quant_elite_v6_4 import run_v6_4_protocol

def run_sim():
    # HOU Lineup from confirmed lineup image
    hou_lineup = [
        ('C. Correa', 'R'),
        ('Y. Alvarez', 'L'),
        ('I. Paredes', 'R'),
        ('C. Walker', 'R'),
        ('Jose Altuve', 'R'),
        ('Yainer Diaz', 'R'),
        ('B. Matthews', 'R'),
        ('D. Harris', 'L'),
        ('C. Vazquez', 'R')
    ]
    
    # BAL Lineup from confirmed lineup image
    bal_lineup = [
        ('G. Henderson', 'L'),
        ('Taylor Ward', 'R'),
        ('A. Rutschman', 'S'),
        ('Pete Alonso', 'R'),
        ('D. Beavers', 'L'),
        ('J. Jackson', 'R'),
        ('C. Cowser', 'L'),
        ('Coby Mayo', 'R'),
        ('B. Alexander', 'R')
    ]
    
    # HOU @ BAL | 12:35 PM ET
    # HOU SP: Peter Lambert (R), 3.27 ERA
    # BAL SP: Chris Bassitt (R), 6.75 ERA
    # Weather: Assuming 60F, 5mph (Camden Yards)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: HOU @ BAL...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='HOU',
        home_team='BAL',
        away_sp_name='Peter Lambert',
        home_sp_name='Chris Bassitt',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.27,
        home_era=6.75,
        away_lineup=hou_lineup,
        home_lineup=bal_lineup,
        park_factor=100, # Camden Yards
        is_dome=False,
        temp_f=60,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=0,
        rain_intensity=0.0,
        away_drs=1, 
        home_drs=2, 
        away_manager_hook=0.0,
        home_manager_hook=-0.5, # Bassitt on short leash with that ERA
        away_bp_pitches_d1=0,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='C. Vazquez',
        home_catcher='A. Rutschman',
        game_time='12:35'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Peter Lambert (HOU)', a_k)
    print_k_table('Chris Bassitt (BAL)', h_k)

if __name__ == '__main__':
    run_sim()