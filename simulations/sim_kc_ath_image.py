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
    # KC Lineup from IMAGE
    kc_lineup = [
        ('M. Garcia', 'R'),
        ('Bobby Witt', 'R'),
        ('Lane Thomas', 'R'),
        ('S. Perez', 'R'),
        ('Nick Loftin', 'R'),
        ('S. Marte', 'R'),
        ('C. Jensen', 'L'),
        ('I. Collins', 'S'),
        ('Elias Diaz', 'R')
    ]
    
    # ATH Lineup from IMAGE
    ath_lineup = [
        ('Jacob Wilson', 'R'),
        ('S. Langeliers', 'R'),
        ('Nick Kurtz', 'L'),
        ('Colby Thomas', 'R'),
        ('D. Hernaiz', 'R'),
        ('C. Cortes', 'L'),
        ('Austin Wynns', 'R'),
        ('Zack Gelof', 'R'),
        ('L. Butler', 'L')
    ]
    
    # KC @ ATH | 3:05 PM ET
    # Weather: 74F, 2mph Wind
    # Umpire: D.J. Reyburn (9.0 R/G)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: KC @ ATH (IMAGE DATA)...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='KC',
        home_team='ATH',
        away_sp_name='Noah Cameron',
        home_sp_name='Jeffrey Springs',
        away_sp_hand='L',
        home_sp_hand='L',
        away_era=5.13,
        home_era=3.79,
        away_lineup=kc_lineup,
        home_lineup=ath_lineup,
        park_factor=96, 
        is_dome=False,
        temp_f=74,
        wind_mph=2,
        wind_ang=90, # Wind 2mph is negligible but I'll set it to 90
        humidity=50,
        altitude=0,
        rain_intensity=0.0,
        away_drs=0, # Assume neutral unless specified
        home_drs=0,
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=0,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='neutral', # 9.0 R/G is neutral/slightly hitter friendly
        away_catcher='Elias Diaz',
        home_catcher='Austin Wynns',
        game_time='15:05'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Noah Cameron (KC)', a_k)
    print_k_table('Jeffrey Springs (ATH)', h_k)

if __name__ == '__main__':
    run_sim()