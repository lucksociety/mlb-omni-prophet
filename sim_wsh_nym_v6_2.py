import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

def run_sim():
    # WSH Lineup from screenshot
    wsh_lineup = [
        ('James Wood', 'L'),
        ('Luis Garcia', 'L'),
        ('Brady House', 'R'),
        ('CJ Abrams', 'L'),
        ('Daylen Lile', 'L'),
        ('Jacob Young', 'R'),
        ('Nasim Nunez', 'S'),
        ('Jose Tena', 'L'),
        ('Keibert Ruiz', 'S')
    ]
    
    # NYM Lineup from screenshot
    nym_lineup = [
        ('Bo Bichette', 'R'),
        ('Juan Soto', 'L'),
        ('F. Alvarez', 'R'),
        ('Luis Robert', 'R'),
        ('Brett Baty', 'L'),
        ('Mark Vientos', 'R'),
        ('M. Semien', 'R'),
        ('Carson Benge', 'L'),
        ('R. Mauricio', 'S')
    ]
    
    # Game 7: WSH @ NYM
    # WSH SP: Zack Littell (R), 7.56 ERA
    # NYM SP: Clay Holmes (R), 2.10 ERA
    # Weather: Assuming 68F, 5mph (Citi Field)
    
    ar, hr, a_k, h_k = run_v6_2_protocol(
        away_team='WSN',
        home_team='NYM',
        away_sp_name='Zack Littell',
        home_sp_name='Clay Holmes',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=7.56,
        home_era=2.10,
        away_lineup=wsh_lineup,
        home_lineup=nym_lineup,
        park_factor=96, # Citi Field
        is_dome=False,
        temp_f=68,
        wind_mph=5,
        wind_ang=90,
        humidity=50,
        altitude=50,
        rain_intensity=0.0
    )

    def print_k_table(name, dist):
        print(f"\nSTRIKEOUT O/U PROBABILITIES: {name}")
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over = sum(1 for k in dist if k > line) / len(dist) * 100
            print(f"  Line {line:3.1f}: Over {over:5.1f}% | Under {100-over:5.1f}%")

    print_k_table('Zack Littell (WSH)', a_k)
    print_k_table('Clay Holmes (NYM)', h_k)

if __name__ == '__main__':
    run_sim()
