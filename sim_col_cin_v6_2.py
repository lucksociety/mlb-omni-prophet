import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

def run_sim():
    # COL Lineup from screenshot
    col_lineup = [
        ('E. Julien', 'L'),
        ('H. Goodman', 'R'),
        ('M. Moniak', 'L'),
        ('TJ Rumfield', 'L'),
        ('Willi Castro', 'S'),
        ('T. Johnston', 'L'),
        ('Kyle Karros', 'R'),
        ('E. Tovar', 'R'),
        ('J. McCarthy', 'L')
    ]
    
    # CIN Lineup from screenshot
    cin_lineup = [
        ('TJ Friedl', 'L'),
        ('Matt McLain', 'R'),
        ('E. De La Cruz', 'S'),
        ('Sal Stewart', 'R'),
        ('N. Lowe', 'L'),
        ('S. Steer', 'R'),
        ('T. Stephenson', 'R'),
        ('Will Benson', 'L'),
        ('K. Hayes', 'R')
    ]
    
    # Game 3: COL @ CIN
    # COL SP: Tomoyuki Sugano (R), 3.42 ERA
    # CIN SP: Chase Burns (R), 2.57 ERA
    # Weather: Assuming 72F, 5mph (GABP)
    
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='COL',
        home_team='CIN',
        away_sp_name='Tomoyuki Sugano',
        home_sp_name='Chase Burns',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.42,
        home_era=2.57,
        away_lineup=col_lineup,
        home_lineup=cin_lineup,
        park_factor=122, # GABP
        is_dome=False,
        temp_f=72,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=500,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Tomoyuki Sugano (COL)', a_k)
    print_k_table('Chase Burns (CIN)', h_k)

if __name__ == '__main__':
    run_sim()
