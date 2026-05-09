import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

MIA_LINEUP = [
    ('Jakob Marsee', 'L'), ('Kyle Stowers', 'L'), ('Otto Lopez', 'R'),
    ('Xavier Edwards', 'S'), ('Liam Hicks', 'L'), ('Abimelec Ramirez', 'R'),
    ('Owen Caissie', 'L'), ('Graham Pauley', 'L'), ('Connor Norby', 'R')
]

SFG_LINEUP = [
    ('Willy Adames', 'R'), ('Luis Arraez', 'L'), ('Matt Chapman', 'R'),
    ('Rafael Devers', 'L'), ('Casey Schmitt', 'R'), ('Jung Hoo Lee', 'L'),
    ('Heliot Ramos', 'R'), ('Drew Gilbert', 'L'), ('Patrick Bailey', 'S')
]

if __name__ == '__main__':
    # Oracle Park (SFG)
    # Weather: 62F, Wind 15 mph In from RF, Humidity 65%, Altitude 0ft
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='MIA',
        home_team='SFG',
        away_sp_name='Max Meyer',
        home_sp_name='Landen Roupp',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.96,
        home_era=2.28,
        away_lineup=MIA_LINEUP,
        home_lineup=SFG_LINEUP,
        park_factor=95,
        is_dome=False,
        temp_f=62,
        wind_mph=15,
        wind_ang=225, # Blowing in from Right Field
        humidity=65,
        altitude=0,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Max Meyer (MIA)', a_k)
    print_k_table('Landen Roupp (SFG)', h_k)
