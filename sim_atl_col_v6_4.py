import sys
import os

# Add workspace to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

if __name__ == '__main__':
    # ── ATL LINEUP (Confirmed 2026-05-01) ──
    away_lineup = [
        ('Ronald Acuna', 'R'), 
        ('Drake Baldwin', 'L'), 
        ('Ozzie Albies', 'S'), 
        ('Matt Olson', 'L'), 
        ('Mauricio Dubon', 'R'), 
        ('Austin Riley', 'R'), 
        ('Eli White', 'R'), 
        ('Jonah Heim', 'S'), 
        ('Jorge Mateo', 'R')
    ]
    
    # ── COL LINEUP (Confirmed 2026-05-01) ──
    home_lineup = [
        ('Edouard Julien', 'L'), 
        ('Mickey Moniak', 'L'), 
        ('Hunter Goodman', 'R'), 
        ('TJ Rumfield', 'L'), 
        ('Tyler Freeman', 'R'), 
        ('Troy Johnston', 'L'), 
        ('Willi Castro', 'S'), 
        ('Ezequiel Tovar', 'R'), 
        ('Jake McCarthy', 'L')
    ]
    
    # Run Protocol V6.4
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='ATL',
        home_team='COL',
        away_sp_name='Grant Holmes',
        home_sp_name='Jose Quintana',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=3.62,
        home_era=4.91,
        away_lineup=away_lineup,
        home_lineup=home_lineup,
        park_factor=115,    # Coors Field
        is_dome=False,
        temp_f=60,
        wind_mph=6,
        wind_ang=90,        # Out to CF
        humidity=50,
        altitude=5280,      # Denver
        rain_intensity=0.0,
        away_drs=5,         # Braves Infield
        home_drs=-5,        # Rockies Defense tax
        away_manager_hook=0.2, # Snitker Hook
        home_manager_hook=-0.2, # Black's Veteran Leash
        away_bp_pitches_d1=12, # Recent usage
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=25,
        home_bp_pitches_d2=10,
        umpire_zone='neutral',
        away_catcher='Jonah Heim',
        home_catcher='Hunter Goodman',
        game_time='18:40'
    )
    
    # Extra Analysis
    import statistics
    print(f"\n── DEBUG DATA ───────────────────────────────────────────────────")
    print(f"  ATL Run Distribution: Med={statistics.median(ar)}, Std={statistics.stdev(ar):.2f}")
    print(f"  COL Run Distribution: Med={statistics.median(hr)}, Std={statistics.stdev(hr):.2f}")
