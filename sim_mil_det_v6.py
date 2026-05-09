import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

AWAY_LINEUP = [
    ('B. Lockridge', 'R'), ('Brice Turang', 'L'), ('W. Contreras', 'R'),
    ('Gary Sanchez', 'R'), ('Luis Matos', 'R'), ('B. Perkins', 'S'),
    ('Luis Rengifo', 'S'), ('Joey Ortiz', 'R'), ('D. Hamilton', 'L'),
]

HOME_LINEUP = [
    ('K. McGonigle', 'L'), ('G. Torres', 'R'), ('Colt Keith', 'L'),
    ('Riley Greene', 'L'), ('D. Dingler', 'R'), ('K. Carpenter', 'L'),
    ('S. Torkelson', 'R'), ('W. Perez', 'S'), ('Javier Baez', 'R'),
]

if __name__ == '__main__':
    run_v6_2_protocol(
        away_team='MIL',
        home_team='DET',
        away_sp_name='Brandon Sproat',
        home_sp_name='Tarik Skubal',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=6.88,
        home_era=2.08,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=98, # Comerica Park
        is_dome=False,
        temp_f=58,
        wind_mph=8,
        wind_ang=225, # In from LF
        humidity=50,
        altitude=0,
        rain_intensity=0.0
    )
