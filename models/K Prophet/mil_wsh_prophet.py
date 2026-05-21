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
import random
from engine import KProphetEngine
from k_pipeline import KProphetMaster

def run_simulation():
    # PITCHER DATA (2026 Telemetry - May 2 Recalibration)
    # Kyle Harrison: North-South "Unicorn" LHP. High carry 4-seam.
    # VAA of -4.1 triggers North-South in V11.0 logic (> -4.1 needed, so we use -4.0)
    away_p = {
        "Name": "Kyle Harrison",
        "Hand": "L",
        "Stuff": 102,
        "Pit+ FA": 118, # Triggers North-South
        "K_pct": 31.3,
        "BB_pct": 8.5,
        "xERA": 3.06,
        "VAA": -4.0, # Triggers North-South
        "ShortLeash": False,
        "TTT_Penalty": 0.85,
        "IP": 120.0 # Experienced enough for stabilization
    }

    # Foster Griffin: East-West LHP. Horizontal break specialist.
    home_p = {
        "Name": "Foster Griffin",
        "Hand": "L",
        "Stuff": 92,
        "Pit+ SI": 112, # Triggers East-West
        "K_pct": 20.8,
        "BB_pct": 7.3,
        "xERA": 3.38,
        "VAA": -4.5,
        "ShortLeash": False,
        "TTT_Penalty": 0.78,
        "IP": 110.0
    }

    # LINEUP DATA (Projected for May 2, 2026)
    # Brewers (vs LHP Griffin)
    away_lineup = [
        {"Name": "B. Lockridge", "Hand": "R", "K_pct": 34.6, "O_Swing": 35.5, "Z_Contact": 78.5},
        {"Name": "Brice Turang", "Hand": "L", "K_pct": 23.8, "O_Swing": 32.1, "Z_Contact": 82.4},
        {"Name": "W. Contreras", "Hand": "R", "K_pct": 16.2, "O_Swing": 28.5, "Z_Contact": 88.5},
        {"Name": "Jake Bauers", "Hand": "L", "K_pct": 20.8, "O_Swing": 30.2, "Z_Contact": 81.5},
        {"Name": "Gary Sanchez", "Hand": "R", "K_pct": 28.5, "O_Swing": 34.5, "Z_Contact": 75.5},
        {"Name": "Luis Rengifo", "Hand": "S", "K_pct": 20.3, "O_Swing": 29.5, "Z_Contact": 83.5},
        {"Name": "Greg Jones", "Hand": "S", "K_pct": 40.9, "O_Swing": 38.5, "Z_Contact": 68.5},
        {"Name": "B. Perkins", "Hand": "S", "K_pct": 24.5, "O_Swing": 31.5, "Z_Contact": 79.5},
        {"Name": "Joey Ortiz", "Hand": "R", "K_pct": 19.2, "O_Swing": 27.5, "Z_Contact": 85.5}
    ]

    # Nationals (vs LHP Harrison)
    home_lineup = [
        {"Name": "James Wood", "Hand": "L", "K_pct": 36.7, "O_Swing": 31.5, "Z_Contact": 72.5},
        {"Name": "Curtis Mead", "Hand": "R", "K_pct": 18.2, "O_Swing": 26.5, "Z_Contact": 85.5},
        {"Name": "Brady House", "Hand": "R", "K_pct": 33.8, "O_Swing": 32.5, "Z_Contact": 74.5},
        {"Name": "CJ Abrams", "Hand": "L", "K_pct": 20.0, "O_Swing": 28.5, "Z_Contact": 81.5},
        {"Name": "Jacob Young", "Hand": "R", "K_pct": 15.2, "O_Swing": 24.5, "Z_Contact": 89.5},
        {"Name": "Daylen Lile", "Hand": "L", "K_pct": 15.8, "O_Swing": 23.5, "Z_Contact": 87.5},
        {"Name": "Joey Wiemer", "Hand": "R", "K_pct": 36.7, "O_Swing": 35.5, "Z_Contact": 70.5},
        {"Name": "Nasim Nunez", "Hand": "S", "K_pct": 16.9, "O_Swing": 25.5, "Z_Contact": 84.5},
        {"Name": "Drew Millas", "Hand": "S", "K_pct": 21.5, "O_Swing": 28.5, "Z_Contact": 82.5}
    ]

    # ENVIRONMENT & UMPIRE
    env = {
        "Weather": {"temp": 61, "dome": False, "humidity": 36},
        "Umpire": {"Name": "Junior Valentine", "CS_pct": 15.8}, # Tight zone factor
        "Catcher": {"Name": "William Contreras / Drew Millas", "Framing": 1.02},
        "Ballpark": "Nationals Park",
        "ParkFactor": 1.00 
    }

    # RUN SIMULATION
    master = KProphetMaster()
    
    print(f"Activation: K Prophet V11.0 (Deterministic Reality Engine) - May 2, 2026 Recalibration")
    print(f"Matchup: {away_p['Name']} (MIL) @ {home_p['Name']} (WSH)")
    print("-" * 80)

    # Away Simulation (Harrison)
    proj_away = master.execute_pipeline(away_p, home_lineup, env, {"PitchLimit": 95})
    # Home Simulation (Griffin)
    proj_home = master.execute_pipeline(home_p, away_lineup, env, {"PitchLimit": 92})

    results = {"Away": proj_away, "Home": proj_home}

    for side, v in results.items():
        p_name = away_p['Name'] if side == 'Away' else home_p['Name']
        print(f"{side} Pitcher: {p_name}")
        print(f"  Deterministic Exact K Prediction: {v['exact_k']} Ks")
        print(f"  Confidence Level: {v['confidence']*100:.2f}%")
        print(f"  Expected Batters Faced (BF): {v['telemetry']['ExpectedBF']:.1f}")
        print(f"  Final pK (Probability of K): {v['telemetry']['Final_pK']:.4f}")
        print(f"  Archetype: {v['telemetry']['Archetype']}")
        print("  Probability Distribution:")
        for line in [4.5, 5.5, 6.5, 7.5]:
            probs = v['probabilities'].get(line, {'Over': 0, 'Under': 0})
            print(f"    Over/Under {line}: Over {probs['Over']*100:.1f}% | Under {probs['Under']*100:.1f}%")
        print("-" * 40)

if __name__ == "__main__":
    run_simulation()