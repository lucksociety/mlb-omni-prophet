from quant_elite_v6_1 import run_v6_1_protocol

# COL @ NYM - April 24, 2026
COL_LINEUP = [
    ('Mickey Moniak', 'L'), ('Hunter Goodman', 'R'), ('TJ Rumfield', 'L'),
    ('Tyler Freeman', 'R'), ('Troy Johnston', 'L'), ('Kyle Karros', 'R'),
    ('Ezequiel Tovar', 'R'), ('Jake McCarthy', 'L'), ('Brenton Doyle', 'R')
]

NYM_LINEUP = [
    ('Bo Bichette', 'R'), ('Juan Soto', 'L'), ('Francisco Alvarez', 'R'),
    ('Brett Baty', 'L'), ('Mark Vientos', 'R'), ('Marcus Semien', 'R'),
    ('Carson Benge', 'L'), ('Tyrone Taylor', 'R'), ('Ronny Mauricio', 'S')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='COL',
        home_team='NYM',
        away_sp_name='Michael Lorenzen',
        home_sp_name='Freddy Peralta',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=7.48,
        home_era=4.05,
        away_lineup=COL_LINEUP,
        home_lineup=NYM_LINEUP,
        park_factor=96,
        is_dome=False,
        temp_f=51,
        wind_mph=8,
        wind_ang=90, 
        humidity=65,
        altitude=15,
        rain_intensity=0.05
    )
