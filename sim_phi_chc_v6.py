import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

AWAY_LINEUP = [
    ('Trea Turner', 'R'), ('K. Schwarber', 'L'), ('Bryce Harper', 'L'),
    ('Felix Reyes', 'R'), ('B. Marsh', 'L'), ('Bryson Stott', 'L'),
    ('Alec Bohm', 'R'), ('J. Crawford', 'L'), ('G. Stubbs', 'L'),
]

HOME_LINEUP = [
    ('Nico Hoerner', 'R'), ('Alex Bregman', 'R'), ('Ian Happ', 'S'),
    ('Seiya Suzuki', 'R'), ('M. Busch', 'L'), ('D. Swanson', 'R'),
    ('M. Ballesteros', 'L'), ('Miguel Amaya', 'R'), ('P. Crow-Armstrong', 'L'),
]

if __name__ == '__main__':
    run_v6_2_protocol(
        away_team='PHI',
        home_team='CHC',
        away_sp_name='Cristopher Sanchez',
        home_sp_name='Edward Cabrera',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=1.59,
        home_era=2.38,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=100, # Wrigley Field
        is_dome=False,
        temp_f=72,
        wind_mph=14,
        wind_ang=0, # Out (0 degrees is usually out at Wrigley in many simple models, let's stick to the prompt's wind_ang logic where 90 is cross)
        humidity=50,
        altitude=0,
        rain_intensity=0.0
    )
