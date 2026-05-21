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
    # MIA Lineup from screenshot
    mia_lineup = [
        ('Jakob Marsee', 'L'),
        ('Kyle Stowers', 'L'),
        ('Otto Lopez', 'R'),
        ('X. Edwards', 'S'),
        ('Liam Hicks', 'L'),
        ('A. Ramirez', 'R'),
        ('Owen Caissie', 'L'),
        ('Connor Norby', 'R'),
        ('G. Pauley', 'L')
    ]
    
    # LAD Lineup from screenshot
    lad_lineup = [
        ('Kyle Tucker', 'L'),
        ('F. Freeman', 'L'),
        ('Will Smith', 'R'),
        ('T. Hernandez', 'R'),
        ('Max Muncy', 'L'),
        ('Andy Pages', 'R'),
        ('D. Rushing', 'L'),
        ('Hyeseong Kim', 'L'),
        ('A. Freeland', 'S')
    ]
    
    # Game 15: MIA @ LAD
    # MIA SP: Janson Junk (R), 3.67 ERA
    # LAD SP: Shohei Ohtani (R), 0.38 ERA
    # Weather: Assuming 68F, 5mph (Dodger Stadium)
    
    run_v6_2_protocol(
        away_team='MIA',
        home_team='LAD',
        away_sp_name='Janson Junk',
        home_sp_name='Shohei Ohtani',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.67,
        home_era=0.38,
        away_lineup=mia_lineup,
        home_lineup=lad_lineup,
        park_factor=100, # Dodger Stadium
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=200,
        rain_intensity=0.0
    )

if __name__ == '__main__':
    run_sim()