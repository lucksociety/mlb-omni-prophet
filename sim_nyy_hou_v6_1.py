import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_1 import run_v6_1_protocol

# NYY Expected Lineup
NYY_LINEUP = [
    ('T. Grisham', 'L'), 
    ('Ben Rice', 'L'), 
    ('Aaron Judge', 'R'), 
    ('C. Bellinger', 'L'), 
    ('G. Stanton', 'R'), 
    ('J. Chisholm', 'L'), 
    ('Austin Wells', 'L'), 
    ('J. Caballero', 'R'), 
    ('Ryan McMahon', 'L')
]

# HOU Expected Lineup
HOU_LINEUP = [
    ('C. Correa', 'R'), 
    ('Y. Alvarez', 'L'), 
    ('Jose Altuve', 'R'), 
    ('C. Walker', 'R'), 
    ('I. Paredes', 'R'), 
    ('Cam Smith', 'R'), 
    ('Yainer Diaz', 'R'), 
    ('S. Whitcomb', 'R'), 
    ('B. Matthews', 'R')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='NYY',
        home_team='HOU',
        away_sp_name='Ryan Weathers',
        home_sp_name='Mike Burrows',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=3.18,
        home_era=6.75,
        away_lineup=NYY_LINEUP,
        home_lineup=HOU_LINEUP,
        park_factor=100, # Minute Maid Park
        is_dome=True, # Roof Closed
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=80,
        rain_intensity=0.0
    )
