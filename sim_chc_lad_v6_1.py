import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_1 import run_v6_1_protocol

# CHC Expected Lineup
CHC_LINEUP = [
    ('Nico Hoerner', 'R'), 
    ('M. Busch', 'L'), 
    ('Alex Bregman', 'R'), 
    ('Ian Happ', 'S'), 
    ('Seiya Suzuki', 'R'), 
    ('M. Ballesteros', 'L'), 
    ('Carson Kelly', 'R'), 
    ('P. Crow-Armstrong', 'L'), 
    ('D. Swanson', 'R')
]

# LAD Expected Lineup
LAD_LINEUP = [
    ('S. Ohtani', 'L'), 
    ('F. Freeman', 'L'), 
    ('Will Smith', 'R'), 
    ('Kyle Tucker', 'L'), 
    ('Max Muncy', 'L'), 
    ('T. Hernandez', 'R'), 
    ('Andy Pages', 'R'), 
    ('Hyeseong Kim', 'L'), 
    ('A. Freeland', 'S')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='CHC',
        home_team='LAD',
        away_sp_name='Colin Rea',
        home_sp_name='Roki Sasaki',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.00,
        home_era=6.11,
        away_lineup=CHC_LINEUP,
        home_lineup=LAD_LINEUP,
        park_factor=102, # Dodger Stadium
        is_dome=False,
        temp_f=65,
        wind_mph=6,
        wind_ang=180, # Blowing in
        humidity=60,
        altitude=267,
        rain_intensity=0.1 # Light rain
    )
