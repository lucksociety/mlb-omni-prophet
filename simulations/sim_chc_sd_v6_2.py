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
    # CHC Lineup from screenshot
    chc_lineup = [
        ('Nico Hoerner', 'R'),
        ('M. Busch', 'L'),
        ('Alex Bregman', 'R'),
        ('Ian Happ', 'S'),
        ('Seiya Suzuki', 'R'),
        ('M. Ballesteros', 'L'),
        ('Carson Kelly', 'R'),
        ('P. Crow-Armstrong', 'L'),
        ('D. Swanson', 'R')
    ]
    
    # SD Lineup from screenshot
    sd_lineup = [
        ('R. Laureano', 'R'),
        ('F. Tatis', 'R'),
        ('J. Merrill', 'L'),
        ('M. Machado', 'R'),
        ('X. Bogaerts', 'R'),
        ('Gavin Sheets', 'L'),
        ('M. Andujar', 'R'),
        ('F. Fermin', 'R'),
        ('J. Cronenworth', 'L')
    ]
    
    # Game 14: CHC @ SD
    # CHC SP: Edward Cabrera (R), 2.73 ERA
    # SD SP: Walker Buehler (R), 5.75 ERA
    # Weather: Assuming 68F, 5mph (Petco Park)
    
    run_v6_2_protocol(
        away_team='CHC',
        home_team='SDP',
        away_sp_name='Edward Cabrera',
        home_sp_name='Walker Buehler',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.73,
        home_era=5.75,
        away_lineup=chc_lineup,
        home_lineup=sd_lineup,
        park_factor=95, # Petco Park
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=10,
        rain_intensity=0.0
    )

if __name__ == '__main__':
    run_sim()