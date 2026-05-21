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
    
    # Guardians Lineup vs LHP (Lopez)
    cle_lineup = [
        {'Name': 'Steven Kwan', 'Hand': 'L', 'K_pct': 9.5, 'O_Swing': 39.1, 'Z_Contact': 92.5},
        {'Name': 'A. Martinez', 'Hand': 'S', 'K_pct': 18.0, 'O_Swing': 30.0, 'Z_Contact': 85.0},
        {'Name': 'Jose Ramirez', 'Hand': 'S', 'K_pct': 11.5, 'O_Swing': 26.5, 'Z_Contact': 88.5},
        {'Name': 'Rhys Hoskins', 'Hand': 'R', 'K_pct': 25.0, 'O_Swing': 42.1, 'Z_Contact': 80.0},
        {'Name': 'David Fry', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 32.0, 'Z_Contact': 82.0},
        {'Name': 'Travis Bazzana', 'Hand': 'L', 'K_pct': 17.4, 'O_Swing': 22.0, 'Z_Contact': 90.0},
        {'Name': 'Daniel Schneemann', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 47.9, 'Z_Contact': 82.0},
        {'Name': 'Austin Hedges', 'Hand': 'R', 'K_pct': 26.0, 'O_Swing': 30.0, 'Z_Contact': 81.0},
        {'Name': 'Bo Rocchio', 'Hand': 'S', 'K_pct': 17.9, 'O_Swing': 31.0, 'Z_Contact': 84.0},
    ]

    # Athletics Lineup vs RHP (Cecconi)
    ath_lineup = [
        {'Name': 'Nick Kurtz', 'Hand': 'L', 'K_pct': 30.8, 'O_Swing': 41.9, 'Z_Contact': 76.0},
        {'Name': 'Shea Langeliers', 'Hand': 'R', 'K_pct': 22.5, 'O_Swing': 35.0, 'Z_Contact': 76.0},
        {'Name': 'Tyler Soderstrom', 'Hand': 'L', 'K_pct': 21.6, 'O_Swing': 33.8, 'Z_Contact': 79.5},
        {'Name': 'Brent Rooker', 'Hand': 'R', 'K_pct': 25.5, 'O_Swing': 32.5, 'Z_Contact': 78.5},
        {'Name': 'Carlos Cortes', 'Hand': 'L', 'K_pct': 56.5, 'O_Swing': 31.5, 'Z_Contact': 75.0},
        {'Name': 'Jacob Wilson', 'Hand': 'R', 'K_pct': 11.1, 'O_Swing': 44.2, 'Z_Contact': 89.6},
        {'Name': 'Jeff McNeil', 'Hand': 'L', 'K_pct': 13.2, 'O_Swing': 26.5, 'Z_Contact': 88.0},
        {'Name': 'Lawrence Butler', 'Hand': 'L', 'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 81.0},
        {'Name': 'Darell Hernaiz', 'Hand': 'R', 'K_pct': 20.0, 'O_Swing': 33.0, 'Z_Contact': 82.0},
    ]

    # Pitcher Data
    cecconi = {
        'Name': 'Slade Cecconi',
        'Hand': 'R',
        'K_pct': 21.5,
        'Stuff': 104,
        'VAA': -4.4,
        'IP': 30.0,
        'BB_pct': 8.5,
        'xERA': 4.85
    }

    lopez = {
        'Name': 'Jacob Lopez',
        'Hand': 'L',
        'K_pct': 24.2,
        'Stuff': 98,
        'VAA': -4.1,
        'IP': 24.2,
        'BB_pct': 12.5,
        'xERA': 5.10
    }

    env = {
        'Weather': {'temp': 78, 'dome': False},
        'Umpire': {'CS_pct': 15.8}, # Shane Livensparger "Tight" Zone
        'ParkFactor': 0.95,
    }

    # Execute Athletics vs Cecconi
    env['Catcher'] = {'Name': 'Bo Naylor'}
    res_cecconi = master.execute_pipeline(cecconi, ath_lineup, env, {'PitchLimit': 85})

    # Execute Guardians vs Lopez
    env['Catcher'] = {'Name': 'Shea Langeliers'}
    res_lopez = master.execute_pipeline(lopez, cle_lineup, env, {'PitchLimit': 95})

    print("\n" + "█" + "▀"*90 + "█")
    print("█ K PROPHET V11.0 — THE SINGULARITY (CLE @ ATH)                                         █")
    print("█" + "▄"*90 + "█")
    
    for name, res in [("Slade Cecconi", res_cecconi), ("Jacob Lopez", res_lopez)]:
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
