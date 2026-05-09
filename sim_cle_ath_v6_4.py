import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

# --- GAME DATA: CLE @ ATH (May 1, 2026) ---
# Location: Sutter Health Park, West Sacramento (Hitter Friendly)

# Lineups
cle_lineup = [
    ('Steven Kwan', 'L'),
    ('C. DeLauter', 'L'),
    ('Jose Ramirez', 'S'),
    ('K. Manzardo', 'L'),
    ('Rhys Hoskins', 'R'),
    ('D. Schneemann', 'L'),
    ('T. Bazzana', 'L'),
    ('Bo Naylor', 'L'),
    ('B. Rocchio', 'S')
]

ath_lineup = [
    ('Jacob Wilson', 'R'),
    ('S. Langeliers', 'R'),
    ('Nick Kurtz', 'L'),
    ('Brent Rooker', 'R'),
    ('D. Hernaiz', 'R'),
    ('T. Soderstrom', 'L'),
    ('Colby Thomas', 'R'),
    ('Zack Gelof', 'R'),
    ('Jeff McNeil', 'L')
]

# Run Simulation
if __name__ == "__main__":
    run_v6_4_protocol(
        away_team='CLE',
        home_team='ATH',
        away_sp_name='Joey Cantillo',
        home_sp_name='J.T. Ginn',
        away_sp_hand='L',
        home_sp_hand='R',
        away_era=2.97,
        home_era=3.24,
        away_lineup=cle_lineup,
        home_lineup=ath_lineup,
        park_factor=105, # Sutter Health Park (Hitter Friendly)
        is_dome=False,
        temp_f=77,
        wind_mph=6,
        wind_ang=0, # Blowing out to center
        humidity=35,
        altitude=30,
        rain_intensity=0.0,
        away_drs=5, # Guardians defense is elite
        home_drs=0,
        away_manager_hook=0.2, # Vogt trusts his guys
        home_manager_hook=-0.2, # Kotsay hooks Ginn early
        away_bp_pitches_d1=15,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=25,
        home_bp_pitches_d2=15,
        umpire_zone='neutral',
        away_catcher='Bo Naylor',
        home_catcher='S. Langeliers',
        game_time='19:00'
    )
