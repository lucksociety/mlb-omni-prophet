import sys
import os
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')
from quant_elite_v6_2 import run_v6_2_protocol

def run_sim():
    # BOS Lineup from screenshot
    bos_lineup = [
        ('Jarren Duran', 'L'),
        ('W. Contreras', 'R'),
        ('R. Anthony', 'L'),
        ('Wilyer Abreu', 'L'),
        ('Trevor Story', 'R'),
        ('M. Mayer', 'L'),
        ('C. Rafaela', 'R'),
        ('C. Narvaez', 'R'),
        ('Caleb Durbin', 'R')
    ]
    
    # TOR Lineup from screenshot
    tor_lineup = [
        ('Myles Straw', 'R'),
        ('E. Clement', 'R'),
        ('V. Guerrero', 'R'),
        ('K. Okamoto', 'R'),
        ('Eloy Jimenez', 'R'),
        ('Lenyn Sosa', 'R'),
        ('D. Varsho', 'L'),
        ('D. Schneider', 'R'),
        ('T. Heineman', 'S')
    ]
    
    # Game 6: BOS @ TOR
    # BOS SP: Payton Tolle (L), 1.50 ERA
    # TOR SP: Trey Yesavage (R), 0.00 ERA (Stat is low/fresh)
    # Weather: Rogers Centre (Dome)
    
    run_v6_2_protocol(
        away_team='BOS',
        home_team='TOR',
        away_sp_name='Payton Tolle',
        home_sp_name='Trey Yesavage',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=1.50,
        home_era=4.50, # Defaulting ERA to 4.50 for Yesavage as 0.00 is likely small sample/unstable for state engine
        away_lineup=bos_lineup,
        home_lineup=tor_lineup,
        park_factor=101, 
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=0,
        rain_intensity=0.0
    )

if __name__ == '__main__':
    run_sim()
