import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

def run_sim():
    # KC Lineup from confirmed lineup image
    kc_lineup = [
        ('M. Garcia', 'R'),
        ('Bobby Witt', 'R'),
        ('V. Pasquantino', 'L'),
        ('S. Perez', 'R'),
        ('Lane Thomas', 'R'),
        ('S. Marte', 'R'),
        ('C. Jensen', 'L'),
        ('Nick Loftin', 'R'),
        ('I. Collins', 'S')
    ]
    
    # ATH Lineup from confirmed lineup image
    ath_lineup = [
        ('Jacob Wilson', 'R'),
        ('S. Langeliers', 'R'),
        ('Nick Kurtz', 'L'),
        ('Brent Rooker', 'R'),
        ('Colby Thomas', 'R'),
        ('T. Soderstrom', 'L'),
        ('Zack Gelof', 'R'),
        ('D. Hernaiz', 'R'),
        ('Jeff McNeil', 'L')
    ]
    
    # KC @ ATH | 3:05 PM ET
    # KC SP: Noah Cameron (L), 5.13 ERA
    # ATH SP: Jeffrey Springs (L), 3.79 ERA
    # Weather: Assuming 65F, 10mph (Oakland/Athletics Park)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: KC @ ATH...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='KC',
        home_team='ATH',
        away_sp_name='Noah Cameron',
        home_sp_name='Jeffrey Springs',
        away_sp_hand='L',
        home_sp_hand='L',
        away_era=5.13,
        home_era=3.79,
        away_lineup=kc_lineup,
        home_lineup=ath_lineup,
        park_factor=96, 
        is_dome=False,
        temp_f=65,
        wind_mph=10,
        wind_ang=90,
        humidity=50,
        altitude=0,
        rain_intensity=0.0,
        away_drs=1, 
        home_drs=1, 
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=0,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='C. Jensen',
        home_catcher='S. Langeliers',
        game_time='15:05'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Noah Cameron (KC)', a_k)
    print_k_table('Jeffrey Springs (ATH)', h_k)

if __name__ == '__main__':
    run_sim()
