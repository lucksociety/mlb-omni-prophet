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
import quant_elite_v9 as qe

away_team = 'CIN'
home_team = 'PIT'
away_sp_name = 'Rhett Lowder'
home_sp_name = 'Carmen Mlodzinski'

# Lineups from screenshot
away_lineup = [
    ('TJ Friedl', 'L'),
    ('JJ Bleday', 'L'),
    ('Elly De La Cruz', 'S'),
    ('Sal Stewart', 'R'),
    ('Nathaniel Lowe', 'L'),
    ('Spencer Steer', 'R'),
    ('Will Benson', 'L'),
    ('Tyler Stephenson', 'R'),
    ('Ke\'Bryan Hayes', 'R')
]

home_lineup = [
    ('Oneil Cruz', 'L'),
    ('Brandon Lowe', 'L'),
    ('Bryan Reynolds', 'S'),
    ('Ryan O\'Hearn', 'L'),
    ('Nick Gonzales', 'R'),
    ('Marcell Ozuna', 'R'),
    ('Spencer Horwitz', 'L'),
    ('Konnor Griffin', 'R'),
    ('Henry Davis', 'R')
]

# Run Protocol
qe.run_v9_protocol(
    away_team=away_team,
    home_team=home_team,
    away_sp_name=away_sp_name,
    home_sp_name=home_sp_name,
    away_sp_hand='R',
    home_sp_hand='R',
    away_era=3.18,
    home_era=4.13,
    away_lineup=away_lineup,
    home_lineup=home_lineup,
    park_factor=112, # Runs factor
    is_dome=False,
    temp_f=48,
    wind_mph=9,
    wind_ang=180, # Inward
    humidity=63,
    altitude=743,
    rain_intensity=0.1,
    away_drs=-3,
    home_drs=7,
    away_manager_hook=0.2, # Francona (Slow)
    home_manager_hook=-0.3, # Kelly (Quick)
    away_bp_pitches_d1=119,
    away_bp_pitches_d2=0,
    home_bp_pitches_d1=28,
    home_bp_pitches_d2=0,
    umpire_zone='tight',
    away_catcher='Tyler Stephenson',
    home_catcher='Henry Davis',
    game_time='16:05',
    is_game_1=False
)