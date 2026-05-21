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

AWAY_LINEUP = [
    ('Zach Neto', 'R'), ('Mike Trout', 'R'), ('Yoan Moncada', 'S'),
    ('Jorge Soler', 'R'), ('Jo Adell', 'R'), ('Josh Lowe', 'L'),
    ('V. Grissom', 'R'), ('T. d\'Arnaud', 'R'), ('Adam Frazier', 'L')
]

HOME_LINEUP = [
    ('C. Meidroth', 'R'), ('M. Vargas', 'R'), ('M. Murakami', 'L'),
    ('Austin Hays', 'R'), ('C. Montgomery', 'L'), ('Edgar Quero', 'S'),
    ('Derek Hill', 'R'), ('L. Acuna', 'R'), ('S. Antonacci', 'L')
]

if __name__ == '__main__':
    # Environmental Data: 50°F, 13 mph Wind (L-R)
    # Pitchers: Kikuchi (6.21) vs Fedde (3.42)
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='LAA',
        home_team='CWS',
        away_sp_name='Yusei Kikuchi',
        home_sp_name='Erick Fedde',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=6.21,
        home_era=3.42,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=98,
        is_dome=False,
        temp_f=50,
        wind_mph=13,
        wind_ang=270, # Left to Right
        humidity=50,
        altitude=600,
        rain_intensity=0.0,
        away_drs=0,
        home_drs=-1,
        away_manager_hook=-0.5, # Kikuchi short leash
        home_manager_hook=0.0,
        away_bp_pitches_d1=20,
        away_bp_pitches_d2=10,
        home_bp_pitches_d1=5,
        home_bp_pitches_d2=15,
        umpire_zone='neutral'
    )
    
    # Calculate Joint Probability
    n = len(ar)
    success = sum(1 for i in range(n) if (ar[i] + hr[i] > 6.5) and (h_k[i] > 3.5))
    joint_prob = (success / n) * 100
    print(f"\n── 4. JOINT PROBABILITY (SGP) ─────────────────────────────────────")
    print(f"  [LAA/CWS Over 6.5] AND [E. Fedde Over 3.5 K]: {joint_prob:.2f}%")