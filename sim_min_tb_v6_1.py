import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_1 import run_v6_1_protocol

# MIN Confirmed Lineup
MIN_LINEUP = [
    ('Byron Buxton', 'R'), 
    ('A. Martin', 'R'), 
    ('Josh Bell', 'S'), 
    ('Ryan Jeffers', 'R'), 
    ('V. Caratini', 'S'), 
    ('L. Keaschall', 'R'), 
    ('Matt Wallner', 'L'), 
    ('Royce Lewis', 'R'), 
    ('Brooks Lee', 'S')
]

# TB Confirmed Lineup
TB_LINEUP = [
    ('C. Simpson', 'L'), 
    ('J. Caminero', 'R'), 
    ('J. Aranda', 'L'), 
    ('Yandy Diaz', 'R'), 
    ('Jake Fraley', 'L'), 
    ('B. Williamson', 'R'), 
    ('C. Mullins', 'L'), 
    ('Nick Fortes', 'R'), 
    ('R. Palacios', 'L')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='MIN',
        home_team='TBR',
        away_sp_name='Bailey Ober',
        home_sp_name='Shane McClanahan',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=4.15,
        home_era=5.00,
        away_lineup=MIN_LINEUP,
        home_lineup=TB_LINEUP,
        park_factor=94, # Tropicana Field
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=44,
        rain_intensity=0.0
    )
