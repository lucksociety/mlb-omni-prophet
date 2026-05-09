import sys
import os
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')
from quant_elite_v6_2 import run_v6_2_protocol

def run_sim():
    # STL Lineup from screenshot
    stl_lineup = [
        ('J. Wetherholt', 'L'),
        ('Ivan Herrera', 'R'),
        ('A. Burleson', 'L'),
        ('J. Walker', 'R'),
        ('Nolan Gorman', 'L'),
        ('Masyn Winn', 'R'),
        ('N. Church', 'L'),
        ('Pedro Pages', 'R'),
        ('Victor Scott', 'L')
    ]
    
    # PIT Lineup from screenshot
    pit_lineup = [
        ('Oneil Cruz', 'L'),
        ('Brandon Lowe', 'L'),
        ('B. Reynolds', 'S'),
        ('Ryan O\'Hearn', 'L'),
        ('Marcell Ozuna', 'R'),
        ('Nick Gonzales', 'R'),
        ('S. Horwitz', 'L'),
        ('K. Griffin', 'R'),
        ('Henry Davis', 'R')
    ]
    
    # Game 5: STL @ PIT
    # STL SP: Kyle Leahy (R), 5.63 ERA
    # PIT SP: Braxton Ashcraft (R), 2.43 ERA
    # Weather: Assuming 68F, 5mph (PNC Park)
    
    run_v6_2_protocol(
        away_team='STL',
        home_team='PIT',
        away_sp_name='Kyle Leahy',
        home_sp_name='Braxton Ashcraft',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=5.63,
        home_era=2.43,
        away_lineup=stl_lineup,
        home_lineup=pit_lineup,
        park_factor=98, # PNC Park
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=700,
        rain_intensity=0.0
    )

if __name__ == '__main__':
    run_sim()
