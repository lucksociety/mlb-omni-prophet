import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

def run_sim():
    # DET Lineup from screenshot
    det_lineup = [
        ('Jahmai Jones', 'R'),
        ('G. Torres', 'R'),
        ('K. McGonigle', 'L'),
        ('M. Vierling', 'R'),
        ('D. Dingler', 'R'),
        ('Riley Greene', 'L'),
        ('S. Torkelson', 'R'),
        ('Hao-Yu Lee', 'R'),
        ('Javier Baez', 'R')
    ]
    
    # ATL Lineup from screenshot
    atl_lineup = [
        ('Ronald Acuna', 'R'),
        ('D. Baldwin', 'L'),
        ('Matt Olson', 'L'),
        ('Ozzie Albies', 'S'),
        ('M. Harris', 'L'),
        ('Austin Riley', 'R'),
        ('D. Smith', 'L'),
        ('M. Dubon', 'R'),
        ('M. Yastrzemski', 'L')
    ]
    
    # Game 8: DET @ ATL
    # DET SP: Casey Mize (R), 2.51 ERA
    # ATL SP: Martin Perez (L), 2.70 ERA
    # Weather: Assuming 68F, 5mph (Truist Park)
    
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='DET',
        home_team='ATL',
        away_sp_name='Casey Mize',
        home_sp_name='Martin Perez',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=2.51,
        home_era=2.70,
        away_lineup=det_lineup,
        home_lineup=atl_lineup,
        park_factor=101, # Truist Park
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=1000,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Casey Mize (DET)', a_k)
    print_k_table('Martin Perez (ATL)', h_k)

if __name__ == '__main__':
    run_sim()
