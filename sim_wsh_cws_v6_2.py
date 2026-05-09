import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

WSH_LINEUP = [
    ('James Wood', 'L'), ('Luis Garcia Jr.', 'L'), ('Brady House', 'R'),
    ('CJ Abrams', 'L'), ('Jacob Young', 'R'), ('Daylen Lile', 'L'),
    ('Nasim Nunez', 'S'), ('Jose Tena', 'L'), ('Keibert Ruiz', 'S')
]

CWS_LINEUP = [
    ('Charles Meidroth', 'R'), ('Miguel Vargas', 'R'), ('Munetaka Murakami', 'L'),
    ('Everson Pereira', 'R'), ('Edgar Quero', 'S'), ('Colson Montgomery', 'L'),
    ('T. Murray', 'R'), ('Derek Hill', 'R'), ('Luisangel Acuna', 'R')
]

if __name__ == '__main__':
    # Guaranteed Rate Field (CWS)
    # Weather: 69F, High Wind (24 mph) blowing OUT, Rain Intensity 0.6
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='WSH',
        home_team='CWS',
        away_sp_name='Foster Griffin',
        home_sp_name='Sean Burke',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=3.38,
        home_era=4.10,
        away_lineup=WSH_LINEUP,
        home_lineup=CWS_LINEUP,
        park_factor=101,
        is_dome=False,
        temp_f=69,
        wind_mph=24,
        wind_ang=0, # Blowing straight OUT
        humidity=80,
        altitude=600,
        rain_intensity=0.6
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Foster Griffin (WSH)', a_k)
    print_k_table('Sean Burke (CWS)', h_k)
