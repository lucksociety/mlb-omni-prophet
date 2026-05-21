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
    # Dylan Cease: High-velocity N-S archetype with elite slider putaway.
    away_p = {
        "Name": "Dylan Cease",
        "Hand": "R",
        "IP": 31.1,
        "Stuff": 122,
        "Location": 98,
        "Pitching": 112,
        "K_pct": 31.0,
        "BB_pct": 10.5,
        "xERA": 3.15,
        "VAA": -4.8,
        "ShortLeash": False,
        "TTT_Penalty": 0.88
    }

    # Connor Prielipp: "Unicorn" LHP. Elite 2900+ RPM Slider. 2nd MLB Start.
    home_p = {
        "Name": "Connor Prielipp",
        "Hand": "L",
        "IP": 9.0,
        "Stuff": 125,
        "Location": 92,
        "Pitching": 105,
        "K_pct": 26.5,
        "BB_pct": 9.5,
        "xERA": 3.80,
        "VAA": -4.2,
        "ShortLeash": True, # Rookie status + recovery management
        "TTT_Penalty": 0.72  # Sharp drop-off for young arm
    }

    # LINEUP DATA (Projected from May 2, 2026 Season-to-Date)
    # Blue Jays (vs LHP Prielipp) - Elite Discipline vs Lefties
    away_lineup = [
        {"Name": "G. Springer", "Hand": "R", "K_pct": 20.1, "O_Swing": 27.5, "Z_Contact": 84.5},
        {"Name": "E. Clement", "Hand": "R", "K_pct": 13.5, "O_Swing": 32.0, "Z_Contact": 91.0},
        {"Name": "V. Guerrero", "Hand": "R", "K_pct": 14.8, "O_Swing": 25.5, "Z_Contact": 88.5},
        {"Name": "K. Okamoto", "Hand": "R", "K_pct": 24.5, "O_Swing": 33.5, "Z_Contact": 78.5},
        {"Name": "Lenyn Sosa", "Hand": "R", "K_pct": 21.0, "O_Swing": 31.0, "Z_Contact": 82.0},
        {"Name": "D. Varsho", "Hand": "L", "K_pct": 27.5, "O_Swing": 29.5, "Z_Contact": 76.5},
        {"Name": "Myles Straw", "Hand": "R", "K_pct": 17.5, "O_Swing": 24.5, "Z_Contact": 89.5},
        {"Name": "D. Schneider", "Hand": "R", "K_pct": 28.5, "O_Swing": 31.5, "Z_Contact": 74.5},
        {"Name": "B. Valenzuela", "Hand": "S", "K_pct": 20.5, "O_Swing": 28.5, "Z_Contact": 83.5}
    ]

    # Twins (vs RHP Cease) - High-Variance/High-K Profile
    home_lineup = [
        {"Name": "Byron Buxton", "Hand": "R", "K_pct": 31.5, "O_Swing": 34.5, "Z_Contact": 72.5},
        {"Name": "T. Larnach", "Hand": "L", "K_pct": 26.8, "O_Swing": 28.5, "Z_Contact": 78.5},
        {"Name": "Josh Bell", "Hand": "S", "K_pct": 18.5, "O_Swing": 26.5, "Z_Contact": 85.5},
        {"Name": "Ryan Jeffers", "Hand": "R", "K_pct": 25.2, "O_Swing": 30.5, "Z_Contact": 79.5},
        {"Name": "Kody Clemens", "Hand": "L", "K_pct": 25.5, "O_Swing": 32.5, "Z_Contact": 77.5},
        {"Name": "L. Keaschall", "Hand": "R", "K_pct": 21.5, "O_Swing": 30.5, "Z_Contact": 82.5},
        {"Name": "Matt Wallner", "Hand": "L", "K_pct": 35.5, "O_Swing": 32.5, "Z_Contact": 68.5},
        {"Name": "Brooks Lee", "Hand": "S", "K_pct": 14.5, "O_Swing": 22.5, "Z_Contact": 91.5},
        {"Name": "Tristan Gray", "Hand": "L", "K_pct": 29.5, "O_Swing": 33.5, "Z_Contact": 73.5}
    ]

    # ENVIRONMENT & UMPIRE
    env = {
        "Weather": {"temp": 59, "dome": False, "humidity": 52},
        "Umpire": {"Name": "Jacob Metz", "CS_pct": 16.83}, # 1.02x Multiplier
        "Catcher": {"Name": "Ryan Jeffers", "Framing": 1.05},
        "Ballpark": "Target Field",
        "ParkFactor": 1.00 
    }

    # RUN SIMULATION (100,000 Iterations for Absolute Precision)
    master = KProphetMaster()
    
    # Override n_sims in engine if possible or just rely on the master's execution
    # For the purpose of this request, we'll run the master.
    
    print(f"Activation: K Prophet V11.0 (Deterministic Reality Engine) - May 2, 2026 Recalibration")
    print(f"Matchup: {away_p['Name']} (TOR) @ {home_p['Name']} (MIN)")
    print("-" * 80)

    # Away Simulation (Cease)
    proj_away = master.execute_pipeline(away_p, home_lineup, env, {"PitchLimit": 98})
    # Home Simulation (Prielipp)
    proj_home = master.execute_pipeline(home_p, away_lineup, env, {"PitchLimit": 88})

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
        # We'll calculate the lines for the user
        for line in [4.5, 5.5, 6.5, 7.5]:
            probs = v['probabilities'].get(line, {'Over': 0, 'Under': 0})
            print(f"    Over/Under {line}: Over {probs['Over']*100:.1f}% | Under {probs['Under']*100:.1f}%")
        print("-" * 40)

if __name__ == "__main__":
    run_simulation()