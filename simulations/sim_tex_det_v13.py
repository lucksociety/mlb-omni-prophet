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
#!/usr/bin/env python3
from quant_elite_v6_5 import run_v6_5_protocol

# --- GROUND TRUTH LINEUPS (2026-05-02) ---
tex_lineup = [
    ('Evan Carter', 'L'),
    ('Corey Seager', 'L'),
    ('Josh Jung', 'R'),
    ('Joc Pederson', 'L'),
    ('Jake Burger', 'R'),
    ('A. Osuna', 'L'),
    ('E. Duran', 'R'),
    ('Josh Smith', 'L'),
    ('Danny Jansen', 'R')
]

det_lineup = [
    ('Kevin McGonigle', 'L'),
    ('Gleyber Torres', 'R'),
    ('Colt Keith', 'L'),
    ('Riley Greene', 'L'),
    ('Dillon Dingler', 'R'),
    ('Kerry Carpenter', 'L'),
    ('Spencer Torkelson', 'R'),
    ('Wenceel Pérez', 'S'),
    ('Jace Jung', 'L')
]

# --- SIMULATION EXECUTION ---
# Parameters:
# away_team='TEX', home_team='DET', away_sp='Kumar Rocker', home_sp='Keider Montero'
# away_era=3.38, home_era=4.00
# park_factor=98 (Comerica), is_dome=False, temp=49, wind_mph=7, wind_ang=0 (Out)
# humidity=52, altitude=600 (Detroit avg), rain_intensity=0
# away_drs=-2 (TEX injuries), home_drs=3 (DET fielding edge)
# away_manager_hook=-0.3 (Aggressive hook due to BP depth), home_manager_hook=0.2 (Long leash)
# umpire_zone='tight' (Hanahan 92.4% accuracy)
# catchers: Jansen (Standard), Dingler (91st percentile)

if __name__ == "__main__":
    run_v6_5_protocol(
        away_team='TEX',
        home_team='DET',
        away_sp_name='Kumar Rocker',
        home_sp_name='Keider Montero',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.38,
        home_era=4.00,
        away_lineup=tex_lineup,
        home_lineup=det_lineup,
        park_factor=98,
        is_dome=False,
        temp_f=49,
        wind_mph=7,
        wind_ang=0,
        humidity=52,
        altitude=600,
        rain_intensity=0.0,
        away_drs=-2,
        home_drs=3,
        away_manager_hook=-0.3,
        home_manager_hook=0.2,
        umpire_zone='tight',
        away_catcher='Danny Jansen',
        home_catcher='Dillon Dingler',
        game_time='19:15'
    )