import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

SD_LINEUP = [
    ('Ramon Laureano', 'R'), ('Fernando Tatis Jr.', 'R'), ('Jackson Merrill', 'L'),
    ('Manny Machado', 'R'), ('Xander Bogaerts', 'R'), ('Gavin Sheets', 'L'),
    ('Miguel Andujar', 'R'), ('Freddy Fermin', 'R'), ('Jake Cronenworth', 'L')
]

ARI_LINEUP = [
    ('Geraldo Perdomo', 'S'), ('Ketel Marte', 'S'), ('Corbin Carroll', 'L'),
    ('Adrian Del Castillo', 'L'), ('Lourdes Gurriel Jr.', 'R'), ('Ildemaro Vargas', 'S'),
    ('Nolan Arenado', 'R'), ('Julian Fernandez', 'R'), ('Alek Thomas', 'L')
]

if __name__ == '__main__':
    # Estadio Alfredo Harp Helú (Mexico City)
    # Altitude: 7,350ft (Extreme Carry)
    # Weather: 78F, Light Wind, 30% Humidity
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='SD',
        home_team='ARI',
        away_sp_name='Michael King',
        home_sp_name='Ryne Nelson',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.28,
        home_era=6.97,
        away_lineup=SD_LINEUP,
        home_lineup=ARI_LINEUP,
        park_factor=125, # Mexico City Modifier
        is_dome=False,
        temp_f=78,
        wind_mph=5,
        wind_ang=90,
        humidity=30,
        altitude=7350,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Michael King (SD)', a_k)
    print_k_table('Ryne Nelson (ARI)', h_k)
