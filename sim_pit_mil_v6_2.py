import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

PIT_LINEUP = [
    ('Jake Mangum', 'S'), ('Ryan O\'Hearn', 'L'), ('Bryan Reynolds', 'S'),
    ('Marcell Ozuna', 'R'), ('Nick Gonzales', 'R'), ('Oneil Cruz', 'L'),
    ('Konnor Griffin', 'R'), ('Nick Yorke', 'R'), ('Henry Davis', 'R')
]

MIL_LINEUP = [
    ('Brice Turang', 'L'), ('William Contreras', 'R'), ('Jake Bauers', 'L'),
    ('Gary Sanchez', 'R'), ('Garrett Mitchell', 'L'), ('Brandon Lockridge', 'R'),
    ('Sal Frelick', 'L'), ('David Hamilton', 'L'), ('Joey Ortiz', 'R')
]

if __name__ == '__main__':
    # American Family Field (MIL)
    # Weather: Dome CLOSED
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='PIT',
        home_team='MIL',
        away_sp_name='Carmen Mlodzinski',
        home_sp_name='Kyle Harrison',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=3.28,
        home_era=3.06,
        away_lineup=PIT_LINEUP,
        home_lineup=MIL_LINEUP,
        park_factor=102,
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=600,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('C. Mlodzinski (PIT)', a_k)
    print_k_table('Kyle Harrison (MIL)', h_k)
