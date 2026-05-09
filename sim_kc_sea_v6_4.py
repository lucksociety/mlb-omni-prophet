import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

# --- GAME DATA: KC @ SEA (May 1, 2026) ---
# Location: T-Mobile Park, Seattle (Roof Closed, Pitcher Friendly)

# Lineups
kc_lineup = [
    ('M. Garcia', 'R'),
    ('Bobby Witt', 'R'),
    ('V. Pasquantino', 'L'),
    ('S. Perez', 'R'),
    ('C. Jensen', 'L'),
    ('J. Caglianone', 'L'),
    ('I. Collins', 'S'),
    ('M. Massey', 'L'),
    ('Kyle Isbel', 'L')
]

sea_lineup = [
    ('J. Crawford', 'L'),
    ('Cal Raleigh', 'S'),
    ('J. Rodriguez', 'R'),
    ('Josh Naylor', 'L'),
    ('R. Arozarena', 'R'),
    ('Mitch Garver', 'R'),
    ('Cole Young', 'L'),
    ('Connor Joe', 'R'),
    ('Leo Rivas', 'S')
]

# Run Simulation
if __name__ == "__main__":
    run_v6_4_protocol(
        away_team='KC',
        home_team='SEA',
        away_sp_name='Cole Ragans',
        home_sp_name='Bryan Woo',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=5.00,
        home_era=3.86,
        away_lineup=kc_lineup,
        home_lineup=sea_lineup,
        park_factor=92, # T-Mobile Park (Pitcher Friendly)
        is_dome=True, # Roof Closed
        temp_f=70, # Controlled environment
        wind_mph=0,
        wind_ang=0,
        humidity=45,
        altitude=10,
        rain_intensity=0.0,
        away_drs=0,
        home_drs=2,
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=30, # Struggling bullpen
        away_bp_pitches_d2=15,
        home_bp_pitches_d1=40, # Heavy usage recently
        home_bp_pitches_d2=25,
        umpire_zone='neutral', # ABS System active
        away_catcher='S. Perez',
        home_catcher='Cal Raleigh',
        game_time='18:40'
    )
