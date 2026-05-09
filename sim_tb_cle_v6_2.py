import sys
import os

# Add the current directory to sys.path to import quant_elite_v6_2
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')
from quant_elite_v6_2 import run_v6_2_protocol

def run_sim():
    # TB Lineup from screenshot
    tb_lineup = [
        ('Chandler Simpson', 'L'),
        ('Junior Caminero', 'R'),
        ('J. Aranda', 'L'),
        ('Yandy Diaz', 'R'),
        ('Jake Fraley', 'L'),
        ('B. Williamson', 'R'),
        ('C. Mullins', 'L'),
        ('Nick Fortes', 'R'),
        ('Taylor Walls', 'S')
    ]
    
    # CLE Lineup from screenshot
    cle_lineup = [
        ('Steven Kwan', 'L'),
        ('C. DeLauter', 'L'),
        ('Jose Ramirez', 'S'),
        ('K. Manzardo', 'L'),
        ('G. Valera', 'L'),
        ('Daniel Schneemann', 'L'),
        ('T. Bazzana', 'L'),
        ('Bo Naylor', 'L'),
        ('Brayan Rocchio', 'S')
    ]
    
    # Game 1: TB @ CLE
    # TB SP: Nick Martinez (R), 2.10 ERA
    # CLE SP: Tanner Bibee (R), 4.45 ERA
    # Weather: 66F, Wind 8 mph L-R (90 deg)
    
    run_v6_2_protocol(
        away_team='TBR',
        home_team='CLE',
        away_sp_name='Nick Martinez',
        home_sp_name='Tanner Bibee',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.10,
        home_era=4.45,
        away_lineup=tb_lineup,
        home_lineup=cle_lineup,
        park_factor=100, # Progressive Field
        is_dome=False,
        temp_f=66,
        wind_mph=8,
        wind_ang=90, # L-R crosswind
        humidity=50,
        altitude=600,
        rain_intensity=0.0
    )

if __name__ == '__main__':
    run_sim()
