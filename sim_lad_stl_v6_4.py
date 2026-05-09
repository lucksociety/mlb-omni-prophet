import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

LAD_LINEUP = [
    ('Shohei Ohtani', 'L'), ('Freddie Freeman', 'L'), ('Will Smith', 'R'),
    ('Kyle Tucker', 'L'), ('Teoscar Hernandez', 'R'), ('Max Muncy', 'L'),
    ('Andy Pages', 'R'), ('Hyeseong Kim', 'L'), ('Alex Freeland', 'S'),
]

STL_LINEUP = [
    ('JJ Wetherholt', 'L'), ('Ivan Herrera', 'R'), ('Alec Burleson', 'L'),
    ('Jordan Walker', 'R'), ('Nolan Gorman', 'L'), ('Masyn Winn', 'R'),
    ('Nathan Church', 'L'), ('Ramon Urias', 'R'), ('Victor Scott', 'L'),
]

if __name__ == '__main__':
    run_v6_4_protocol(
        away_team='LAD',
        home_team='STL',
        away_sp_name='Roki Sasaki',
        home_sp_name='Michael McGreevy',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=6.35,
        home_era=4.05,
        away_lineup=LAD_LINEUP,
        home_lineup=STL_LINEUP,
        park_factor=98,
        is_dome=False,
        temp_f=56,
        wind_mph=9,
        wind_ang=340, # NNW
        humidity=52,
        altitude=465, # STL elevation
        rain_intensity=0.0,
        away_drs=5,          # Elite LAD defense
        home_drs=2,          # Average STL defense
        away_manager_hook=0.2, 
        home_manager_hook=0.0,
        away_bp_pitches_d1=15, 
        away_bp_pitches_d2=10,
        home_bp_pitches_d1=20, 
        home_bp_pitches_d2=5,
        umpire_zone='neutral', # Nestor Ceja is pitcher-friendly but logic will handle mods
        away_catcher='Will Smith',
        home_catcher='Ivan Herrera'
    )
