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
    # SEA Lineup from screenshot
    sea_lineup = [
        ('J. Crawford', 'L'),
        ('Cal Raleigh', 'S'),
        ('J. Rodriguez', 'R'),
        ('Josh Naylor', 'L'),
        ('R. Arozarena', 'R'),
        ('Luke Raley', 'L'),
        ('D. Canzone', 'L'),
        ('Cole Young', 'L'),
        ('Leo Rivas', 'S')
    ]
    
    # MIN Lineup from screenshot
    min_lineup = [
        ('Byron Buxton', 'R'),
        ('Brooks Lee', 'S'),
        ('T. Larnach', 'L'),
        ('Josh Bell', 'S'),
        ('Ryan Jeffers', 'R'),
        ('Kody Clemens', 'L'),
        ('L. Keaschall', 'R'),
        ('Matt Wallner', 'L'),
        ('Royce Lewis', 'R')
    ]
    
    # Game 11: SEA @ MIN
    # SEA SP: Logan Gilbert (R), 4.36 ERA
    # MIN SP: Joe Ryan (R), 3.90 ERA
    # Weather: Assuming 68F, 5mph (Target Field)
    
    run_v6_2_protocol(
        away_team='SEA',
        home_team='MIN',
        away_sp_name='Logan Gilbert',
        home_sp_name='Joe Ryan',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=4.36,
        home_era=3.90,
        away_lineup=sea_lineup,
        home_lineup=min_lineup,
        park_factor=100, # Target Field
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=800,
        rain_intensity=0.0
    )

if __name__ == '__main__':
    run_sim()