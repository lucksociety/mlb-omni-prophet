#!/usr/bin/env python3
import sys
import os

# Add the current directory to sys.path to import quant_elite_v9
sys.path.append(os.getcwd())

from quant_elite_v9 import run_v9_protocol, ARCHETYPES, CATCHER_TIERS

# Update Archetypes and Catcher Tiers for this specific game
ARCHETYPES['Slade Cecconi'] = 'Standard'
ARCHETYPES['Jacob Lopez'] = 'Standard'
CATCHER_TIERS['Austin Hedges'] = {'framing': 1.15, 'offensive_mod': -10}
CATCHER_TIERS['Shea Langeliers'] = {'framing': 1.00, 'offensive_mod': 5}

# Game Data
away_team = 'CLE'
home_team = 'ATH'
away_sp_name = 'Slade Cecconi'
home_sp_name = 'Jacob Lopez'
away_sp_hand = 'R'
home_sp_hand = 'L'
away_era = 6.23
home_era = 5.84

# Lineups
away_lineup = [
    ('Steven Kwan', 'L'), 
    ('Angel Martinez', 'S'), 
    ('Jose Ramirez', 'S'), 
    ('Rhys Hoskins', 'R'), 
    ('David Fry', 'R'), 
    ('Travis Bazzana', 'L'), 
    ('Daniel Schneemann', 'L'), 
    ('Austin Hedges', 'R'), 
    ('Brayan Rocchio', 'S')
]

home_lineup = [
    ('Nick Kurtz', 'L'), 
    ('Shea Langeliers', 'R'), 
    ('Tyler Soderstrom', 'L'), 
    ('Brent Rooker', 'R'), 
    ('Carlos Cortes', 'L'), 
    ('Jacob Wilson', 'R'), 
    ('Jeff McNeil', 'L'), 
    ('Lawrence Butler', 'L'), 
    ('Darell Hernaiz', 'R')
]

# Run Protocol
run_v9_protocol(
    away_team=away_team,
    home_team=home_team,
    away_sp_name=away_sp_name,
    home_sp_name=home_sp_name,
    away_sp_hand=away_sp_hand,
    home_sp_hand=home_sp_hand,
    away_era=away_era,
    home_era=home_era,
    away_lineup=away_lineup,
    home_lineup=home_lineup,
    park_factor=117, # Sutter Health Park Launchpad
    is_dome=False,
    temp_f=75,
    wind_mph=6,
    wind_ang=45, # Blowing out to RF
    humidity=60,
    altitude=30,
    rain_intensity=0,
    away_drs=2, # Guardians defense slightly above avg
    home_drs=0,
    away_manager_hook=0.0,
    home_manager_hook=0.0,
    away_bp_pitches_d1=45,
    home_bp_pitches_d1=35,
    umpire_zone='neutral',
    away_catcher='Austin Hedges',
    home_catcher='Shea Langeliers',
    game_time='16:05',
    is_game_1=True
)
