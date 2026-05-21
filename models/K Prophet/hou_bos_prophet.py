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

def run_prediction():
    engine = KProphetEngine()
    
    # HOU Lineup vs LHP (Jake Bennett)
    hou_lineup = [
        {'Name': 'Carlos Correa', 'Hand': 'R', 'K_pct': 18.6, 'O_Swing': 28.5, 'Z_Contact': 86.2},
        {'Name': 'Yordan Alvarez', 'Hand': 'L', 'K_pct': 18.0, 'O_Swing': 32.1, 'Z_Contact': 82.5},
        {'Name': 'Isaac Paredes', 'Hand': 'R', 'K_pct': 16.5, 'O_Swing': 22.4, 'Z_Contact': 89.1},
        {'Name': 'Christian Walker', 'Hand': 'R', 'K_pct': 25.1, 'O_Swing': 31.0, 'Z_Contact': 81.4},
        {'Name': 'Jose Altuve', 'Hand': 'R', 'K_pct': 16.8, 'O_Swing': 34.2, 'Z_Contact': 91.5},
        {'Name': 'Yainer Diaz', 'Hand': 'R', 'K_pct': 15.4, 'O_Swing': 40.5, 'Z_Contact': 88.2},
        {'Name': 'Cam Smith', 'Hand': 'R', 'K_pct': 27.0, 'O_Swing': 33.5, 'Z_Contact': 78.5},
        {'Name': 'Brice Matthews', 'Hand': 'R', 'K_pct': 28.5, 'O_Swing': 35.0, 'Z_Contact': 76.0},
        {'Name': 'Dustin Harris', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 29.0, 'Z_Contact': 84.0},
    ]

    # BOS Lineup vs RHP (Mike Burrows)
    bos_lineup = [
        {'Name': 'Jarren Duran', 'Hand': 'L', 'K_pct': 25.6, 'O_Swing': 33.2, 'Z_Contact': 80.5},
        {'Name': 'Willson Contreras', 'Hand': 'R', 'K_pct': 27.5, 'O_Swing': 34.1, 'Z_Contact': 78.2},
        {'Name': 'Roman Anthony', 'Hand': 'L', 'K_pct': 27.6, 'O_Swing': 28.5, 'Z_Contact': 79.5},
        {'Name': 'Wilyer Abreu', 'Hand': 'L', 'K_pct': 26.5, 'O_Swing': 32.0, 'Z_Contact': 81.0},
        {'Name': 'Trevor Story', 'Hand': 'R', 'K_pct': 26.4, 'O_Swing': 36.8, 'Z_Contact': 75.4},
        {'Name': 'Marcelo Mayer', 'Hand': 'L', 'K_pct': 24.5, 'O_Swing': 30.5, 'Z_Contact': 82.0},
        {'Name': 'Ceddanne Rafaela', 'Hand': 'R', 'K_pct': 20.1, 'O_Swing': 44.5, 'Z_Contact': 85.2},
        {'Name': 'Carlos Narvaez', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 84.5},
        {'Name': 'Caleb Durbin', 'Hand': 'R', 'K_pct': 11.0, 'O_Swing': 21.5, 'Z_Contact': 94.2},
    ]

    # Pitcher Data
    burrows = {
        'Name': 'Mike Burrows',
        'Hand': 'R',
        'K_pct': 26.0,
        'Stuff': 108,
        'VAA': -4.3,
        'Pit+ FA': 108,
        'Pit+ SI': 105,
        'Pit+ SL': 102,
        'IP': 31.7
    }

    bennett = {
        'Name': 'Jake Bennett',
        'Hand': 'L',
        'K_pct': 19.0, # AAA baseline
        'Stuff': 98,
        'VAA': -4.7,
        'Pit+ FA': 100,
        'Pit+ SI': 102,
        'Pit+ SL': 105,
        'IP': 21.0 # AAA
    }

    env = {
        'Weather': {'temp': 60},
        'Umpire': {'CS_pct': 16.5},
        'ParkFactor': 1.02,
        'Catcher': {'Name': 'Yainer Diaz'} # BOS will use Narvaez
    }

    # Execute HOU vs Bennett
    env['Catcher'] = {'Name': 'Yainer Diaz'}
    res_bennett = engine.project(bennett, hou_lineup, env, {'PitchLimit': 80}) # 80 pitch limit for debut

    # Execute BOS vs Burrows
    env['Catcher'] = {'Name': 'Carlos Narvaez'}
    res_burrows = engine.project(burrows, bos_lineup, env, {'PitchLimit': 95})

    print("\n" + "="*50)
    print("K PROPHET V10.1 — PROJECTION OUTPUT")
    print("="*50)
    
    print(f"\nSTARTING PITCHER: {burrows['Name']} (HOU)")
    print(f"Opponent: Boston Red Sox")
    print(f"Mean K: {res_burrows['mean_k']:.2f}")
    print(f"Exact K: {res_burrows['exact_k']}")
    print(f"Confidence: {res_burrows['confidence']*100:.1f}%")
    for line, prob in res_burrows['probabilities'].items():
        print(f"  Line {line}: Over {prob['Over']*100:.1f}% | Under {prob['Under']*100:.1f}%")

    print(f"\nSTARTING PITCHER: {bennett['Name']} (BOS)")
    print(f"Opponent: Houston Astros")
    print(f"Mean K: {res_bennett['mean_k']:.2f}")
    print(f"Exact K: {res_bennett['exact_k']}")
    print(f"Confidence: {res_bennett['confidence']*100:.1f}%")
    for line, prob in res_bennett['probabilities'].items():
        print(f"  Line {line}: Over {prob['Over']*100:.1f}% | Under {prob['Under']*100:.1f}%")
    print("="*50)

if __name__ == "__main__":
    run_prediction()