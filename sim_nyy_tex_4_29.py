import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

AWAY_LINEUP = [
    ('Trent Grisham', 'L'), ('Ben Rice', 'L'), ('Aaron Judge', 'R'),
    ('Cody Bellinger', 'L'), ('Jazz Chisholm Jr.', 'L'), ('Jasson Dominguez', 'S'),
    ('J.C. Escarra', 'L'), ('Ryan McMahon', 'L'), ('Jose Caballero', 'R')
]

HOME_LINEUP = [
    ('Brandon Nimmo', 'L'), ('Josh Jung', 'R'), ('Corey Seager', 'L'),
    ('Joc Pederson', 'L'), ('Jake Burger', 'R'), ('Evan Carter', 'L'),
    ('Kyle Higashioka', 'R'), ('Alejandro Osuna', 'L'), ('Ezequiel Duran', 'R')
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='NYY',
        home_team='TEX',
        away_sp_name='Elmer Rodriguez',
        home_sp_name='Nathan Eovaldi',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=4.50, # Estimated/Minor callup
        home_era=5.79,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=102,
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=600,
        rain_intensity=0.0,
        away_drs=1,
        home_drs=2,
        away_manager_hook=-1.0, # Rookie pitcher
        home_manager_hook=0.0,
        away_bp_pitches_d1=5,
        away_bp_pitches_d2=10,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=5,
        umpire_zone='neutral'
    )
