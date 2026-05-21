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

# ARI @ MIL - April 29, 2026
away_team = 'ARI'
home_team = 'MIL'
away_sp = 'E. Rodriguez'
home_sp = 'Brandon Sproat'
away_sp_hand = 'L'
home_sp_hand = 'R'
away_era = 2.89
home_era = 6.45

ari_lineup = [
    ('Geraldo Perdomo', 'S'),
    ('Ketel Marte', 'S'),
    ('Corbin Carroll', 'L'),
    ('Adrian Del Castillo', 'L'),
    ('Ildemaro Vargas', 'S'),
    ('Lourdes Gurriel', 'R'),
    ('Nolan Arenado', 'R'),
    ('Jose Fernandez', 'R'),
    ('Alek Thomas', 'L')
]

mil_lineup = [
    ('Brandon Lockridge', 'R'),
    ('Brice Turang', 'L'),
    ('William Contreras', 'R'),
    ('Jake Bauers', 'L'),
    ('Gary Sanchez', 'R'),
    ('Luis Rengifo', 'S'),
    ('Greg Jones', 'S'),
    ('Blake Perkins', 'S'),
    ('Joey Ortiz', 'R')
]

# Environmental Factors
park_factor = 102 # American Family Field
is_dome = True
temp_f = 70 # Controlled indoor temp
wind_mph = 0
wind_ang = 0
humidity = 71
altitude = 600
rain_intensity = 0

run_v6_4_protocol(away_team, home_team, away_sp, home_sp, away_sp_hand, home_sp_hand,
                  away_era, home_era, ari_lineup, mil_lineup,
                  park_factor, is_dome, temp_f, wind_mph, wind_ang,
                  humidity, altitude, rain_intensity)