import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_1 import run_v6_1_protocol

# PHI Expected Lineup
PHI_LINEUP = [
    ('Trea Turner', 'R'), 
    ('K. Schwarber', 'L'), 
    ('Bryce Harper', 'L'), 
    ('A. Garcia', 'R'), 
    ('B. Marsh', 'L'), 
    ('Alec Bohm', 'R'), 
    ('Bryson Stott', 'L'), 
    ('J. Crawford', 'L'), 
    ('R. Marchan', 'S')
]

# ATL Expected Lineup
ATL_LINEUP = [
    ('Ronald Acuna', 'R'), 
    ('D. Baldwin', 'L'), 
    ('Matt Olson', 'L'), 
    ('Austin Riley', 'R'), 
    ('Ozzie Albies', 'S'), 
    ('M. Harris', 'L'), 
    ('D. Smith', 'L'), 
    ('M. Dubon', 'R'), 
    ('M. Yastrzemski', 'L')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='PHI',
        home_team='ATL',
        away_sp_name='Zack Wheeler',
        home_sp_name='Bryce Elder',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.30, # Calibrated from placeholder 0.00
        home_era=1.50,
        away_lineup=PHI_LINEUP,
        home_lineup=ATL_LINEUP,
        park_factor=105, # Truist Park
        is_dome=False,
        temp_f=68,
        wind_mph=4,
        wind_ang=210, # Blowing somewhat in from left-center
        humidity=60,
        altitude=1000,
        rain_intensity=0.0
    )
