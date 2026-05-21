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

from quant_elite_v6_1 import run_v6_1_protocol

# ATH Expected Lineup
ATH_LINEUP = [
    ('Jacob Wilson', 'R'), 
    ('S. Langeliers', 'R'), 
    ('Nick Kurtz', 'L'), 
    ('Andy Ibanez', 'R'), 
    ('Max Muncy', 'R'), 
    ('T. Soderstrom', 'L'), 
    ('D. Hernaiz', 'R'), 
    ('Colby Thomas', 'R'), 
    ('Zack Gelof', 'R')
]

# TEX Expected Lineup
TEX_LINEUP = [
    ('B. Nimmo', 'L'), 
    ('Corey Seager', 'L'), 
    ('Jake Burger', 'R'), 
    ('Josh Jung', 'R'), 
    ('K. Higashioka', 'R'), 
    ('A. McCutchen', 'R'), 
    ('Sam Haggerty', 'S'), 
    ('E. Duran', 'R'), 
    ('Josh Smith', 'L')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='ATH',
        home_team='TEX',
        away_sp_name='Jeffrey Springs',
        home_sp_name='MacKenzie Gore',
        away_sp_hand='L',
        home_sp_hand='L',
        away_era=3.34,
        home_era=4.15,
        away_lineup=ATH_LINEUP,
        home_lineup=TEX_LINEUP,
        park_factor=99, # Globe Life Field
        is_dome=True, # Assuming roof closed for heat
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=605,
        rain_intensity=0.0
    )