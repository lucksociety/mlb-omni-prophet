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
#!/usr/bin/env python3
from quant_elite_v6_5 import run_v6_5_protocol

# MLB QUANT-PROPHET V13.0: CWS @ SD 2026-05-02
# Research-Driven Inputs (from intelligence/matchup_CWS_SD_2026-05-02.md)

# CWS Lineup (Ground-Truth from Screenshot)
cws_lineup = [
    ('Andrew Benintendi', 'L'),
    ('Munetaka Murakami', 'L'),
    ('Miguel Vargas', 'R'),
    ('Colson Montgomery', 'L'),
    ('Charles Meidroth', 'R'),
    ('Sam Antonacci', 'L'),
    ('Edgar Quero', 'S'),
    ('Jarred Kelenic', 'L'),
    ('Triston Peters', 'L')
]

# SD Lineup (Ground-Truth from Screenshot)
sd_lineup = [
    ('Ramon Laureano', 'R'),
    ('Fernando Tatis Jr.', 'R'),
    ('Jackson Merrill', 'L'),
    ('Manny Machado', 'R'),
    ('Xander Bogaerts', 'R'),
    ('Gavin Sheets', 'L'),
    ('Miguel Andujar', 'R'),
    ('Luis Campusano', 'R'),
    ('Jake Cronenworth', 'L')
]

# Pitchers: Sean Burke (CWS) vs Michael King (SD)
# ERA 2026: Burke 3.21, King 2.41
# Environment: Petco Park, 67F, 81% Humidity, 10mph L-R Wind (90 deg), ADI 98.5
# Umpire: Sean Barber (Tight)

if __name__ == '__main__':
    run_v6_5_protocol(
        away_team='CHW', # White Sox abbreviation in database
        home_team='SDP', # Padres abbreviation in database
        away_sp_name='Sean Burke',
        home_sp_name='Michael King',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.21,
        home_era=2.41,
        away_lineup=cws_lineup,
        home_lineup=sd_lineup,
        park_factor=96,
        is_dome=False,
        temp_f=67,
        wind_mph=10,
        wind_ang=90,
        humidity=81,
        altitude=15,
        rain_intensity=0.0,
        away_drs=0,
        home_drs=2, # SD defense slight edge
        away_manager_hook=-0.2, # Grifol hook
        home_manager_hook=0.3, # Shildt aggressive hook/pen
        away_bp_pitches_d1=15, # Dominguez used
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='tight', # Sean Barber
        away_catcher='Edgar Quero',
        home_catcher='Luis Campusano',
        game_time='17:40' # Local time 5:40 PM PT
    )