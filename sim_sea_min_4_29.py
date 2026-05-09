import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

AWAY_LINEUP = [
    ('J.P. Crawford', 'L'), ('Cal Raleigh', 'S'), ('Julio Rodriguez', 'R'),
    ('Josh Naylor', 'L'), ('Randy Arozarena', 'R'), ('Luke Raley', 'L'),
    ('Dominic Canzone', 'L'), ('Cole Young', 'L'), ('Will Wilson', 'R')
]

HOME_LINEUP = [
    ('Byron Buxton', 'R'), ('Trevor Larnach', 'L'), ('Josh Bell', 'S'),
    ('Ryan Jeffers', 'R'), ('Kody Clemens', 'L'), ('Luke Keaschall', 'R'),
    ('Matt Wallner', 'L'), ('Brooks Lee', 'S'), ('Royce Lewis', 'R')
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='SEA',
        home_team='MIN',
        away_sp_name='George Kirby',
        home_sp_name='Taj Bradley',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.97,
        home_era=2.91,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=100,
        is_dome=False,
        temp_f=49,
        wind_mph=10,
        wind_ang=180, # Out to CF
        humidity=45,
        altitude=800,
        rain_intensity=0.0,
        away_drs=5, # Kirby + Elite Defense
        home_drs=2,
        away_manager_hook=0.5,
        home_manager_hook=0.5,
        away_bp_pitches_d1=5,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=10,
        home_bp_pitches_d2=5,
        umpire_zone='neutral'
    )
