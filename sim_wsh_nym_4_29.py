from quant_elite_v6_4 import run_v6_4_protocol

# WSH @ NYM - April 29, 2026
away_team = 'WSH'
home_team = 'NYM'
away_sp = 'Cade Cavalli'
home_sp = 'David Peterson'
away_sp_hand = 'R'
home_sp_hand = 'L'
away_era = 4.01
home_era = 5.06

wsh_lineup = [
    ('James Wood', 'L'),
    ('Curtis Mead', 'R'),
    ('Brady House', 'R'),
    ('CJ Abrams', 'L'),
    ('Jacob Young', 'R'),
    ('Daylen Lile', 'L'),
    ('Joey Wiemer', 'R'),
    ('Nasim Nunez', 'S'),
    ('Keibert Ruiz', 'S')
]

nym_lineup = [
    ('Bo Bichette', 'R'),
    ('Juan Soto', 'L'),
    ('MJ Melendez', 'L'),
    ('Francisco Alvarez', 'R'),
    ('Brett Baty', 'L'),
    ('Tyrone Taylor', 'R'),
    ('Carson Benge', 'L'),
    ('Marcus Semien', 'R'),
    ('Ronny Mauricio', 'S')
]

# Environmental Factors
park_factor = 97 # Citi Field
is_dome = False
temp_f = 54
wind_mph = 10
wind_ang = 0 # SW wind is a tailwind at Citi Field (NE orientation)
humidity = 66
altitude = 50
rain_intensity = 0.6 # 56% chance of showers

run_v6_4_protocol(away_team, home_team, away_sp, home_sp, away_sp_hand, home_sp_hand,
                  away_era, home_era, wsh_lineup, nym_lineup,
                  park_factor, is_dome, temp_f, wind_mph, wind_ang,
                  humidity, altitude, rain_intensity)
