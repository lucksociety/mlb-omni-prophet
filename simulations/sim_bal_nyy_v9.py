#!/usr/bin/env python3
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import os

# Add current directory to path to import quant_elite_v9
sys.path.append(os.getcwd())

import quant_elite_v9 as qe

# --- 1. RESEARCH AUDIT OVERRIDE (2026-05-02) ---

# Update Archetypes for the matchup
qe.ARCHETYPES['Kyle Bradish'] = 'Unicorn'
qe.ARCHETYPES['Ryan Weathers'] = 'North-South'

# Catcher Tiers update for 2026 ABS System
qe.CATCHER_TIERS['Adley Rutschman'] = {'framing': 1.0, 'offensive_mod': 5} # ABS neutralizes framing, offense remains
qe.CATCHER_TIERS['J.C. Escarra'] = {'framing': 1.0, 'offensive_mod': 0}

# --- 2. LINEUP CONFIGURATION ---

# Baltimore Orioles (Away)
away_lineup = [
    ('Taylor Ward', 'R'),
    ('Gunnar Henderson', 'L'),
    ('Adley Rutschman', 'S'),
    ('Pete Alonso', 'R'),
    ('Tyler O\'Neill', 'R'),
    ('Jeremiah Jackson', 'R'),
    ('Leody Taveras', 'S'),
    ('Coby Mayo', 'R'),
    ('Blaze Alexander', 'R')
]

# New York Yankees (Home)
home_lineup = [
    ('Trent Grisham', 'L'),
    ('Ben Rice', 'L'),
    ('Aaron Judge', 'R'),
    ('Cody Bellinger', 'L'),
    ('Jazz Chisholm Jr.', 'L'),
    ('Jasson Domínguez', 'S'),
    ('J.C. Escarra', 'L'),
    ('Ryan McMahon', 'L'),
    ('José Caballero', 'R')
]

# --- 3. EXECUTE PROTOCOL ---

if __name__ == '__main__':
    qe.run_v9_protocol(
        away_team='BAL',
        home_team='NYY',
        away_sp_name='Kyle Bradish',
        home_sp_name='Ryan Weathers',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=4.20,
        home_era=3.21,
        away_lineup=away_lineup,
        home_lineup=home_lineup,
        park_factor=105,      # Yankee Stadium Short Porch / Hitter Friendly
        is_dome=False,
        temp_f=56,            # Cloudy, May in NYC
        wind_mph=10,          # Out to Right/Center
        wind_ang=45,          # Vector towards RF
        humidity=60,
        altitude=50,
        rain_intensity=0,     # Cloudy but no active rain expected for start
        away_drs=10,          # BAL solid defense
        home_drs=15,          # NYY elite defense
        away_manager_hook=0.2, # Bradish returning from injury, cautious hook
        home_manager_hook=0.0,
        away_bp_pitches_d1=0,  # Top arms rested
        away_bp_pitches_d2=15, 
        home_bp_pitches_d1=0,  # Top arms rested
        home_bp_pitches_d2=12,
        umpire_zone='neutral', # ABS System active
        away_catcher='Adley Rutschman',
        home_catcher='J.C. Escarra',
        game_time='13:35',
        is_game_1=True
    )