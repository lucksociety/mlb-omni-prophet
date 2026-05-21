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
    
    # Royals Lineup vs RHP
    kc_lineup = [
        {'Name': 'Maikel Garcia', 'Hand': 'R', 'K_pct': 17.5, 'O_Swing': 32.5, 'Z_Contact': 85.0},
        {'Name': 'Bobby Witt Jr.', 'Hand': 'R', 'K_pct': 16.2, 'O_Swing': 28.5, 'Z_Contact': 88.0},
        {'Name': 'Vinnie Pasquantino', 'Hand': 'L', 'K_pct': 11.5, 'O_Swing': 24.0, 'Z_Contact': 92.5},
        {'Name': 'Salvador Perez', 'Hand': 'R', 'K_pct': 18.2, 'O_Swing': 40.5, 'Z_Contact': 81.0},
        {'Name': 'Carter Jensen', 'Hand': 'L', 'K_pct': 25.6, 'O_Swing': 42.9, 'Z_Contact': 69.0},
        {'Name': 'Jac Caglianone', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 35.0, 'Z_Contact': 80.0},
        {'Name': 'Isaac Collins', 'Hand': 'S', 'K_pct': 33.3, 'O_Swing': 30.0, 'Z_Contact': 82.8},
        {'Name': 'Michael Massey', 'Hand': 'L', 'K_pct': 18.0, 'O_Swing': 32.0, 'Z_Contact': 84.0},
        {'Name': 'Kyle Isbel', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 31.0, 'Z_Contact': 81.0},
    ]

    # Mariners Lineup vs LHP
    sea_lineup = [
        {'Name': 'J.P. Crawford', 'Hand': 'L', 'K_pct': 18.5, 'O_Swing': 24.5, 'Z_Contact': 88.5},
        {'Name': 'Cal Raleigh', 'Hand': 'S', 'K_pct': 28.5, 'O_Swing': 30.0, 'Z_Contact': 75.0},
        {'Name': 'Julio Rodriguez', 'Hand': 'R', 'K_pct': 25.5, 'O_Swing': 32.7, 'Z_Contact': 80.5},
        {'Name': 'Josh Naylor', 'Hand': 'L', 'K_pct': 14.5, 'O_Swing': 28.5, 'Z_Contact': 89.0},
        {'Name': 'Randy Arozarena', 'Hand': 'R', 'K_pct': 24.5, 'O_Swing': 30.1, 'Z_Contact': 78.0},
        {'Name': 'Mitch Garver', 'Hand': 'R', 'K_pct': 26.5, 'O_Swing': 26.5, 'Z_Contact': 82.0},
        {'Name': 'Cole Young', 'Hand': 'L', 'K_pct': 26.8, 'O_Swing': 29.3, 'Z_Contact': 78.6},
        {'Name': 'Connor Joe', 'Hand': 'R', 'K_pct': 21.0, 'O_Swing': 29.0, 'Z_Contact': 84.5},
        {'Name': 'Leo Rivas', 'Hand': 'S', 'K_pct': 25.0, 'O_Swing': 32.0, 'Z_Contact': 81.0},
    ]

    # Pitcher Data
    ragans = {
        'Name': 'Cole Ragans',
        'Hand': 'L',
        'K_pct': 29.5,
        'Stuff': 118,
        'VAA': -4.5,
        'IP': 45.0
    }

    woo = {
        'Name': 'Bryan Woo',
        'Hand': 'R',
        'K_pct': 19.1,
        'Stuff': 105,
        'VAA': -4.2,
        'IP': 30.0
    }

    env = {
        'Weather': {'temp': 72, 'dome': True},
        'Umpire': {'CS_pct': 16.5},
        'ParkFactor': 0.96,
    }

    # Execute Mariners vs Ragans
    env['Catcher'] = {'Name': 'Salvador Perez'}
    res_ragans = master.execute_pipeline(ragans, sea_lineup, env, {'PitchLimit': 95})

    # Execute Royals vs Woo
    env['Catcher'] = {'Name': 'Cal Raleigh'}
    res_woo = master.execute_pipeline(woo, kc_lineup, env, {'PitchLimit': 90})

    print("\n" + "█" + "▀"*90 + "█")
    print("█ K PROPHET V10.1 — THE SINGULARITY (KC @ SEA)                                          █")
    print("█" + "▄"*90 + "█")
    
    for name, res in [("Cole Ragans", res_ragans), ("Bryan Woo", res_woo)]:
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