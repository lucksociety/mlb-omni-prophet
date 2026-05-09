import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v9 import run_v9_protocol

def run_sim():
    # WSH Lineup
    wsh_lineup = [
        ('James Wood', 'L'),
        ('Luis Garcia', 'L'),
        ('Daylen Lile', 'L'),
        ('CJ Abrams', 'L'),
        ('Jose Tena', 'L'),
        ('Jorbit Vivas', 'L'),
        ('Nasim Nunez', 'S'),
        ('Drew Millas', 'S'),
        ('Jacob Young', 'R')
    ]
    
    # NYM Lineup
    nym_lineup = [
        ('Bo Bichette', 'R'),
        ('Juan Soto', 'L'),
        ('MJ Melendez', 'L'),
        ('Mark Vientos', 'R'),
        ('Brett Baty', 'L'),
        ('M. Semien', 'R'),
        ('Carson Benge', 'L'),
        ('Luis Torrens', 'R'),
        ('R. Mauricio', 'S')
    ]
    
    print("\n🚀 EXECUTING QUANT-ELITE V9.0: WSH @ NYM (4/30 Backtest)...")
    
    ar, hr, a_k, h_k = run_v9_protocol(
        away_team='WSH',
        home_team='NYM',
        away_sp_name='Miles Mikolas',
        home_sp_name='Freddy Peralta',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=8.49,
        home_era=3.90,
        away_lineup=wsh_lineup,
        home_lineup=nym_lineup,
        park_factor=96,
        is_dome=False,
        temp_f=60,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=0,
        rain_intensity=0.0,
        away_drs=1, 
        home_drs=2, 
        away_manager_hook=-0.5,
        home_manager_hook=0.0,
        away_bp_pitches_d1=0,
        away_bp_pitches_d2=0,
        home_bp_pitches_d1=0,
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='Drew Millas',
        home_catcher='Luis Torrens',
        game_time='13:10'
    )

    def print_k_table(name, dist):
        import statistics
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Miles Mikolas (WSH)', a_k)
    print_k_table('Freddy Peralta (NYM)', h_k)

if __name__ == '__main__':
    run_sim()
