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
from quant_elite_v6_4 import run_v6_4_protocol

# COL @ CIN - April 29, 2026
away_team = 'COL'
home_team = 'CIN'
away_sp = 'Tomoyuki Sugano'
home_sp = 'B. Williamson'
away_sp_hand = 'R'
home_sp_hand = 'L'
away_era = 3.42
home_era = 5.40

col_lineup = [
    ('Jordan Beck', 'R'),
    ('B. Doyle', 'R'),
    ('TJ Rumfield', 'L'),
    ('H. Goodman', 'R'),
    ('Willi Castro', 'S'),
    ('B. Sullivan', 'L'),
    ('Kyle Karros', 'R'),
    ('E. Tovar', 'R'),
    ('M. Moniak', 'L')
]

cin_lineup = [
    ('TJ Friedl', 'L'),
    ('Matt McLain', 'R'),
    ('E. De La Cruz', 'S'),
    ('Sal Stewart', 'R'),
    ('N. Lowe', 'L'),
    ('S. Steer', 'R'),
    ('JJ Bleday', 'L'),
    ('Jose Trevino', 'R'),
    ('K. Hayes', 'R')
]

# Environmental Factors
park_factor = 103 # GABP is hitter friendly
is_dome = False
temp_f = 64
wind_mph = 10
wind_ang = 45 # WNW wind at GABP orientation
humidity = 63
altitude = 500 # Cincinnati elevation
rain_intensity = 0.3 # 30% chance

ar, hr, a_k, h_k = run_v6_4_protocol(away_team, home_team, away_sp, home_sp, away_sp_hand, home_sp_hand,
                                  away_era, home_era, col_lineup, cin_lineup,
                                  park_factor, is_dome, temp_f, wind_mph, wind_ang,
                                  humidity, altitude, rain_intensity)

n = len(ar)
sugano_over_3_5 = sum(1 for k in a_k if k > 3.5) / n * 100
print(f"\n--- PROP PROBABILITY ---")
print(f"Tomoyuki Sugano Over 3.5 K: {sugano_over_3_5:.1f}%")