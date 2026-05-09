import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_1 import run_v6_1_protocol

# LAA Expected Lineup
LAA_LINEUP = [
    ('Zach Neto', 'R'), 
    ('Mike Trout', 'R'), 
    ('Jo Adell', 'R'), 
    ('Jorge Soler', 'R'), 
    ('O. Peraza', 'R'), 
    ('N. Schanuel', 'L'), 
    ('V. Grissom', 'R'), 
    ('L. O\'Hoppe', 'R'), 
    ('B. Teodosio', 'R')
]

# KC Expected Lineup
KC_LINEUP = [
    ('M. Garcia', 'R'), 
    ('Bobby Witt', 'R'), 
    ('V. Pasquantino', 'L'), 
    ('S. Perez', 'R'), 
    ('C. Jensen', 'L'), 
    ('M. Massey', 'L'), 
    ('J. Caglianone', 'L'), 
    ('I. Collins', 'S'), 
    ('Kyle Isbel', 'L')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='LAA',
        home_team='KCR',
        away_sp_name='Walbert Urena',
        home_sp_name='Cole Ragans',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=2.35,
        home_era=6.00,
        away_lineup=LAA_LINEUP,
        home_lineup=KC_LINEUP,
        park_factor=101, # Kauffman Stadium
        is_dome=False,
        temp_f=62,
        wind_mph=9,
        wind_ang=60, # Cross-wind blowing somewhat out
        humidity=50,
        altitude=912,
        rain_intensity=0.0
    )
