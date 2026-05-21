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
    # ARI Lineup from confirmed lineup image
    ari_lineup = [
        ('G. Perdomo', 'S'),
        ('Ketel Marte', 'S'),
        ('C. Carroll', 'L'),
        ('A. Del Castillo', 'L'),
        ('I. Vargas', 'S'),
        ('L. Gurriel', 'R'),
        ('N. Arenado', 'R'),
        ('J. Fernandez', 'R'),
        ('Alek Thomas', 'L')
    ]
    
    # MIL Lineup from confirmed lineup image
    mil_lineup = [
        ('Brice Turang', 'L'),
        ('W. Contreras', 'R'),
        ('Jake Bauers', 'L'),
        ('Gary Sanchez', 'R'),
        ('G. Mitchell', 'L'),
        ('Sal Frelick', 'L'),
        ('Luis Rengifo', 'S'),
        ('D. Hamilton', 'L'),
        ('B. Lockridge', 'R')
    ]
    
    # ARI @ MIL | 1:40 PM ET
    # ARI SP: Michael Soroka (R), 2.60 ERA
    # MIL SP: Brandon Woodruff (R), 3.77 ERA
    # Weather: Dome (American Family Field)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: ARI @ MIL...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='ARI',
        home_team='MIL',
        away_sp_name='Michael Soroka',
        home_sp_name='Brandon Woodruff',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.60,
        home_era=3.77,
        away_lineup=ari_lineup,
        home_lineup=mil_lineup,
        park_factor=101, # American Family Field
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=45,
        altitude=600,
        rain_intensity=0.0,
        away_drs=3, 
        home_drs=3, 
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=0,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='A. Del Castillo',
        home_catcher='W. Contreras',
        game_time='13:40'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5, 8.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Michael Soroka (ARI)', a_k)
    print_k_table('Brandon Woodruff (MIL)', h_k)

if __name__ == '__main__':
    run_sim()