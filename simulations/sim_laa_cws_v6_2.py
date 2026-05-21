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
    # LAA Lineup from screenshot
    laa_lineup = [
        ('Zach Neto', 'R'),
        ('Mike Trout', 'R'),
        ('Yoan Moncada', 'S'),
        ('Jorge Soler', 'R'),
        ('N. Schanuel', 'L'),
        ('Jo Adell', 'R'),
        ('Josh Lowe', 'L'),
        ('T. d\'Arnaud', 'R'),
        ('Adam Frazier', 'L')
    ]
    
    # CWS Lineup from screenshot
    cws_lineup = [
        ('A. Benintendi', 'L'),
        ('M. Murakami', 'L'),
        ('M. Vargas', 'R'),
        ('C. Montgomery', 'L'),
        ('E. Pereira', 'R'),
        ('S. Antonacci', 'L'),
        ('C. Meidroth', 'R'),
        ('T. Peters', 'L'),
        ('Edgar Quero', 'S')
    ]
    
    # Game 9: LAA @ CWS
    # LAA SP: Jose Soriano (R), 0.24 ERA
    # CWS SP: Davis Martin (R), 2.01 ERA
    # Weather: Assuming 68F, 5mph (Guaranteed Rate Field)
    
    run_v6_2_protocol(
        away_team='LAA',
        home_team='CHW',
        away_sp_name='Jose Soriano',
        home_sp_name='Davis Martin',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=0.24,
        home_era=2.01,
        away_lineup=laa_lineup,
        home_lineup=cws_lineup,
        park_factor=101, # Guaranteed Rate Field
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=600,
        rain_intensity=0.0
    )

if __name__ == '__main__':
    run_sim()