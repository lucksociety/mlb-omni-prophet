import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v9 import run_v9_protocol

def run_sim():
    # TOR Blue Jays Lineup (Confirmed 04/30)
    tor_lineup = [
        ('George Springer', 'R'),
        ('Jesus Sanchez', 'L'),
        ('Vladimir Guerrero Jr.', 'R'),
        ('Kazuma Okamoto', 'R'),
        ('Daulton Varsho', 'L'),
        ('Ernie Clement', 'R'),
        ('Yohendrick Pinango', 'L'),
        ('Andres Gimenez', 'L'),
        ('Brandon Valenzuela', 'S')
    ]
    
    # MN Twins Lineup (Confirmed 04/30)
    min_lineup = [
        ('Byron Buxton', 'R'),
        ('Trevor Larnach', 'L'),
        ('Ryan Jeffers', 'R'),
        ('Josh Bell', 'S'),
        ('Austin Martin', 'R'),
        ('Kody Clemens', 'L'),
        ('Luke Keaschall', 'R'),
        ('Brooks Lee', 'S'),
        ('Royce Lewis', 'R')
    ]
    
    # Kevin Gausman (TOR): 2.57 ERA
    # Bailey Ober (MIN): 3.94 ERA
    
    print("\n🚀 EXECUTING QUANT-ELITE V9.0: TOR @ MIN...")
    
    ar, hr, a_k, h_k = run_v9_protocol(
        away_team='TOR',
        home_team='MIN',
        away_sp_name='Kevin Gausman',
        home_sp_name='Bailey Ober',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=2.57,
        home_era=3.94,
        away_lineup=tor_lineup,
        home_lineup=min_lineup,
        park_factor=102, # Target Field
        is_dome=False,
        temp_f=52, # Cool night
        wind_mph=9, # Across diamond
        wind_ang=90, 
        humidity=45,
        altitude=812,
        rain_intensity=0.0,
        away_drs=5, # Elite Blue Jays D
        home_drs=1, 
        away_manager_hook=0.5, # Ace hook
        home_manager_hook=-1.0, # Twins thin bullpen / Ober early pull if laboring
        away_bp_pitches_d1=12,
        away_bp_pitches_d2=20,
        home_bp_pitches_d1=25, # Tired arms (Duran/Jax)
        home_bp_pitches_d2=20,
        umpire_zone='neutral',
        away_catcher='Brandon Valenzuela',
        home_catcher='Ryan Jeffers',
        game_time='19:40'
    )
    gausman_k_under_5_5 = sum(1 for k in a_k if k < 5.5) / len(a_k) * 100
    ober_k_over_3_5 = sum(1 for k in h_k if k > 3.5) / len(h_k) * 100
    
    print(f"\n🎯 BET PROBABILITIES:")
    print(f"  Gausman Under 5.5 K: {gausman_k_under_5_5:.1f}%")
    print(f"  Ober Over 3.5 K: {ober_k_over_3_5:.1f}%")

if __name__ == '__main__':
    run_sim()
