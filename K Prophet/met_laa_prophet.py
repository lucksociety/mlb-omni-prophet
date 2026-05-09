import sys
import os

# Add current directory to path
sys.path.append('/Users/danielreiss/Desktop/Antigravity/K Prophet')

from k_pipeline import KProphetMaster

def run_prediction():
    master = KProphetMaster()
    
    # Mets Lineup vs RHP
    mets_lineup = [
        {'Name': 'Bo Bichette', 'Hand': 'R', 'K_pct': 15.3, 'O_Swing': 32.5, 'Z_Contact': 86.2},
        {'Name': 'Juan Soto', 'Hand': 'L', 'K_pct': 21.4, 'O_Swing': 19.8, 'Z_Contact': 84.5},
        {'Name': 'MJ Melendez', 'Hand': 'L', 'K_pct': 26.0, 'O_Swing': 34.2, 'Z_Contact': 78.5},
        {'Name': 'Francisco Alvarez', 'Hand': 'R', 'K_pct': 26.1, 'O_Swing': 31.0, 'Z_Contact': 81.2},
        {'Name': 'Brett Baty', 'Hand': 'L', 'K_pct': 27.3, 'O_Swing': 35.5, 'Z_Contact': 77.8},
        {'Name': 'Marcus Semien', 'Hand': 'R', 'K_pct': 19.2, 'O_Swing': 26.5, 'Z_Contact': 88.0},
        {'Name': 'Carson Benge', 'Hand': 'L', 'K_pct': 16.7, 'O_Swing': 28.0, 'Z_Contact': 83.5},
        {'Name': 'Tyrone Taylor', 'Hand': 'R', 'K_pct': 17.4, 'O_Swing': 31.2, 'Z_Contact': 84.0},
        {'Name': 'Ronny Mauricio', 'Hand': 'S', 'K_pct': 24.0, 'O_Swing': 38.5, 'Z_Contact': 76.0},
    ]

    # Angels Lineup vs RHP
    angels_lineup = [
        {'Name': 'Zach Neto', 'Hand': 'R', 'K_pct': 27.5, 'O_Swing': 33.8, 'Z_Contact': 80.5},
        {'Name': 'Mike Trout', 'Hand': 'R', 'K_pct': 31.4, 'O_Swing': 21.5, 'Z_Contact': 83.2},
        {'Name': 'Yoan Moncada', 'Hand': 'S', 'K_pct': 27.1, 'O_Swing': 31.5, 'Z_Contact': 81.8},
        {'Name': 'Jorge Soler', 'Hand': 'R', 'K_pct': 22.9, 'O_Swing': 29.5, 'Z_Contact': 82.5},
        {'Name': 'Nolan Schanuel', 'Hand': 'L', 'K_pct': 13.1, 'O_Swing': 23.5, 'Z_Contact': 91.2},
        {'Name': 'Jo Adell', 'Hand': 'R', 'K_pct': 26.6, 'O_Swing': 36.8, 'Z_Contact': 75.5},
        {'Name': 'Josh Lowe', 'Hand': 'L', 'K_pct': 28.2, 'O_Swing': 35.2, 'Z_Contact': 77.2},
        {'Name': 'Travis d\'Arnaud', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 33.0, 'Z_Contact': 84.5},
        {'Name': 'Adam Frazier', 'Hand': 'L', 'K_pct': 18.0, 'O_Swing': 24.5, 'Z_Contact': 92.5},
    ]

    # Pitcher Data
    scott = {
        'Name': 'Christian Scott',
        'Hand': 'R',
        'K_pct': 23.0,
        'Stuff': 105,
        'VAA': -4.5,
        'IP': 1.1,
        'ShortLeash': True
    }

    urena = {
        'Name': 'Walbert Urena',
        'Hand': 'R',
        'K_pct': 21.7,
        'Stuff': 115,
        'VAA': -4.2,
        'IP': 45.0
    }

    env = {
        'Weather': {'temp': 73, 'dome': False},
        'Umpire': {'CS_pct': 16.5},
        'ParkFactor': 1.0,
    }

    # Execute Angels vs Scott
    env['Catcher'] = {'Name': 'Francisco Alvarez'}
    res_scott = master.execute_pipeline(scott, angels_lineup, env, {'PitchLimit': 85})

    # Execute Mets vs Urena
    env['Catcher'] = {'Name': 'Travis d\'Arnaud'}
    res_urena = master.execute_pipeline(urena, mets_lineup, env, {'PitchLimit': 92})

    print("\n" + "█" + "▀"*90 + "█")
    print("█ K PROPHET V10.1 — THE SINGULARITY (METS @ ANGELS)                                     █")
    print("█" + "▄"*90 + "█")
    
    for name, res in [("Christian Scott", res_scott), ("Walbert Urena", res_urena)]:
        print(f"\nSTARTING PITCHER: {name}")
        print(f"Mean K: {res['mean_k']:.2f} | Exact K: {res['exact_k']} | Confidence: {res['confidence']*100:.1f}%")
        print(f"┌{'─'*30}┬{'─'*60}┐")
        probs = res['probabilities']
        prob_str = " | ".join([f"{line}: O {probs[line]['Over']*100:4.1f}% / U {probs[line]['Under']*100:4.1f}%" for line in [3.5, 4.5, 5.5, 6.5, 7.5]])
        print(f"│ {'Line Probabilities':<28} │ {prob_str} │")
        tel = res['telemetry']
        telemetry_str = f"BF: {tel['ExpectedBF']:.1f} | pK: {tel['Final_pK']:.3f} | Arch: {tel.get('Archetype', 'N/A')}"
        print(f"│ {'Telemetry':<28} │ {telemetry_str:<60} │")
        print(f"└{'─'*30}┴{'─'*60}┘")
    print("\n" + "="*92)

if __name__ == "__main__":
    run_prediction()
