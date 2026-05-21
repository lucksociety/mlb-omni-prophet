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

# MIA Confirmed Lineup
MIA_LINEUP = [
    ('A. Ramirez', 'R'), 
    ('Otto Lopez', 'R'), 
    ('Kyle Stowers', 'L'), 
    ('Connor Norby', 'R'), 
    ('X. Edwards', 'S'), 
    ('H. Hernandez', 'R'), 
    ('Leo Jimenez', 'R'), 
    ('J. Sanoja', 'R'), 
    ('Esteury Ruiz', 'R')
]

# SF Confirmed Lineup
SF_LINEUP = [
    ('Willy Adames', 'R'), 
    ('Luis Arraez', 'L'), 
    ('Matt Chapman', 'R'), 
    ('R. Devers', 'L'), 
    ('C. Schmitt', 'R'), 
    ('Jung Hoo Lee', 'L'), 
    ('Heliot Ramos', 'R'), 
    ('Drew Gilbert', 'L'), 
    ('P. Bailey', 'S')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='MIA',
        home_team='SFG',
        away_sp_name='Eury Perez',
        home_sp_name='Robbie Ray',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=4.15,
        home_era=2.86,
        away_lineup=MIA_LINEUP,
        home_lineup=SF_LINEUP,
        park_factor=95, # Oracle Park is pitcher friendly
        is_dome=False,
        temp_f=58,
        wind_mph=8,
        wind_ang=45, # Blowing out toward left-center
        humidity=70,
        altitude=10,
        rain_intensity=0.0
    )