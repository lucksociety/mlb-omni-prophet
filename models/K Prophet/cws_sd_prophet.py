import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import os

# Add current directory to path
sys.path.append('/Users/danielreiss/Desktop/Antigravity/K Prophet')

from k_pipeline import KProphetMaster

def run_prediction():
    master = KProphetMaster()
    
    # White Sox Lineup vs RHP
    cws_lineup = [
        {'Name': 'Andrew Benintendi', 'Hand': 'L', 'K_pct': 22.3, 'O_Swing': 34.6, 'Z_Contact': 81.5},
        {'Name': 'Munetaka Murakami', 'Hand': 'L', 'K_pct': 33.8, 'O_Swing': 18.0, 'Z_Contact': 56.8},
        {'Name': 'Miguel Vargas', 'Hand': 'R', 'K_pct': 17.1, 'O_Swing': 32.7, 'Z_Contact': 83.5},
        {'Name': 'Colson Montgomery', 'Hand': 'L', 'K_pct': 29.2, 'O_Swing': 35.0, 'Z_Contact': 75.0}, # Normalized
        {'Name': 'Chase Meidroth', 'Hand': 'R', 'K_pct': 15.7, 'O_Swing': 23.0, 'Z_Contact': 90.0},
        {'Name': 'Sam Antonacci', 'Hand': 'L', 'K_pct': 18.1, 'O_Swing': 35.0, 'Z_Contact': 80.0}, # Adjusted from outlier
        {'Name': 'Austin Hays', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 33.0, 'Z_Contact': 82.0},
        {'Name': 'Tristan Peters', 'Hand': 'L', 'K_pct': 21.6, 'O_Swing': 35.6, 'Z_Contact': 80.0},
        {'Name': 'Drew Romo', 'Hand': 'S', 'K_pct': 25.0, 'O_Swing': 25.0, 'Z_Contact': 91.2},
    ]

    # Padres Lineup vs LHP
    sd_lineup = [
        {'Name': 'Ramon Laureano', 'Hand': 'R', 'K_pct': 22.6, 'O_Swing': 30.1, 'Z_Contact': 77.0},
        {'Name': 'Fernando Tatis Jr.', 'Hand': 'R', 'K_pct': 20.8, 'O_Swing': 32.5, 'Z_Contact': 81.5},
        {'Name': 'Miguel Andujar', 'Hand': 'R', 'K_pct': 18.0, 'O_Swing': 35.0, 'Z_Contact': 84.0},
        {'Name': 'Manny Machado', 'Hand': 'R', 'K_pct': 22.2, 'O_Swing': 32.7, 'Z_Contact': 80.5},
        {'Name': 'Xander Bogaerts', 'Hand': 'R', 'K_pct': 15.2, 'O_Swing': 29.0, 'Z_Contact': 86.5},
        {'Name': 'Ty France', 'Hand': 'R', 'K_pct': 21.0, 'O_Swing': 30.0, 'Z_Contact': 84.0},
        {'Name': 'Nick Castellanos', 'Hand': 'R', 'K_pct': 24.5, 'O_Swing': 40.0, 'Z_Contact': 78.0},
        {'Name': 'Freddy Fermin', 'Hand': 'R', 'K_pct': 18.0, 'O_Swing': 33.0, 'Z_Contact': 83.0},
        {'Name': 'Brooks Johnson', 'Hand': 'S', 'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 80.0},
    ]

    # Pitcher Data
    schultz = {
        'Name': 'Noah Schultz',
        'Hand': 'L',
        'K_pct': 28.6,
        'Stuff': 112,
        'VAA': -4.1,
        'IP': 40.0
    }

    marquez = {
        'Name': 'German Marquez',
        'Hand': 'R',
        'K_pct': 16.2,
        'Stuff': 100,
        'VAA': -4.6,
        'IP': 25.0
    }

    env = {
        'Weather': {'temp': 65, 'dome': False},
        'Umpire': {'CS_pct': 16.5},
        'ParkFactor': 0.95,
    }

    # Execute Padres vs Schultz
    env['Catcher'] = {'Name': 'Drew Romo'}
    res_schultz = master.execute_pipeline(schultz, sd_lineup, env, {'PitchLimit': 85})

    # Execute White Sox vs Marquez
    env['Catcher'] = {'Name': 'Freddy Fermin'}
    res_marquez = master.execute_pipeline(marquez, cws_lineup, env, {'PitchLimit': 90})

    print("\n" + "█" + "▀"*90 + "█")
    print("█ K PROPHET V10.1 — THE SINGULARITY (CWS @ SD)                                          █")
    print("█" + "▄"*90 + "█")
    
    for name, res in [("Noah Schultz", res_schultz), ("German Marquez", res_marquez)]:
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