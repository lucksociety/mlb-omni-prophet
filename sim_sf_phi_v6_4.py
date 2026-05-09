import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_4 import run_v6_4_protocol

def run_sim():
    # SF Lineup from confirmed lineup image
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
    
    # PHI Lineup from confirmed lineup image
    phi_lineup = [
        ('Trea Turner', 'R'),
        ('K. Schwarber', 'L'),
        ('Bryce Harper', 'L'),
        ('A. Garcia', 'R'),
        ('B. Marsh', 'L'),
        ('Bryson Stott', 'L'),
        ('Edmundo Sosa', 'R'),
        ('J. Crawford', 'L'),
        ('R. Marchan', 'S')
    ]
    
    # SF @ PHI | 12:35 PM ET
    # SF SP: Logan Webb (R), 4.86 ERA
    # PHI SP: Cristopher Sánchez (L), 2.94 ERA
    # Weather: Assuming 60F, 5mph (Citizens Bank Park)
    
    print("\n🚀 EXECUTING QUANT-ELITE V6.4: SF @ PHI...")
    
    ar, hr, a_k, h_k = run_v6_4_protocol(
        away_team='SF',
        home_team='PHI',
        away_sp_name='Logan Webb',
        home_sp_name='Cristopher Sánchez',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=4.86,
        home_era=2.94,
        away_lineup=sf_lineup,
        home_lineup=phi_lineup,
        park_factor=104, # Citizens Bank Park
        is_dome=False,
        temp_f=60,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=0,
        rain_intensity=0.0,
        away_drs=4, 
        home_drs=3, 
        away_manager_hook=0.0,
        home_manager_hook=0.0,
        away_bp_pitches_d1=0,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='Patrick Bailey', # God tier framing
        home_catcher='R. Marchan',
        game_time='12:35'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Logan Webb (SF)', a_k)
    print_k_table('Cristopher Sánchez (PHI)', h_k)

if __name__ == '__main__':
    run_sim()
