import sys
import os
import statistics
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v9 import run_v9_protocol, ARCHETYPES

# Update Archetypes
ARCHETYPES['Andrew Painter'] = 'North-South'
ARCHETYPES['Max Meyer'] = 'Unicorn'

AWAY_LINEUP = [
    ('Trea Turner', 'R'), ('K. Schwarber', 'L'), ('Bryce Harper', 'L'),
    ('A. Garcia', 'R'), ('B. Marsh', 'L'), ('Bryson Stott', 'L'),
    ('Alec Bohm', 'R'), ('J. Crawford', 'L'), ('R. Marchan', 'S'),
]

HOME_LINEUP = [
    ('Jakob Marsee', 'L'), ('Kyle Stowers', 'L'), ('Otto Lopez', 'R'),
    ('X. Edwards', 'S'), ('Liam Hicks', 'L'), ('A. Ramirez', 'R'),
    ('Owen Caissie', 'L'), ('G. Pauley', 'L'), ('Connor Norby', 'R'),
]

if __name__ == '__main__':
    ar, hr, a_k, h_k = run_v9_protocol(
        away_team='PHI', home_team='MIA',
        away_sp_name='Andrew Painter', home_sp_name='Max Meyer',
        away_sp_hand='R', home_sp_hand='R',
        away_era=5.25, home_era=4.66,
        away_lineup=AWAY_LINEUP, home_lineup=HOME_LINEUP,
        park_factor=97, is_dome=True, temp_f=72, wind_mph=0,
        away_bp_pitches_d1=40, home_bp_pitches_d1=25,
        away_catcher='Rafael Marchan', home_catcher='Liam Hicks',
        game_time='16:10'
    )
    
    def print_k_probs(name, dist):
        n = len(dist)
        print(f"\n--- {name} K-Probability Distribution ---")
        for line in [3.5, 4.5, 5.5, 6.5]:
            over_p = sum(1 for k in dist if k > line) / n * 100
            print(f"Over {line}: {over_p:.2f}% | Under {line}: {100-over_p:.2f}%")

    print_k_probs('Andrew Painter', a_k)
    print_k_probs('Max Meyer', h_k)
