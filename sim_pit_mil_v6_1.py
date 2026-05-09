import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_1 import run_v6_1_protocol

# PIT Expected Lineup
PIT_LINEUP = [
    ('Oneil Cruz', 'L'), 
    ('Brandon Lowe', 'L'), 
    ('B. Reynolds', 'S'), 
    ('Ryan O\'Hearn', 'L'), 
    ('Nick Yorke', 'R'), 
    ('M. Ozuna', 'R'), 
    ('S. Horwitz', 'L'), 
    ('K. Griffin', 'R'), 
    ('Joey Bart', 'R')
]

# MIL Expected Lineup
MIL_LINEUP = [
    ('Brice Turang', 'L'), 
    ('W. Contreras', 'R'), 
    ('Jake Bauers', 'L'), 
    ('Gary Sanchez', 'R'), 
    ('G. Mitchell', 'L'), 
    ('B. Lockridge', 'R'), 
    ('Sal Frelick', 'L'), 
    ('D. Hamilton', 'L'), 
    ('Joey Ortiz', 'R')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='PIT',
        home_team='MIL',
        away_sp_name='Mitch Keller',
        home_sp_name='J. Misiorowski',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.79,
        home_era=3.04,
        away_lineup=PIT_LINEUP,
        home_lineup=MIL_LINEUP,
        park_factor=101, # American Family Field
        is_dome=True, # Roof Closed
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=604,
        rain_intensity=0.0
    )
