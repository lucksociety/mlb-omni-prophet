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

from quant_elite_v9 import run_v9_protocol

def run_sim():
    # SF Giants Lineup
    sf_lineup = [
        ('Heliot Ramos', 'R'),
        ('Matt Chapman', 'R'),
        ('Luis Arraez', 'L'),
        ('Casey Schmitt', 'R'),
        ('Rafael Devers', 'L'),
        ('Willy Adames', 'R'),
        ('Jung Hoo Lee', 'L'),
        ('Eric Haase', 'R'),
        ('Drew Gilbert', 'L')
    ]
    
    # PHI Phillies Lineup
    phi_lineup = [
        ('Trea Turner', 'R'),
        ('Kyle Schwarber', 'L'),
        ('Bryce Harper', 'L'),
        ('Adolis Garcia', 'R'),
        ('Bryson Stott', 'L'),
        ('Alec Bohm', 'R'),
        ('Justin Crawford', 'L'),
        ('Felix Reyes', 'R'),
        ('Garrett Stubbs', 'L')
    ]
    
    # Adrian Houser (SF): 7.36 ERA
    # Trevor Richards (PHI): 3.80 ERA (Primary)
    
    print("\n🚀 EXECUTING QUANT-ELITE V9.0: SF @ PHI (Game 2)...")
    
    ar, hr, a_k, h_k = run_v9_protocol(
        away_team='SF',
        home_team='PHI',
        away_sp_name='Adrian Houser',
        home_sp_name='Trevor Richards',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=7.36,
        home_era=3.80,
        away_lineup=sf_lineup,
        home_lineup=phi_lineup,
        park_factor=103,
        is_dome=False,
        temp_f=66,
        wind_mph=8, # Normal breeze
        wind_ang=45, # Cross-out
        humidity=45,
        altitude=50,
        rain_intensity=0.0,
        away_drs=2, 
        home_drs=3, 
        away_manager_hook=0.0,
        home_manager_hook=0.0, # Richards is primary, no hook penalty like opener
        away_bp_pitches_d1=15,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=25,
        home_bp_pitches_d2=10,
        umpire_zone='neutral',
        away_catcher='Eric Haase',
        home_catcher='Garrett Stubbs',
        game_time='17:35'
    )
    tr = [ar[i]+hr[i] for i in range(len(ar))]
    over_8_5 = sum(1 for r in tr if r > 8.5) / len(tr) * 100
    houser_k_over_3_5 = sum(1 for k in a_k if k > 3.5) / len(a_k) * 100
    
    print(f"\n🎯 BET PROBABILITIES:")
    print(f"  Over 8.5 Runs: {over_8_5:.1f}%")
    print(f"  Houser Over 3.5 K: {houser_k_over_3_5:.1f}%")

if __name__ == '__main__':
    run_sim()