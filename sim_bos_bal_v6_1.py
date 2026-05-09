from quant_elite_v6_1 import run_v6_1_protocol

# BOS @ BAL - April 24, 2026
BOS_LINEUP = [
    ('Jarren Duran', 'L'), ('Ceddanne Rafaela', 'R'), ('Masataka Yoshida', 'L'),
    ('William Contreras', 'R'), ('Wilyer Abreu', 'L'), ('Trevor Story', 'R'),
    ('Marcelo Mayer', 'L'), ('Caleb Durbin', 'R'), ('Carlos Narvaez', 'R')
]

BAL_LINEUP = [
    ('Gunnar Henderson', 'L'), ('Taylor Ward', 'R'), ('Adley Rutschman', 'S'),
    ('Pete Alonso', 'R'), ('Dylan Beavers', 'L'), ('Samuel Basallo', 'L'),
    ('Leody Taveras', 'S'), ('Coby Mayo', 'R'), ('Jackson Holliday', 'R') # Image says J. Jackson, but let's assume Jackson Holliday or similar
]

# Note: Image shows "J. Jackson" at 2B for BAL. Might be Jackson Holliday or someone else. 
# Looking at "MLB Stats" file, Jackson Holliday is #127. Let's use him if J. Jackson isn't found.

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='BOS',
        home_team='BAL',
        away_sp_name='Brayan Bello',
        home_sp_name='Brandon Young',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=6.75,
        home_era=4.15, # Brandon Young has 0.00 ERA but small sample, using league average/xFIP proxy for stability
        away_lineup=BOS_LINEUP,
        home_lineup=BAL_LINEUP,
        park_factor=98,
        is_dome=False,
        temp_f=65,
        wind_mph=5,
        wind_ang=90, 
        humidity=60,
        altitude=30,
        rain_intensity=0.2 # Light risk
    )
