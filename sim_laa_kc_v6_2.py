import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

LAA_LINEUP = [
    ('Zach Neto', 'R'), ('Mike Trout', 'R'), ('Nolan Schanuel', 'L'),
    ('Jorge Soler', 'R'), ('Yoan Moncada', 'S'), ('Jo Adell', 'R'),
    ('Josh Lowe', 'L'), ('Logan O\'Hoppe', 'R'), ('Adam Frazier', 'L')
]

KC_LINEUP = [
    ('Maikel Garcia', 'R'), ('Bobby Witt Jr.', 'R'), ('Vinnie Pasquantino', 'L'),
    ('Salvador Perez', 'R'), ('Christian Jensen', 'L'), ('Lane Thomas', 'R'),
    ('Starling Marte', 'R'), ('Isaac Collins', 'S'), ('Nick Loftin', 'R')
]

if __name__ == '__main__':
    # Kauffman Stadium (KC)
    # Weather: 68F, Wind 12 mph In from LF, Humidity 55%, Altitude 800ft
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='LAA',
        home_team='KC',
        away_sp_name='Reid Detmers',
        home_sp_name='Seth Lugo',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=4.08,
        home_era=1.15,
        away_lineup=LAA_LINEUP,
        home_lineup=KC_LINEUP,
        park_factor=96,
        is_dome=False,
        temp_f=68,
        wind_mph=12,
        wind_ang=225, # Blowing in from Left Field
        humidity=55,
        altitude=800,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Reid Detmers (LAA)', a_k)
    print_k_table('Seth Lugo (KC)', h_k)
