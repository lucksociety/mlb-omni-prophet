import json
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

from engine import GenerativeWorldModel

def extract_overrides(pitcher):
    return {
        "Velo_Delta": float(pitcher.get("Velo_Delta", 0)),
        "Release_SD_X": float(pitcher.get("Release_SD_X", 1.0)),
        "Release_SD_Z": float(pitcher.get("Release_SD_Z", 1.0)),
        "ShortLeash": pitcher.get("ShortLeash", False),
        "Sleep_Cycle_Disruption": float(pitcher.get("Sleep_Cycle_Disruption", 0.0))
    }

def extract_pitcher_bundle(pitcher):
    adv = {
        "K_pct": float(pitcher.get("K_pct", 22.7)) if pitcher.get("K_pct", "MISSING") != "MISSING" else 22.7
    }
    plus = {
        "Stuff": float(pitcher.get("Stuff", 100)) if pitcher.get("Stuff", "MISSING") != "MISSING" else 100
    }
    return {"adv": adv, "plus": plus, "sc": {}, "disc": {}}

def extract_env(data):
    env_data = data.get("Environment", {})
    game_info = data.get("GameInfo", {})
    
    # Map stadium orientations (Pseudo-Coriolis mapping)
    stadium = game_info.get("Ballpark", "")
    orientation_map = {
        "LoanDepot Park": 85,
        "Yankee Stadium": 65,
        "Fenway Park": 45,
    }
    orientation = orientation_map.get(stadium, 45) # Default 45 degrees
    
    return {
        "Weather": {"temp": 72, "dome": env_data.get("Roof", "Open") == "Closed"},
        "ParkFactor": 1.0,
        "Orientation": orientation,
        "CloudDensity": 0.3 if env_data.get("Roof", "Open") == "Closed" else 0.7, # Roof dictates VCI
        "Clay_Moisture": 0.6 if env_data.get("Roof", "Open") == "Closed" else 0.4
    }

from k_pipeline import KProphetMaster

def run_singularity(data):
    master = KProphetMaster()
    results = {}
    
    # Environment mapping
    env_data = data.get("Environment", {})
    game_info = data.get("GameInfo", {})
    weather = {"temp": 72, "dome": env_data.get("Roof", "Open") == "Closed"}
    env = {'Weather': weather, 'Umpire': {'CS_pct': 16.5}, 'Catcher': {'Framing': 50.0}}
    
    for side in ["Away", "Home"]:
        pitcher = data[side]
        pitcher_name = pitcher.get("Name", "Unknown")
        
        # Build Pitcher Data
        pitcher_data = {
            'PitchCounts': pitcher.get('PitchCounts', [90]),
            'ShortLeash': pitcher.get('ShortLeash', False),
            'InjuryFlag': 0.0,
            'BB_pct': float(pitcher.get('BB_pct', 8.5) or 8.5),
            'Zone_pct': float(pitcher.get('Zone_pct', 50.0) or 50.0),
            'SwStr': float(pitcher.get('SwStr', 11.0) or 11.0),
            'CSW': float(pitcher.get('CSW', 27.0) or 27.0),
            'K_pct': float(pitcher.get('K_pct', 22.0) or 22.0),
            'PitchMix': {}, # Statcast data integration pending
            'TTT_Penalty': 0.85
        }
        
        manager_data = {'Conservatism': 0.1}
        
        # Dummy lineup for single game test
        lineup_data = [{'O_Swing': 30.0, 'K_Weakness': {}} for _ in range(9)]
        
        proj = master.execute_pipeline(pitcher_data, lineup_data, env, manager_data)
        results[pitcher_name] = proj
        
    print("┌" + "─"*96 + "┐")
    print("│ THE OMEGA DIRECTIVE: DETERMINISTIC REALITY ENGINE (DRE) V8.1                                   │")
    print("├" + "─"*22 + "┬" + "─"*18 + "┬" + "─"*54 + "┤")
    print("│ Pitcher              │ Deterministic K  │ God Protocol Telemetry                               │")
    print("├" + "─"*22 + "┼" + "─"*18 + "┼" + "─"*54 + "┤")
    for p, v in results.items():
        if v['status'] == 'REJECTED':
            telemetry = f"REJECTED: {v['reason']}"
            k_val = "N/A"
            conf = 0.0
        else:
            conf = v["confidence"] * 100
            bf = v['telemetry']['ExpectedBF']
            ppa = v['telemetry']['PitchesPerPA']
            k_val = f"{v['exact_k']} Ks"
            telemetry = f"BF: {bf:.1f} | P/PA: {ppa:.2f} | Predictability: {v['predictability_score']:.1f}"
        
        print(f"│ {p:<20} │ {k_val:<16} │ {telemetry:<52} │")
        print(f"│ {'':<20} │ ({conf:>6.2f}%)       │ {'':<52} │")
    print("└" + "─"*22 + "┴" + "─"*18 + "┴" + "─"*54 + "┘")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python k_model.py <data.json>")
        sys.exit(1)
        
    with open(sys.argv[1]) as f:
        data = json.load(f)
        
    run_singularity(data)