#!/usr/bin/env python3
import json
import random
from engine import KProphetEngine
from k_pipeline import KProphetMaster

def run_simulation():
    # PITCHER DATA (2026 Telemetry - May 2 Recalibration)
    # Roki Sasaki: Unicorn archetype with elite velocity and flat VAA.
    away_p = {
        "Name": "Roki Sasaki",
        "Hand": "R",
        "IP": 30.0,
        "Stuff": 125,
        "Location": 102,
        "Pitching": 115,
        "K_pct": 32.0,
        "BB_pct": 8.5,
        "xERA": 3.85,
        "VAA": -4.1,
        "ShortLeash": False,
        "TTT_Penalty": 0.90
    }

    # Michael McGreevy: East-West archetype. Elite command, low stuff.
    home_p = {
        "Name": "Michael McGreevy",
        "Hand": "R",
        "IP": 27.1,
        "Stuff": 78,
        "Location": 110,
        "Pitching": 93,
        "K_pct": 16.5,
        "BB_pct": 3.9,
        "xERA": 4.15,
        "VAA": -4.9,
        "ShortLeash": False,
        "TTT_Penalty": 0.85
    }

    # LINEUP DATA (Projected from May 2, 2026 Season-to-Date)
    # Cardinals (vs RHP Sasaki)
    home_lineup = [
        {"Name": "J. Wetherholt", "Hand": "L", "K_pct": 18.0, "O_Swing": 28.0, "Z_Contact": 86.0},
        {"Name": "I. Herrera", "Hand": "R", "K_pct": 17.2, "O_Swing": 27.0, "Z_Contact": 88.0},
        {"Name": "A. Burleson", "Hand": "L", "K_pct": 12.5, "O_Swing": 26.0, "Z_Contact": 90.0},
        {"Name": "J. Walker", "Hand": "R", "K_pct": 32.2, "O_Swing": 41.7, "Z_Contact": 72.0},
        {"Name": "N. Gorman", "Hand": "L", "K_pct": 28.2, "O_Swing": 34.0, "Z_Contact": 75.0},
        {"Name": "M. Winn", "Hand": "R", "K_pct": 21.2, "O_Swing": 28.0, "Z_Contact": 84.0},
        {"Name": "N. Church", "Hand": "L", "K_pct": 25.0, "O_Swing": 30.0, "Z_Contact": 82.0},
        {"Name": "R. Urias", "Hand": "R", "K_pct": 19.5, "O_Swing": 28.0, "Z_Contact": 85.0},
        {"Name": "V. Scott", "Hand": "L", "K_pct": 12.5, "O_Swing": 24.0, "Z_Contact": 92.0}
    ]

    # Dodgers (vs RHP McGreevy)
    away_lineup = [
        {"Name": "S. Ohtani", "Hand": "L", "K_pct": 23.9, "O_Swing": 37.8, "Z_Contact": 78.0},
        {"Name": "F. Freeman", "Hand": "L", "K_pct": 11.8, "O_Swing": 25.0, "Z_Contact": 91.0},
        {"Name": "W. Smith", "Hand": "R", "K_pct": 17.0, "O_Swing": 27.5, "Z_Contact": 88.0},
        {"Name": "K. Tucker", "Hand": "L", "K_pct": 21.6, "O_Swing": 30.5, "Z_Contact": 84.5},
        {"Name": "T. Hernandez", "Hand": "R", "K_pct": 29.5, "O_Swing": 35.0, "Z_Contact": 76.5},
        {"Name": "M. Muncy", "Hand": "L", "K_pct": 25.9, "O_Swing": 24.7, "Z_Contact": 82.5},
        {"Name": "A. Pages", "Hand": "R", "K_pct": 21.7, "O_Swing": 31.0, "Z_Contact": 83.5},
        {"Name": "H. Kim", "Hand": "L", "K_pct": 20.0, "O_Swing": 28.0, "Z_Contact": 85.0},
        {"Name": "A. Freeland", "Hand": "S", "K_pct": 30.9, "O_Swing": 34.0, "Z_Contact": 74.0}
    ]

    # ENVIRONMENT & UMPIRE
    env = {
        "Weather": {"temp": 56, "dome": False, "humidity": 52},
        "Umpire": {"Name": "Nestor Ceja", "CS_pct": 17.0}, # 1.03x Multiplier
        "Catcher": {"Name": "Will Smith", "Framing": 1.05},
        "Ballpark": "Busch Stadium",
        "ParkFactor": 0.98 
    }

    # RUN SIMULATION (100,000 Iterations)
    master = KProphetMaster()
    
    print(f"Activation: K Prophet V13.0 (Deterministic Reality Engine) - May 2, 2026 Forensic Audit")
    print(f"Matchup: {away_p['Name']} (LAD) @ {home_p['Name']} (STL)")
    print("-" * 80)

    # Away Simulation (Sasaki)
    proj_away = master.execute_pipeline(away_p, home_lineup, env, {"PitchLimit": 95})
    # Home Simulation (McGreevy)
    proj_home = master.execute_pipeline(home_p, away_lineup, env, {"PitchLimit": 90})

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
        for line in [3.5, 4.5, 5.5, 6.5]:
            probs = v['probabilities'].get(line, {'Over': 0, 'Under': 0})
            print(f"    Over/Under {line}: Over {probs['Over']*100:.1f}% | Under {probs['Under']*100:.1f}%")
        print("-" * 40)

if __name__ == "__main__":
    run_simulation()
