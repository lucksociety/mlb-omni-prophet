import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

MIN_LINEUP = [
    ('Byron Buxton', 'R'), ('Trevor Larnach', 'L'), ('Josh Bell', 'S'),
    ('Ryan Jeffers', 'R'), ('Kody Clemens', 'L'), ('Luke Keaschall', 'R'),
    ('Matt Wallner', 'L'), ('Royce Lewis', 'R'), ('Brooks Lee', 'S')
]

TB_LINEUP = [
    ('Chandler Simpson', 'L'), ('Junior Caminero', 'R'), ('Jonathan Aranda', 'L'),
    ('Yandy Diaz', 'R'), ('Jake Fraley', 'L'), ('Cedric Mullins', 'L'),
    ('Nick Fortes', 'R'), ('Richie Palacios', 'L'), ('Taylor Walls', 'S')
]

if __name__ == '__main__':
    # Tropicana Field (TB)
    # Weather: Dome CLOSED (Fixed Roof)
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='MIN',
        home_team='TB',
        away_sp_name='Simeon Woods Richardson',
        home_sp_name='Jesse Scholtens',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=5.96,
        home_era=2.93,
        away_lineup=MIN_LINEUP,
        home_lineup=TB_LINEUP,
        park_factor=95,
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=0,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('S. Woods Richardson (MIN)', a_k)
    print_k_table('Jesse Scholtens (TB)', h_k)
