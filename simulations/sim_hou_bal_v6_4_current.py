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
    # HOU Lineup from current image
    hou_lineup = [
        ('B. Matthews', 'R'),
        ('Y. Alvarez', 'L'),
        ('I. Paredes', 'R'),
        ('C. Walker', 'R'),
        ('D. Harris', 'L'),
        ('Yainer Diaz', 'R'),
        ('Cam Smith', 'R'),
        ('D. Johnson', 'L'),
        ('B. Shewmake', 'L')
    ]
    
    # BAL Lineup from current image
    bal_lineup = [
        ('G. Henderson', 'L'),
        ('Taylor Ward', 'R'),
        ('D. Beavers', 'L'),
        ('Pete Alonso', 'R'),
        ('S. Basallo', 'L'),
        ('T. O\'Neill', 'R'),
        ('L. Taveras', 'S'),
        ('W. Wilson', 'R'),
        ('J. Jackson', 'R')
    ]
    
    # HOU @ BAL | 4:05 PM ET
    # HOU SP: Lance McCullers Jr. (R), 6.75 ERA
    # BAL SP: Brandon Young (R), 2.53 ERA
    
    print("\n🚀 EXECUTING CURRENT QUANT-ELITE V6.4: HOU @ BAL...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='HOU',
        home_team='BAL',
        away_sp_name='Lance McCullers Jr.',
        home_sp_name='Brandon Young',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=6.75,
        home_era=2.53,
        away_lineup=hou_lineup,
        home_lineup=bal_lineup,
        park_factor=100, 
        is_dome=False,
        temp_f=67,
        wind_mph=14,
        wind_ang=270, # L-R wind usually means crosswind or blowing slightly in/out depending on orientation. L-R at Camden is roughly 270 deg.
        humidity=55,
        altitude=0,
        rain_intensity=0.0,
        away_drs=1, 
        home_drs=1, 
        away_manager_hook=-0.5, # McCullers high ERA
        home_manager_hook=0.5,  # Young low ERA, let him go deep
        away_bp_pitches_d1=0,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='tight_high_k', # Stu Scheurwater: 17.0 K/G is high
        away_catcher='Yainer Diaz',
        home_catcher='S. Basallo', # Basallo is catching in the image
        game_time='16:05'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Lance McCullers Jr. (HOU)', a_k)
    print_k_table('Brandon Young (BAL)', h_k)

if __name__ == '__main__':
    run_sim()