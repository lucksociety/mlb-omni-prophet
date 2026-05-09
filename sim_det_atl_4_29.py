from quant_elite_v6_4 import run_v6_4_protocol

# DET @ ATL - April 29, 2026
away_team = 'DET'
home_team = 'ATL'
away_sp = 'Tarik Skubal'
home_sp = 'JR Ritchie'
away_sp_hand = 'L'
home_sp_hand = 'R'
away_era = 2.72
home_era = 2.57

det_lineup = [
    ('K. McGonigle', 'L'),
    ('Gleyber Torres', 'R'),
    ('Colt Keith', 'L'),
    ('Riley Greene', 'L'),
    ('Dillon Dingler', 'R'),
    ('Kerry Carpenter', 'L'),
    ('Spencer Torkelson', 'R'),
    ('W. Perez', 'S'),
    ('Jace Jung', 'L')
]

atl_lineup = [
    ('Ronald Acuna', 'R'),
    ('D. Baldwin', 'L'),
    ('Ozzie Albies', 'S'),
    ('Matt Olson', 'L'),
    ('Austin Riley', 'R'),
    ('Mauricio Dubon', 'R'),
    ('Michael Harris', 'L'),
    ('Eli White', 'R'),
    ('Jonah Heim', 'S')
]

# Environmental Factors
park_factor = 101 # Truist Park
is_dome = False
temp_f = 79
wind_mph = 12
wind_ang = 90 # WNW wind is a crosswind at Truist Park
humidity = 60
altitude = 1000
rain_intensity = 0.8 # 51% chance, thunderstorms expected

run_v6_4_protocol(away_team, home_team, away_sp, home_sp, away_sp_hand, home_sp_hand,
                  away_era, home_era, det_lineup, atl_lineup,
                  park_factor, is_dome, temp_f, wind_mph, wind_ang,
                  humidity, altitude, rain_intensity)
