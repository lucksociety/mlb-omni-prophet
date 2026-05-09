import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

def run_sim():
    # STL Lineup from confirmed lineup image
    stl_lineup = [
        ('J. Wetherholt', 'L'),
        ('Ivan Herrera', 'R'),
        ('A. Burleson', 'L'),
        ('Jordan Walker', 'R'),
        ('Nolan Gorman', 'L'),
        ('Masyn Winn', 'R'),
        ('N. Church', 'L'),
        ('Pedro Pages', 'R'),
        ('Victor Scott', 'L')
    ]
    
    # PIT Lineup from confirmed lineup image
    pit_lineup = [
        ('Oneil Cruz', 'L'),
        ('Brandon Lowe', 'L'),
        ('B. Reynolds', 'S'),
        ('Ryan O\'Hearn', 'L'),
        ('N. Gonzales', 'R'),
        ('S. Horwitz', 'L'),
        ('K. Griffin', 'R'),
        ('Jake Mangum', 'S'),
        ('Henry Davis', 'R')
    ]
    
    # STL @ PIT | 12:35 PM ET
    # STL SP: Hunter Dobbins (R), 4.50 ERA (Rookie Default)
    # PIT SP: Paul Skenes (R), 2.48 ERA
    # Weather: Assuming 62F, 8mph (PNC Park)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: STL @ PIT...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='STL',
        home_team='PIT',
        away_sp_name='Hunter Dobbins',
        home_sp_name='Paul Skenes',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=4.50,
        home_era=2.48,
        away_lineup=stl_lineup,
        home_lineup=pit_lineup,
        park_factor=97, # PNC Park
        is_dome=False,
        temp_f=62,
        wind_mph=8,
        wind_ang=90,
        humidity=50,
        altitude=700,
        rain_intensity=0.0,
        away_drs=0, 
        home_drs=3, 
        away_manager_hook=0.0,
        home_manager_hook=0.5, # Skenes gets a longer leash
        away_bp_pitches_d1=20,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=5,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='Pedro Pages',
        home_catcher='Henry Davis',
        game_time='12:35'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [4.5, 5.5, 6.5, 7.5, 8.5, 9.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Hunter Dobbins (STL)', a_k)
    print_k_table('Paul Skenes (PIT)', h_k)

if __name__ == '__main__':
    run_sim()
