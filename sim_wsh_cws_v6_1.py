import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_1 import run_v6_1_protocol

# WSH Confirmed Lineup
WSH_LINEUP = [
    ('James Wood', 'L'), 
    ('Curtis Mead', 'R'), 
    ('A. Chaparro', 'R'), 
    ('Brady House', 'R'), 
    ('Daylen Lile', 'L'), 
    ('Jacob Young', 'R'), 
    ('Joey Wiemer', 'R'), 
    ('Nasim Nunez', 'S'), 
    ('Keibert Ruiz', 'S')
]

# CWS Confirmed Lineup
CWS_LINEUP = [
    ('A. Benintendi', 'L'), 
    ('M. Murakami', 'L'), 
    ('M. Vargas', 'R'), 
    ('C. Montgomery', 'L'), 
    ('E. Pereira', 'R'), 
    ('S. Antonacci', 'L'), 
    ('C. Meidroth', 'R'), 
    ('T. Peters', 'L'), 
    ('Edgar Quero', 'S')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='WSH',
        home_team='CWS',
        away_sp_name='Jake Irvin',
        home_sp_name='Noah Schultz',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=6.00,
        home_era=3.86,
        away_lineup=WSH_LINEUP,
        home_lineup=CWS_LINEUP,
        park_factor=104, # Guaranteed Rate Field
        is_dome=False,
        temp_f=57,
        wind_mph=7,
        wind_ang=150, # Blowing somewhat in from NNE
        humidity=55,
        altitude=594,
        rain_intensity=0.0
    )
