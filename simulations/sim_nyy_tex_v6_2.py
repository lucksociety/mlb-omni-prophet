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
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')
from quant_elite_v6_2 import run_v6_2_protocol

def run_sim():
    # NYY Lineup from screenshot
    nyy_lineup = [
        ('T. Grisham', 'L'),
        ('Aaron Judge', 'R'),
        ('C. Bellinger', 'L'),
        ('Ben Rice', 'L'),
        ('J. Chisholm', 'L'),
        ('J. Dominguez', 'S'),
        ('Austin Wells', 'L'),
        ('Ryan McMahon', 'L'),
        ('J. Caballero', 'R')
    ]
    
    # TEX Lineup from screenshot
    tex_lineup = [
        ('B. Nimmo', 'L'),
        ('Joc Pederson', 'L'),
        ('Corey Seager', 'L'),
        ('Josh Jung', 'R'),
        ('Evan Carter', 'L'),
        ('Jake Burger', 'R'),
        ('Josh Smith', 'L'),
        ('Danny Jansen', 'R'),
        ('A. Osuna', 'L')
    ]
    
    # Game 12: NYY @ TEX
    # NYY SP: Cam Schlittler (R), 1.77 ERA
    # TEX SP: Jacob deGrom (R), 2.13 ERA
    # Weather: Globe Life Field (Dome)
    
    run_v6_2_protocol(
        away_team='NYY',
        home_team='TEX',
        away_sp_name='Cam Schlittler',
        home_sp_name='Jacob deGrom',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=1.77,
        home_era=2.13,
        away_lineup=nyy_lineup,
        home_lineup=tex_lineup,
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