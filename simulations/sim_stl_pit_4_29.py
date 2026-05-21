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

# STL @ PIT - April 29, 2026
away_team = 'STL'
home_team = 'PIT'
away_sp = 'Andre Pallante'
home_sp = 'Bubba Chandler'
away_sp_hand = 'R'
home_sp_hand = 'R'
away_era = 4.26
home_era = 4.88

stl_lineup = [
    ('J.J. Wetherholt', 'L'),
    ('Ivan Herrera', 'R'),
    ('Alec Burleson', 'L'),
    ('Jordan Walker', 'R'),
    ('Nolan Gorman', 'L'),
    ('Masyn Winn', 'R'),
    ('Nathan Church', 'L'),
    ('Ramon Urias', 'R'),
    ('Victor Scott', 'L')
]

pit_lineup = [
    ('Oneil Cruz', 'L'),
    ('Brandon Lowe', 'L'),
    ('Bryan Reynolds', 'S'),
    ('Ryan O\'Hearn', 'L'),
    ('Marcell Ozuna', 'R'),
    ('Nick Gonzales', 'R'),
    ('Spencer Horwitz', 'L'),
    ('K. Griffin', 'R'),
    ('Joey Bart', 'R')
]

# Environmental Factors
park_factor = 97 # PNC Park is pitcher friendly
is_dome = False
temp_f = 58
wind_mph = 11
wind_ang = 120 # NW wind at PNC orientation (slightly in/across)
humidity = 86
altitude = 700
rain_intensity = 0.6 # 55% chance, light rain

run_v6_4_protocol(away_team, home_team, away_sp, home_sp, away_sp_hand, home_sp_hand,
                  away_era, home_era, stl_lineup, pit_lineup,
                  park_factor, is_dome, temp_f, wind_mph, wind_ang,
                  humidity, altitude, rain_intensity)