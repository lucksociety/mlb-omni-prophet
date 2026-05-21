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

# --- GAME DATA: NYM @ LAA (May 1, 2026) ---

# Lineups
nym_lineup = [
    ('Bo Bichette', 'R'),
    ('Juan Soto', 'L'),
    ('MJ Melendez', 'L'),
    ('F. Alvarez', 'R'),
    ('Brett Baty', 'L'),
    ('M. Semien', 'R'),
    ('Carson Benge', 'L'),
    ('T. Taylor', 'R'),
    ('R. Mauricio', 'S')
]

laa_lineup = [
    ('Zach Neto', 'R'),
    ('Mike Trout', 'R'),
    ('Yoan Moncada', 'S'),
    ('Jorge Soler', 'R'),
    ('N. Schanuel', 'L'),
    ('Jo Adell', 'R'),
    ('Josh Lowe', 'L'),
    ('T. d\'Arnaud', 'R'),
    ('Adam Frazier', 'L')
]

# Run Simulation
if __name__ == "__main__":
    run_v6_4_protocol(
        away_team='NYM',
        home_team='LAA',
        away_sp_name='Christian Scott',
        home_sp_name='Walbert Urena',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=6.75,
        home_era=4.76,
        away_lineup=nym_lineup,
        home_lineup=laa_lineup,
        park_factor=98,
        is_dome=False,
        temp_f=73,
        wind_mph=7,
        wind_ang=0, # Blowing out to center
        humidity=50,
        altitude=160,
        rain_intensity=0.0,
        away_drs=0,
        home_drs=0,
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=25, # Recent usage adjustments
        away_bp_pitches_d2=10,
        home_bp_pitches_d1=45, # High fatigue for LAA
        home_bp_pitches_d2=20,
        umpire_zone='neutral',
        away_catcher='F. Alvarez',
        home_catcher='T. d\'Arnaud',
        game_time='18:30'
    )