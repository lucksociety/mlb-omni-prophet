import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

COL_LINEUP = [
    ('Edouard Julien', 'L'), ('Mickey Moniak', 'L'), ('Hunter Goodman', 'R'),
    ('TJ Rumfield', 'L'), ('Troy Johnston', 'L'), ('Ezequiel Tovar', 'R'),
    ('Kyle Karros', 'R'), ('Willi Castro', 'S'), ('Brenton Doyle', 'R')
]

NYM_LINEUP = [
    ('Bo Bichette', 'R'), ('Juan Soto', 'L'), ('Francisco Alvarez', 'R'),
    ('Luis Robert Jr.', 'R'), ('Brett Baty', 'L'), ('Mark Vientos', 'R'),
    ('Marcus Semien', 'R'), ('Ronny Mauricio', 'S'), ('Carson Benge', 'L')
]

if __name__ == '__main__':
    # Citi Field (NYM) - Game 2 of DH
    # Weather: 68F, Wind 6 mph Neutral, Humidity 70%, Altitude 0ft
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='COL',
        home_team='NYM',
        away_sp_name='Chase Dollander',
        home_sp_name='Kodai Senga',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.88,
        home_era=8.83,
        away_lineup=COL_LINEUP,
        home_lineup=NYM_LINEUP,
        park_factor=96,
        is_dome=False,
        temp_f=68,
        wind_mph=6,
        wind_ang=90, # Neutral
        humidity=70,
        altitude=0,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Chase Dollander (COL)', a_k)
    print_k_table('Kodai Senga (NYM)', h_k)
