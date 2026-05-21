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

# KC @ ATH - April 29, 2026
away_team = 'KC'
home_team = 'ATH'
away_sp = 'Michael Wacha'
home_sp = 'Luis Severino'
away_sp_hand = 'R'
home_sp_hand = 'R'
away_era = 2.51
home_era = 5.17

kc_lineup = [
    ('Maikel Garcia', 'R'),
    ('Bobby Witt Jr.', 'R'),
    ('Carter Jensen', 'L'),
    ('Salvador Perez', 'R'),
    ('Michael Massey', 'L'),
    ('Isaac Collins', 'S'),
    ('Jac Caglianone', 'L'),
    ('Lane Thomas', 'R'),
    ('Kyle Isbel', 'L')
]

ath_lineup = [
    ('Nick Kurtz', 'L'),
    ('Shea Langeliers', 'R'),
    ('Carlos Cortes', 'L'),
    ('Brent Rooker', 'R'),
    ('Jacob Wilson', 'R'),
    ('Jeff McNeil', 'L'),
    ('Zack Gelof', 'R'),
    ('Lawrence Butler', 'L'),
    ('Darell Hernaiz', 'R')
]

# Environmental Factors
park_factor = 104 # Sutter Health Park (Sacramento) - Hitter Friendly
is_dome = False
temp_f = 77
wind_mph = 9
wind_ang = 0 # SW wind is a tailwind at Sutter Health Park
humidity = 42
altitude = 30
rain_intensity = 0

run_v6_4_protocol(away_team, home_team, away_sp, home_sp, away_sp_hand, home_sp_hand,
                  away_era, home_era, kc_lineup, ath_lineup,
                  park_factor, is_dome, temp_f, wind_mph, wind_ang,
                  humidity, altitude, rain_intensity)