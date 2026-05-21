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

from quant_elite_v6_2 import run_v6_2_protocol

def run_sim():
    # ARI Lineup from screenshot
    ari_lineup = [
        ('G. Perdomo', 'S'),
        ('Ketel Marte', 'S'),
        ('C. Carroll', 'L'),
        ('A. Del Castillo', 'L'),
        ('L. Gurriel', 'R'),
        ('I. Vargas', 'S'),
        ('N. Arenado', 'R'),
        ('J. Fernandez', 'R'),
        ('Alek Thomas', 'L')
    ]
    
    # MIL Lineup from screenshot
    mil_lineup = [
        ('Brice Turang', 'L'),
        ('W. Contreras', 'R'),
        ('Jake Bauers', 'L'),
        ('Gary Sanchez', 'R'),
        ('G. Mitchell', 'L'),
        ('Sal Frelick', 'L'),
        ('Luis Rengifo', 'S'),
        ('D. Hamilton', 'L'),
        ('B. Lockridge', 'R')
    ]
    
    # Game 10: ARI @ MIL
    # ARI SP: Merrill Kelly (R), 9.31 ERA
    # MIL SP: Chad Patrick (R), 2.35 ERA
    # Weather: AmFam Field (Dome)
    
    run_v6_2_protocol(
        away_team='ARI',
        home_team='MIL',
        away_sp_name='Merrill Kelly',
        home_sp_name='Chad Patrick',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=9.31,
        home_era=2.35,
        away_lineup=ari_lineup,
        home_lineup=mil_lineup,
        park_factor=101, 
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=600,
        rain_intensity=0.0
    )

if __name__ == '__main__':
    run_sim()