import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

CHC_LINEUP = [
    ('Nico Hoerner', 'R'), ('Alex Bregman', 'R'), ('Seiya Suzuki', 'R'),
    ('Ian Happ', 'S'), ('Carson Kelly', 'R'), ('Michael Busch', 'L'),
    ('Dansby Swanson', 'R'), ('Pete Crow-Armstrong', 'L'), ('Matt Shaw', 'R')
]

LAD_LINEUP = [
    ('Shohei Ohtani', 'L'), ('Freddie Freeman', 'L'), ('Will Smith', 'R'),
    ('Teoscar Hernandez', 'R'), ('Kyle Tucker', 'L'), ('Santiago Espinal', 'R'),
    ('Miguel Rojas', 'R'), ('Andy Pages', 'R'), ('A. Freeland', 'S')
]

if __name__ == '__main__':
    # Dodger Stadium (LAD)
    # Weather: 65F, Wind 8 mph Out to CF, Humidity 50%, Altitude 500ft
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='CHC',
        home_team='LAD',
        away_sp_name='Shota Imanaga',
        home_sp_name='Justin Wrobleski',
        away_sp_hand='L',
        home_sp_hand='L',
        away_era=2.17,
        home_era=1.88,
        away_lineup=CHC_LINEUP,
        home_lineup=LAD_LINEUP,
        park_factor=100,
        is_dome=False,
        temp_f=65,
        wind_mph=8,
        wind_ang=0, # Blowing out to CF
        humidity=50,
        altitude=500,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Shota Imanaga (CHC)', a_k)
    print_k_table('Justin Wrobleski (LAD)', h_k)
