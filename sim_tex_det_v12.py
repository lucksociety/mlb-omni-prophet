
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import quant_elite_v6_5

# Update Archetypes and Catcher Tiers based on V12.0 Research
quant_elite_v6_5.ARCHETYPES['Kumar Rocker'] = 'East-West'
quant_elite_v6_5.ARCHETYPES['Keider Montero'] = 'North-South'

# Catcher Tiers
quant_elite_v6_5.CATCHER_TIERS['Danny Jansen'] = 1.05 # Tier 2
quant_elite_v6_5.CATCHER_TIERS['Dillon Dingler'] = 0.95 # Tier 3

AWAY_LINEUP = [
    ('Evan Carter', 'L'), ('Corey Seager', 'L'), ('Josh Jung', 'R'),
    ('Joc Pederson', 'L'), ('Jake Burger', 'R'), ('A. Osuna', 'L'),
    ('E. Duran', 'R'), ('Josh Smith', 'L'), ('Danny Jansen', 'R')
]

HOME_LINEUP = [
    ('K. McGonigle', 'L'), ('G. Torres', 'R'), ('Colt Keith', 'L'),
    ('Riley Greene', 'L'), ('D. Dingler', 'R'), ('K. Carpenter', 'L'),
    ('S. Torkelson', 'R'), ('W. Perez', 'S'), ('Jace Jung', 'L')
]

if __name__ == '__main__':
    quant_elite_v6_5.run_v6_5_protocol(
        away_team='TEX',
        home_team='DET',
        away_sp_name='Kumar Rocker',
        home_sp_name='Keider Montero',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.38,
        home_era=4.00,
        away_lineup=AWAY_LINEUP,
        home_lineup=HOME_LINEUP,
        park_factor=98,
        is_dome=False,
        temp_f=46,
        wind_mph=8,
        wind_ang=0, # Wind 8 mph Out
        humidity=42,
        altitude=600, # Detroit approx
        rain_intensity=0.01,
        away_drs=2,
        home_drs=-1,
        away_manager_hook=0.5, # Bullpen fatigue means longer leash
        home_manager_hook=0.5,
        away_bp_pitches_d1=120, # Very tired
        away_bp_pitches_d2=40,
        home_bp_pitches_d1=130, # Very tired
        home_bp_pitches_d2=45,
        umpire_zone='neutral',
        away_catcher='Danny Jansen',
        home_catcher='Dillon Dingler',
        game_time='19:15'
    )
