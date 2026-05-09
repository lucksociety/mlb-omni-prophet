import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

NYY_LINEUP = [
    ('Trent Grisham', 'L'), ('Ben Rice', 'L'), ('Aaron Judge', 'R'),
    ('Cody Bellinger', 'L'), ('Giancarlo Stanton', 'R'), ('Jazz Chisholm Jr.', 'L'),
    ('Austin Wells', 'L'), ('Jose Caballero', 'R'), ('Ryan McMahon', 'L')
]

HOU_LINEUP = [
    ('Carlos Correa', 'R'), ('Yordan Alvarez', 'L'), ('Jose Altuve', 'R'),
    ('Christian Walker', 'R'), ('Isaac Paredes', 'R'), ('Cam Smith', 'R'),
    ('Yainer Diaz', 'R'), ('Dustin Harris', 'L'), ('Brice Matthews', 'R')
]

if __name__ == '__main__':
    # Minute Maid Park (HOU)
    # Weather: Roof CLOSED
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='NYY',
        home_team='HOU',
        away_sp_name='Luis Gil',
        home_sp_name='Spencer Arrighetti',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=4.11,
        home_era=2.45,
        away_lineup=NYY_LINEUP,
        home_lineup=HOU_LINEUP,
        park_factor=102,
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=50,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Luis Gil (NYY)', a_k)
    print_k_table('Spencer Arrighetti (HOU)', h_k)
