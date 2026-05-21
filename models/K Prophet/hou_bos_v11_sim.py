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

from engine import KProphetEngine

def run_simulation():
    engine = KProphetEngine()
    
    # HOU Lineup (vs LHP Connelly Early) - 2026 Statcast Recalibration
    hou_lineup = [
        {'Name': 'Carlos Correa', 'Hand': 'R', 'K_pct': 16.5, 'O_Swing': 31.2, 'Z_Contact': 83.7},
        {'Name': 'Yordan Alvarez', 'Hand': 'L', 'K_pct': 10.1, 'O_Swing': 27.3, 'Z_Contact': 92.1},
        {'Name': 'Isaac Paredes', 'Hand': 'R', 'K_pct': 15.5, 'O_Swing': 29.3, 'Z_Contact': 89.2},
        {'Name': 'Christian Walker', 'Hand': 'R', 'K_pct': 17.8, 'O_Swing': 28.6, 'Z_Contact': 84.5},
        {'Name': 'Jose Altuve', 'Hand': 'R', 'K_pct': 18.0, 'O_Swing': 30.3, 'Z_Contact': 86.0},
        {'Name': 'Yainer Diaz', 'Hand': 'R', 'K_pct': 14.9, 'O_Swing': 41.6, 'Z_Contact': 90.4},
        {'Name': 'Brice Matthews', 'Hand': 'R', 'K_pct': 39.7, 'O_Swing': 25.0, 'Z_Contact': 73.3},
        {'Name': 'Cam Smith', 'Hand': 'R', 'K_pct': 28.1, 'O_Swing': 32.0, 'Z_Contact': 81.4},
        {'Name': 'Dustin Harris', 'Hand': 'L', 'K_pct': 13.0, 'O_Swing': 31.5, 'Z_Contact': 88.4},
    ]

    # BOS Lineup (vs RHP Spencer Arrighetti) - 2026 Statcast Recalibration
    bos_lineup = [
        {'Name': 'Jarren Duran', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 34.3, 'Z_Contact': 80.3},
        {'Name': 'Willson Contreras', 'Hand': 'R', 'K_pct': 28.8, 'O_Swing': 30.4, 'Z_Contact': 76.9},
        {'Name': 'Roman Anthony', 'Hand': 'L', 'K_pct': 26.9, 'O_Swing': 22.7, 'Z_Contact': 83.5},
        {'Name': 'Wilyer Abreu', 'Hand': 'L', 'K_pct': 16.9, 'O_Swing': 26.7, 'Z_Contact': 85.0},
        {'Name': 'Trevor Story', 'Hand': 'R', 'K_pct': 29.6, 'O_Swing': 44.8, 'Z_Contact': 80.4},
        {'Name': 'Marcelo Mayer', 'Hand': 'L', 'K_pct': 15.7, 'O_Swing': 23.6, 'Z_Contact': 87.9},
        {'Name': 'Ceddanne Rafaela', 'Hand': 'R', 'K_pct': 22.2, 'O_Swing': 36.3, 'Z_Contact': 79.5},
        {'Name': 'Connor Wong', 'Hand': 'R', 'K_pct': 14.0, 'O_Swing': 34.9, 'Z_Contact': 91.5},
        {'Name': 'Caleb Durbin', 'Hand': 'R', 'K_pct': 14.0, 'O_Swing': 24.5, 'Z_Contact': 88.1},
    ]

    # Pitcher Data
    arrighetti = {
        'Name': 'Spencer Arrighetti',
        'Hand': 'R',
        'K_pct': 18.0, 
        'BB_pct': 11.5,
        'xERA': 5.03,
        'Stuff': 114,
        'VAA': -1.41,
        'Pit+ FA': 118,
        'Pit+ SL': 112,
        'IP': 18.0
    }

    early = {
        'Name': 'Connelly Early',
        'Hand': 'L',
        'K_pct': 22.2,
        'BB_pct': 10.7,
        'xERA': 5.05,
        'Stuff': 104,
        'VAA': -1.65,
        'Pit+ SI': 110,
        'Pit+ SL': 115,
        'IP': 31.7
    }

    env = {
        'Weather': {'temp': 56}, # Marine Layer
        'Umpire': {'CS_pct': 16.2}, # Erich Bacchus (Tight)
        'ParkFactor': 1.02, # Fenway K-Mod
    }

    # Simulation Overrides
    # HOU: Quick hook, extreme fatigue
    hou_overrides = {
        'PitchLimit': 85,
        'ShortLeash': True,
        'Hot_Streak': 1.05 # Arrighetti stuff breakout
    }
    
    # BOS: Aggressive yank before 3rd time through
    bos_overrides = {
        'PitchLimit': 88,
        'ShortLeash': False,
        'Hot_Streak': 1.0
    }

    # Execute Simulations
    res_arrighetti = engine.project(arrighetti, bos_lineup, env, hou_overrides)
    res_early = engine.project(early, hou_lineup, env, bos_overrides)

    print("\n" + "="*60)
    print("K PROPHET V11.0 — DETERMINISTIC REALITY ENGINE (DRE)")
    print("May 2026 Recalibration Protocol — Fenway Park (4:10 PM)")
    print("="*60)
    
    print(f"\nSTARTING PITCHER: {arrighetti['Name']} (HOU)")
    print(f"Opponent: Boston Red Sox")
    print(f"Mean K: {res_arrighetti['mean_k']:.2f}")
    print(f"DRE Exact Strikeout Prediction: {res_arrighetti['exact_k']}")
    print(f"Confidence Level: {res_arrighetti['confidence']*100:.1f}%")
    print(f"Telemetry: BF: {res_arrighetti['telemetry']['ExpectedBF']:.1f} | Final pK: {res_arrighetti['telemetry']['Final_pK']:.4f} | Archetype: {res_arrighetti['telemetry']['Archetype']}")
    print("Probability Distribution:")
    for line, prob in res_arrighetti['probabilities'].items():
        print(f"  Line {line}: Over {prob['Over']*100:.1f}% | Under {prob['Under']*100:.1f}%")

    print(f"\nSTARTING PITCHER: {early['Name']} (BOS)")
    print(f"Opponent: Houston Astros")
    print(f"Mean K: {res_early['mean_k']:.2f}")
    print(f"DRE Exact Strikeout Prediction: {res_early['exact_k']}")
    print(f"Confidence Level: {res_early['confidence']*100:.1f}%")
    print(f"Telemetry: BF: {res_early['telemetry']['ExpectedBF']:.1f} | Final pK: {res_early['telemetry']['Final_pK']:.4f} | Archetype: {res_early['telemetry']['Archetype']}")
    print("Probability Distribution:")
    for line, prob in res_early['probabilities'].items():
        print(f"  Line {line}: Over {prob['Over']*100:.1f}% | Under {prob['Under']*100:.1f}%")
    print("\n" + "="*60)

if __name__ == "__main__":
    run_simulation()