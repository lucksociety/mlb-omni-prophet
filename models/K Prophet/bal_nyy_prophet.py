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
#!/usr/bin/env python3
import json
from engine import KProphetEngine
from k_pipeline import KProphetMaster

def run_simulation():
    # PITCHER DATA (2026 Telemetry)
    away_p = {
        "Name": "Kyle Bradish",
        "Hand": "R",
        "IP": 30.0,
        "Stuff": 101,
        "Location": 96,
        "Pitching": 98,
        "K_pct": 22.8,
        "BB_pct": 12.5,
        "CSW": 27.1,
        "SwStr": 11.3,
        "xERA": 4.20,
        "VAA": -4.3,
        "ShortLeash": False,
        "TTT_Penalty": 0.85
    }

    home_p = {
        "Name": "Ryan Weathers",
        "Hand": "L",
        "IP": 33.2,
        "Stuff": 101,
        "Location": 115,
        "Pitching": 114,
        "K_pct": 29.2,
        "BB_pct": 5.8,
        "CSW": 32.1,
        "SwStr": 11.6,
        "xERA": 3.21,
        "VAA": -3.9,
        "ShortLeash": False,
        "TTT_Penalty": 0.82
    }

    # LINEUP DATA
    # Orioles (vs LHP Weathers)
    away_lineup = [
        {"Name": "Taylor Ward", "Hand": "R", "K_pct": 7.4, "O_Swing": 26.0, "Z_Contact": 88.0},
        {"Name": "G. Henderson", "Hand": "L", "K_pct": 31.4, "O_Swing": 35.0, "Z_Contact": 78.0},
        {"Name": "A. Rutschman", "Hand": "S", "K_pct": 18.0, "O_Swing": 24.0, "Z_Contact": 86.0},
        {"Name": "Pete Alonso", "Hand": "R", "K_pct": 27.3, "O_Swing": 32.0, "Z_Contact": 82.0},
        {"Name": "T. O'Neill", "Hand": "R", "K_pct": 28.5, "O_Swing": 33.0, "Z_Contact": 79.0},
        {"Name": "J. Jackson", "Hand": "R", "K_pct": 23.1, "O_Swing": 30.0, "Z_Contact": 84.0},
        {"Name": "L. Taveras", "Hand": "S", "K_pct": 22.0, "O_Swing": 28.0, "Z_Contact": 85.0},
        {"Name": "Coby Mayo", "Hand": "R", "K_pct": 24.0, "O_Swing": 31.0, "Z_Contact": 81.0},
        {"Name": "B. Alexander", "Hand": "R", "K_pct": 32.1, "O_Swing": 35.0, "Z_Contact": 77.0}
    ]

    # Yankees (vs RHP Bradish)
    home_lineup = [
        {"Name": "T. Grisham", "Hand": "L", "K_pct": 16.5, "O_Swing": 27.0, "Z_Contact": 85.0},
        {"Name": "Ben Rice", "Hand": "L", "K_pct": 33.3, "O_Swing": 34.0, "Z_Contact": 76.0},
        {"Name": "Aaron Judge", "Hand": "R", "K_pct": 26.8, "O_Swing": 30.0, "Z_Contact": 82.0},
        {"Name": "C. Bellinger", "Hand": "L", "K_pct": 14.5, "O_Swing": 25.0, "Z_Contact": 89.0},
        {"Name": "J. Chisholm", "Hand": "L", "K_pct": 29.1, "O_Swing": 33.0, "Z_Contact": 79.0},
        {"Name": "J. Dominguez", "Hand": "S", "K_pct": 25.0, "O_Swing": 30.0, "Z_Contact": 82.0},
        {"Name": "J.C. Escarra", "Hand": "L", "K_pct": 24.0, "O_Swing": 29.0, "Z_Contact": 84.0},
        {"Name": "Ryan McMahon", "Hand": "L", "K_pct": 25.0, "O_Swing": 30.0, "Z_Contact": 81.0},
        {"Name": "J. Caballero", "Hand": "R", "K_pct": 20.0, "O_Swing": 26.0, "Z_Contact": 87.0}
    ]

    # ENVIRONMENT
    env = {
        "Weather": {"temp": 60, "dome": False},
        "Umpire": {"Name": "Alan Porter", "CS_pct": 17.325}, # Standard
        "Catcher": {"Name": "Austin Wells", "Framing": 1.10}, # Elite framer
        "Ballpark": "Yankee Stadium",
        "ParkFactor": 1.02 # Yankee Stadium is slightly hitter-friendly but neutral for Ks
    }

    # RUN MODEL
    master = KProphetMaster()
    
    print(f"Activation: K Prophet V11.0 (Deterministic Reality Engine) - May 2, 2026")
    print(f"Matchup: {away_p['Name']} (BAL) @ {home_p['Name']} (NYY)")
    print("-" * 80)

    # Away Simulation
    proj_away = master.execute_pipeline(away_p, home_lineup, env, {"PitchLimit": 95})
    # Home Simulation
    proj_home = master.execute_pipeline(home_p, away_lineup, env, {"PitchLimit": 92})

    results = {"Away": proj_away, "Home": proj_home}

    for side, v in results.items():
        p_name = away_p['Name'] if side == 'Away' else home_p['Name']
        print(f"{side} Pitcher: {p_name}")
        print(f"  Exact K Prediction: {v['exact_k']} Ks")
        print(f"  Confidence Level: {v['confidence']*100:.2f}%")
        print(f"  Expected BF: {v['telemetry']['ExpectedBF']:.1f}")
        print(f"  Final pK: {v['telemetry']['Final_pK']:.4f}")
        print(f"  Archetype: {v['telemetry']['Archetype']}")
        print("  Probability Distribution:")
        for line, probs in v['probabilities'].items():
            print(f"    {line}: Over {probs['Over']*100:.1f}% | Under {probs['Under']*100:.1f}%")
        print("-" * 40)

if __name__ == "__main__":
    run_simulation()