import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

# --- GAME DATA: CWS @ SD (May 1, 2026) ---
# Location: Petco Park, San Diego (Pitcher Friendly)

# Lineups
cws_lineup = [
    ('A. Benintendi', 'L'),
    ('M. Murakami', 'L'),
    ('M. Vargas', 'R'),
    ('C. Montgomery', 'L'),
    ('C. Meidroth', 'R'),
    ('S. Antonacci', 'L'),
    ('Austin Hays', 'R'),
    ('T. Peters', 'L'),
    ('Drew Romo', 'S')
]

sd_lineup = [
    ('R. Laureano', 'R'),
    ('F. Tatis', 'R'),
    ('M. Andujar', 'R'),
    ('M. Machado', 'R'),
    ('X. Bogaerts', 'R'),
    ('Ty France', 'R'),
    ('N. Castellanos', 'R'),
    ('F. Fermin', 'R'),
    ('B. Johnson', 'S')
]

# Run Simulation
if __name__ == "__main__":
    run_v6_4_protocol(
        away_team='CWS',
        home_team='SD',
        away_sp_name='Noah Schultz',
        home_sp_name='German Marquez',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=3.52,
        home_era=4.38,
        away_lineup=cws_lineup,
        home_lineup=sd_lineup,
        park_factor=94, # Petco Park (Pitcher Friendly)
        is_dome=False,
        temp_f=65,
        wind_mph=7,
        wind_ang=90, # Crosswind (Left to Right)
        humidity=60,
        altitude=15,
        rain_intensity=0.0,
        away_drs=0,
        home_drs=3, # Padres defense is solid
        away_manager_hook=-0.5, # Grifol/V6 logic: hook Schultz early to protect arm
        home_manager_hook=0.0,
        away_bp_pitches_d1=20,
        away_bp_pitches_d2=10,
        home_bp_pitches_d1=30,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='Drew Romo',
        home_catcher='F. Fermin',
        game_time='19:10'
    )
