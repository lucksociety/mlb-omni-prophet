import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

def run_sim():
    # COL Lineup from confirmed lineup image
    col_lineup = [
        ('Jordan Beck', 'R'),
        ('B. Doyle', 'R'),
        ('H. Goodman', 'R'),
        ('T. Freeman', 'R'),
        ('Willi Castro', 'S'),
        ('TJ Rumfield', 'L'),
        ('Kyle Karros', 'R'),
        ('E. Tovar', 'R'),
        ('T. Johnston', 'L')
    ]
    
    # CIN Lineup from confirmed lineup image
    cin_lineup = [
        ('TJ Friedl', 'L'),
        ('Matt McLain', 'R'),
        ('E. De La Cruz', 'S'),
        ('Sal Stewart', 'R'),
        ('N. Lowe', 'L'),
        ('T. Stephenson', 'R'),
        ('JJ Bleday', 'L'),
        ('S. Steer', 'R'),
        ('Will Benson', 'L')
    ]
    
    # COL @ CIN | 12:40 PM ET
    # COL SP: Michael Lorenzen (R), 5.97 ERA
    # CIN SP: Andrew Abbott (L), 6.59 ERA
    # Weather: Assuming 62F, 5mph (Great American Ball Park)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: COL @ CIN...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='COL',
        home_team='CIN',
        away_sp_name='Michael Lorenzen',
        home_sp_name='Andrew Abbott',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=5.97,
        home_era=6.59,
        away_lineup=col_lineup,
        home_lineup=cin_lineup,
        park_factor=109, # GABP
        is_dome=False,
        temp_f=62,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=500,
        rain_intensity=0.0,
        away_drs=0, 
        home_drs=1, 
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=0,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='H. Goodman',
        home_catcher='T. Stephenson',
        game_time='12:40'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Michael Lorenzen (COL)', a_k)
    print_k_table('Andrew Abbott (CIN)', h_k)

if __name__ == '__main__':
    run_sim()
