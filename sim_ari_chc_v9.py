#!/usr/bin/env python3
import sys
import os

# Add current directory to path to import quant_elite_v9
sys.path.append(os.getcwd())

import quant_elite_v9 as qe

# --- 1. RESEARCH AUDIT OVERRIDE (2026-05-02) ---

# Update Archetypes for the matchup
qe.ARCHETYPES['Shota Imanaga'] = 'Unicorn'
qe.ARCHETYPES['Ryne Nelson'] = 'Standard'

# Catcher Tiers update for 2026
qe.CATCHER_TIERS['Carson Kelly'] = {'framing': 1.10, 'offensive_mod': 0}
qe.CATCHER_TIERS['James McCann'] = {'framing': 0.98, 'offensive_mod': -5}

# --- 2. LINEUP CONFIGURATION ---

# Arizona Diamondbacks (Away)
away_lineup = [
    ('Ketel Marte', 'S'),
    ('Geraldo Perdomo', 'S'),
    ('Corbin Carroll', 'L'),
    ('Ildemaro Vargas', 'S'),
    ('Lourdes Gurriel Jr.', 'R'),
    ('Nolan Arenado', 'R'),
    ('Jose Fernandez', 'R'),
    ('James McCann', 'R'),
    ('Jorge Barrosa', 'S')
]

# Chicago Cubs (Home)
home_lineup = [
    ('Nico Hoerner', 'R'),
    ('Michael Busch', 'L'),
    ('Alex Bregman', 'R'),
    ('Ian Happ', 'S'),
    ('Seiya Suzuki', 'R'),
    ('Moisés Ballesteros', 'L'),
    ('Carson Kelly', 'R'),
    ('Pete Crow-Armstrong', 'L'),
    ('Dansby Swanson', 'R')
]

# --- 3. EXECUTE PROTOCOL ---

if __name__ == '__main__':
    qe.run_v9_protocol(
        away_team='ARI',
        home_team='CHC',
        away_sp_name='Ryne Nelson',
        home_sp_name='Shota Imanaga',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=7.71,
        home_era=3.15,
        away_lineup=away_lineup,
        home_lineup=home_lineup,
        park_factor=102,      # Wrigley Field
        is_dome=False,
        temp_f=50,            # Partly Cloudy, Cool
        wind_mph=8,           # Blowing in from ENE (Right Field)
        wind_ang=67,          # ENE Angle
        humidity=50,
        altitude=600,
        rain_intensity=0,
        away_drs=5,           
        home_drs=12,          # Cubs defense remains elite
        away_manager_hook=-0.2, # Nelson on short leash due to 7.71 ERA
        home_manager_hook=0.3,  # Imanaga has elite leash
        away_bp_pitches_d1=45,  # Heavy fatigue
        away_bp_pitches_d2=20, 
        home_bp_pitches_d1=40,  # Heavy fatigue
        home_bp_pitches_d2=25,
        umpire_zone='neutral',  # Gabe Morales
        away_catcher='James McCann',
        home_catcher='Carson Kelly',
        game_time='14:20',
        is_game_1=False        # Middle of series
    )
