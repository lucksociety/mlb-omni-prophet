import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

AWAY_LINEUP = [
    ('Zach Neto', 'R'), ('Mike Trout', 'R'), ('Yoan Moncada', 'S'),
    ('Jorge Soler', 'R'), ('Jo Adell', 'R'), ('Josh Lowe', 'L'),
    ('Vaughn Grissom', 'R'), ('Travis d\'Arnaud', 'R'), ('Adam Frazier', 'L')
]

HOME_LINEUP = [
    ('Chase Meidroth', 'R'), ('Miguel Vargas', 'R'), ('Munetaka Murakami', 'L'),
    ('Austin Hays', 'R'), ('Colson Montgomery', 'L'), ('Edgar Quero', 'S'),
    ('Derek Hill', 'R'), ('Luisangel Acuna', 'R'), ('Sam Antonacci', 'L')
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='LAA',
        home_team='CWS',
        away_sp_name='Yusei Kikuchi',
        home_sp_name='Erick Fedde',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=6.21,
        home_era=3.42,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=98,
        is_dome=False,
        temp_f=50,
        wind_mph=13,
        wind_ang=270, # In from LF
        humidity=50,
        altitude=600,
        rain_intensity=0.0,
        away_drs=0,
        home_drs=-1,
        away_manager_hook=-0.5, # Kikuchi short leash
        home_manager_hook=0.0,
        away_bp_pitches_d1=20,
        away_bp_pitches_d2=10,
        home_bp_pitches_d1=5,
        home_bp_pitches_d2=15,
        umpire_zone='neutral'
    )
