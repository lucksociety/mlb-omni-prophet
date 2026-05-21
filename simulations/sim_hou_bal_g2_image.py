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
    # HOU Lineup from IMAGE (Game 2)
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
    
    # BAL Lineup from IMAGE (Game 2)
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
    
    # HOU @ BAL | 4:05 PM ET (Game 2)
    # HOU SP: Lance McCullers (R), 6.75 ERA
    # BAL SP: Brandon Young (R), 2.53 ERA
    # Weather: Assuming 60F, 5mph (Camden Yards)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: HOU @ BAL GAME 2 (IMAGE DATA)...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='HOU',
        home_team='BAL',
        away_sp_name='Lance McCullers',
        home_sp_name='Brandon Young',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=6.75,
        home_era=2.53,
        away_lineup=hou_lineup,
        home_lineup=bal_lineup,
        park_factor=100, 
        is_dome=False,
        temp_f=60,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=0,
        rain_intensity=0.0,
        away_drs=1, 
        home_drs=2, 
        away_manager_hook=-0.5, # McCullers high ERA leash
        home_manager_hook=0.0,
        away_bp_pitches_d1=15, # DH Game 2, bullpen might be stressed
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=15,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='Yainer Diaz',
        home_catcher='S. Basallo',
        game_time='16:05'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Lance McCullers (HOU)', a_k)
    print_k_table('Brandon Young (BAL)', h_k)

if __name__ == '__main__':
    run_sim()