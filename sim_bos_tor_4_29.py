import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

AWAY_LINEUP = [
    ('Roman Anthony', 'L'),
    ('Willson Contreras', 'R'),
    ('Wilyer Abreu', 'L'),
    ('Ceddanne Rafaela', 'R'),
    ('Trevor Story', 'R'),
    ('Andruw Monasterio', 'R'),
    ('Connor Wong', 'R'),
    ('Isiah Kiner-Falefa', 'R'),
    ('Caleb Durbin', 'R')
]

HOME_LINEUP = [
    ('Ernie Clement', 'R'),
    ('Jesus Sanchez', 'L'),
    ('Vladimir Guerrero Jr.', 'R'),
    ('Kazuma Okamoto', 'R'),
    ('Daulton Varsho', 'L'),
    ('Yohendrick Pinango', 'L'),
    ('Myles Straw', 'R'),
    ('Andres Gimenez', 'L'),
    ('Brandon Valenzuela', 'S')
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='BOS',
        home_team='TOR',
        away_sp_name='Brayan Bello',
        home_sp_name='Eric Lauer',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=9.00,
        home_era=6.75,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=101,
        is_dome=True,
        temp_f=72,
        wind_mph=0,
        wind_ang=0,
        humidity=50,
        altitude=250,
        rain_intensity=0.0,
        away_drs=2,          # Neutral/Slightly above
        home_drs=1,          
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=10,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=15,
        home_bp_pitches_d2=5,
        umpire_zone='neutral'
    )
