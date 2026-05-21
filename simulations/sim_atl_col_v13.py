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

# ── LINEUP DEFINITIONS (VERIFIED BY GROUND-TRUTH IMAGE) ──────────
away_lineup = [
    ('Ronald Acuna', 'R'),
    ('Drake Baldwin', 'L'),
    ('Ozzie Albies', 'S'),
    ('Matt Olson', 'L'),
    ('Michael Harris', 'L'),
    ('Mauricio Dubon', 'R'),
    ('Austin Riley', 'R'),
    ('Mike Yastrzemski', 'L'),
    ('Jorge Mateo', 'R')
]

home_lineup = [
    ('Jordan Beck', 'R'),
    ('Brenton Doyle', 'R'),
    ('TJ Rumfield', 'L'),
    ('Hunter Goodman', 'R'),
    ('Willi Castro', 'S'),
    ('Brett Sullivan', 'L'),
    ('Kyle Karros', 'R'),
    ('Ezequiel Tovar', 'R'),
    ('Troy Johnston', 'L')
]

# ── EXECUTE V13.0 CHAOS ENGINE SIMULATION ────────────────────────
if __name__ == '__main__':
    run_v6_5_protocol(
        away_team='ATL',
        home_team='COL',
        away_sp_name='Chris Sale',
        home_sp_name='Chase Dollander',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=2.31,
        home_era=3.42,
        away_lineup=away_lineup,
        home_lineup=home_lineup,
        park_factor=115,     # Coors Field
        is_dome=False,
        temp_f=71,
        wind_mph=5,
        wind_ang=90,         # East Crosswind
        humidity=11,
        altitude=5280,
        rain_intensity=0.01,
        away_drs=5,          # Braves Defense Elite
        home_drs=-2,         # Rockies Defense Rebuilding
        umpire_zone='wide',  # Chad Whitson 1.02 K-Factor
        away_catcher='Drake Baldwin',
        home_catcher='Hunter Goodman',
        game_time='20:10'
    )