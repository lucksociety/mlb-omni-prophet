#!/usr/bin/env python3
import sys
import os

# Add current directory to path to import quant_elite_v9
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from quant_elite_v9 import run_v9_protocol

# TOR @ MIN | May 2, 2026
# Dylan Cease (R) vs Connor Prielipp (L)

away_team = 'TOR'
home_team = 'MIN'
away_sp_name = 'Dylan Cease'
home_sp_name = 'Connor Prielipp'
away_sp_hand = 'R'
home_sp_hand = 'L'
away_era = 2.87
home_era = 4.00

# Lineups (Names and Hand)
away_lineup = [
    ('George Springer', 'R'),
    ('Ernie Clement', 'R'),
    ('Vladimir Guerrero Jr.', 'R'),
    ('Kazuma Okamoto', 'R'),
    ('Lenyn Sosa', 'R'),
    ('Daulton Varsho', 'L'),
    ('Myles Straw', 'R'),
    ('Davis Schneider', 'R'),
    ('Brandon Valenzuela', 'S')
]

home_lineup = [
    ('Byron Buxton', 'R'),
    ('Trevor Larnach', 'L'),
    ('Josh Bell', 'S'),
    ('Ryan Jeffers', 'R'),
    ('Kody Clemens', 'L'),
    ('Luke Keaschall', 'R'),
    ('Matt Wallner', 'L'),
    ('Brooks Lee', 'S'),
    ('Tristan Gray', 'L')
]

# Environmental Physics
park_factor = 102
is_dome = False
temp_f = 53
wind_mph = 6
wind_ang = 340 # NNW (Blowing in/sideways)
humidity = 60
altitude = 800 # Minneapolis is ~800ft
rain_intensity = 0

# Logistics & Hooks
away_drs = 5 # TOR defense is solid
home_drs = -2 # MIN defense with some rookies/recovering players
away_manager_hook = 0.5 # Schneider tends to let starters go
home_manager_hook = -0.3 # Rocco is quicker with the hook, especially with Prielipp on a count

# Bullpen Fatigue (Estimated based on 2026 season context)
away_bp_pitches_d1 = 15
away_bp_pitches_d2 = 20
home_bp_pitches_d1 = 30
home_bp_pitches_d2 = 45 # MIN BP might be slightly more taxed

# Human Element
umpire_zone = 'wide' # Jacob Metz (Neutral/Wide)
away_catcher = 'Brandon Valenzuela'
home_catcher = 'Ryan Jeffers'

# Execution
ar, hr, a_k, h_k = run_v9_protocol(
    away_team, home_team, away_sp_name, home_sp_name,
    away_sp_hand, home_sp_hand, away_era, home_era,
    away_lineup, home_lineup, park_factor, is_dome, temp_f, wind_mph, wind_ang,
    humidity, altitude, rain_intensity,
    away_drs, home_drs, away_manager_hook, home_manager_hook,
    away_bp_pitches_d1, away_bp_pitches_d2, home_bp_pitches_d1, home_bp_pitches_d2,
    umpire_zone, away_catcher, home_catcher,
    game_time='14:10', is_game_1=True
)
