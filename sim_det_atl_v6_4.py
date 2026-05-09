import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

def run_sim():
    # DET Lineup from confirmed lineup image
    det_lineup = [
        ('K. McGonigle', 'L'),
        ('G. Torres', 'R'),
        ('Colt Keith', 'L'),
        ('Riley Greene', 'L'),
        ('S. Torkelson', 'R'),
        ('K. Carpenter', 'L'),
        ('M. Vierling', 'R'),
        ('Hao-Yu Lee', 'R'),
        ('Jake Rogers', 'R')
    ]
    
    # ATL Lineup from confirmed lineup image
    atl_lineup = [
        ('Ronald Acuna', 'R'),
        ('D. Baldwin', 'L'),
        ('Ozzie Albies', 'S'),
        ('Matt Olson', 'L'),
        ('Austin Riley', 'R'),
        ('M. Dubon', 'R'),
        ('Kyle Farmer', 'R'),
        ('Jorge Mateo', 'R'),
        ('Eli White', 'R')
    ]
    
    # DET @ ATL | 12:15 PM ET
    # DET SP: Framber Valdez (L), 3.41 ERA
    # ATL SP: Bryce Elder (R), 1.95 ERA
    # Weather: 64F, 5mph wind, 60% Humidity (Truist Park)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: DET @ ATL...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='DET',
        home_team='ATL',
        away_sp_name='Framber Valdez',
        home_sp_name='Bryce Elder',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=3.41,
        home_era=1.95,
        away_lineup=det_lineup,
        home_lineup=atl_lineup,
        park_factor=101, 
        is_dome=False,
        temp_f=64,
        wind_mph=5,
        wind_ang=90,
        humidity=60,
        altitude=1000,
        rain_intensity=0.0,
        away_drs=2, # Estimated
        home_drs=5, # Braves defense
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=15, # Rested
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=10, # Rested
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='Jake Rogers',
        home_catcher='D. Baldwin',
        game_time='12:15'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Framber Valdez (DET)', a_k)
    print_k_table('Bryce Elder (ATL)', h_k)

if __name__ == '__main__':
    run_sim()
