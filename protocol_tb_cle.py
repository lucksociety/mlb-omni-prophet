import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

AWAY_LINEUP = [
    ('C. Simpson', 'L'), ('J. Caminero', 'R'), ('J. Aranda', 'L'),
    ('Yandy Diaz', 'R'), ('Jake Fraley', 'L'), ('C. Mullins', 'L'),
    ('R. Palacios', 'L'), ('H. Feduccia', 'L'), ('Taylor Walls', 'S')
]

HOME_LINEUP = [
    ('Steven Kwan', 'L'), ('C. DeLauter', 'L'), ('Jose Ramirez', 'S'),
    ('K. Manzardo', 'L'), ('D. Schneemann', 'L'), ('A. Martinez', 'S'),
    ('T. Bazzana', 'L'), ('Bo Naylor', 'L'), ('B. Rocchio', 'S')
]

if __name__ == '__main__':
    # Environmental Data: 56°F, 11 mph Wind, 68% Rain Risk
    # Pitchers: Rasmussen (2.45) vs Williams (3.28)
    run_v6_4_protocol(
        away_team='TBR',
        home_team='CLE',
        away_sp_name='Drew Rasmussen',
        home_sp_name='Gavin Williams',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.45,
        home_era=3.28,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=95,
        is_dome=False,
        temp_f=56,
        wind_mph=11,
        wind_ang=45, # Diagonal Out
        humidity=65,
        altitude=600,
        rain_intensity=0.2, # Light rain/delay risk
        away_drs=2,
        home_drs=4,
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=10,
        away_bp_pitches_d2=5,
        home_bp_pitches_d1=15,
        home_bp_pitches_d2=0,
        umpire_zone='neutral'
    )
