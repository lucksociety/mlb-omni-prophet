from quant_elite_v6_4 import run_v6_4_protocol

# SF @ PHI - April 29, 2026
away_team = 'SF'
home_team = 'PHI'
away_sp = 'Logan Webb'
home_sp = 'C. Sanchez'
away_sp_hand = 'R'
home_sp_hand = 'L'
away_era = 4.86
home_era = 2.94

sf_lineup = [
    ('Heliot Ramos', 'R'),
    ('Matt Chapman', 'R'),
    ('Luis Arraez', 'L'),
    ('C. Schmitt', 'R'),
    ('R. Devers', 'L'),
    ('Willy Adames', 'R'),
    ('Jung Hoo Lee', 'L'),
    ('J. Encarnacion', 'R'),
    ('P. Bailey', 'S')
]

phi_lineup = [
    ('Trea Turner', 'R'),
    ('K. Schwarber', 'L'),
    ('Bryce Harper', 'L'),
    ('A. Garcia', 'R'),
    ('B. Marsh', 'L'),
    ('Bryson Stott', 'L'),
    ('Alec Bohm', 'R'),
    ('J. Crawford', 'L'),
    ('R. Marchan', 'S')
]

# Environmental Factors
park_factor = 103 # Citizens Bank Park
is_dome = False
temp_f = 60
wind_mph = 11
wind_ang = 135 # SSE wind blowing mostly in at CBP
humidity = 58
altitude = 50
rain_intensity = 0.5 # 49% chance, light showers

ar, hr, a_k, h_k = run_v6_4_protocol(away_team, home_team, away_sp, home_sp, away_sp_hand, home_sp_hand,
                                  away_era, home_era, sf_lineup, phi_lineup,
                                  park_factor, is_dome, temp_f, wind_mph, wind_ang,
                                  humidity, altitude, rain_intensity)

n = len(ar)
over_7 = sum(1 for i in range(n) if ar[i] + hr[i] > 7) / n * 100
webb_under_5_5 = sum(1 for k in a_k if k < 5.5) / n * 100
print(f"\n--- PROP PROBABILITY ---")
print(f"Game Over 7 Runs: {over_7:.1f}%")
print(f"Logan Webb Under 5.5 K: {webb_under_5_5:.1f}%")
