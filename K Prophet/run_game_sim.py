
import sys
import os

# Add the current directory to sys.path so we can import local modules
sys.path.append('/Users/danielreiss/Desktop/Antigravity/K Prophet')

from k_pipeline import KProphetMaster

def run_simulation():
    master = KProphetMaster()

    # Robbie Ray (SFG) vs Rays Lineup
    ray_data = {
        'Name': 'Robbie Ray',
        'Hand': 'L',
        'K_pct': 25.9,
        'BB_pct': 10.4,
        'Stuff': 102,
        'VAA': -4.5,
        'IP': 33.1,
        'Pit+ FA': 105,
        'Pit+ SL': 95,
        'Pit+ CH': 92,
        'ShortLeash': False,
        'TTT_Penalty': 0.85
    }

    # Rays Lineup vs LHP
    rays_lineup = [
        {'Name': 'Chandler Simpson', 'Hand': 'L', 'K_pct': 8.1, 'O_Swing': 25.0, 'Z_Contact': 92.0},
        {'Name': 'Junior Caminero', 'Hand': 'R', 'K_pct': 6.1, 'O_Swing': 28.0, 'Z_Contact': 88.0},
        {'Name': 'Ryan Vilade', 'Hand': 'R', 'K_pct': 20.0, 'O_Swing': 32.0, 'Z_Contact': 85.0},
        {'Name': 'Yandy Diaz', 'Hand': 'R', 'K_pct': 21.4, 'O_Swing': 22.0, 'Z_Contact': 90.0},
        {'Name': 'Ben Williamson', 'Hand': 'R', 'K_pct': 23.5, 'O_Swing': 30.0, 'Z_Contact': 85.0},
        {'Name': 'Jonny DeLuca', 'Hand': 'R', 'K_pct': 22.2, 'O_Swing': 33.0, 'Z_Contact': 84.0},
        {'Name': 'Jake Fraley', 'Hand': 'L', 'K_pct': 22.7, 'O_Swing': 28.0, 'Z_Contact': 85.0},
        {'Name': 'Nick Fortes', 'Hand': 'R', 'K_pct': 13.9, 'O_Swing': 35.0, 'Z_Contact': 87.0},
        {'Name': 'Taylor Walls', 'Hand': 'S', 'K_pct': 25.0, 'O_Swing': 24.0, 'Z_Contact': 82.0}
    ]

    # Shane McClanahan (TBR) vs Giants Lineup
    mcclanahan_data = {
        'Name': 'Shane McClanahan',
        'Hand': 'L',
        'K_pct': 29.5,
        'BB_pct': 12.9,
        'Stuff': 118,
        'VAA': -4.1,
        'IP': 15.0,
        'Pit+ FA': 118,
        'Pit+ SL': 112,
        'Pit+ CH': 115,
        'ShortLeash': True, # Returning from injury
        'TTT_Penalty': 0.82
    }

    # Giants Lineup vs LHP
    giants_lineup = [
        {'Name': 'Heliot Ramos', 'Hand': 'R', 'K_pct': 38.5, 'O_Swing': 35.0, 'Z_Contact': 78.0},
        {'Name': 'Matt Chapman', 'Hand': 'R', 'K_pct': 20.0, 'O_Swing': 30.0, 'Z_Contact': 82.0},
        {'Name': 'Luis Arraez', 'Hand': 'L', 'K_pct': 5.7, 'O_Swing': 18.0, 'Z_Contact': 95.0},
        {'Name': 'Casey Schmitt', 'Hand': 'R', 'K_pct': 20.0, 'O_Swing': 32.0, 'Z_Contact': 84.0},
        {'Name': 'Rafael Devers', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 34.0, 'Z_Contact': 82.0},
        {'Name': 'Willy Adames', 'Hand': 'R', 'K_pct': 27.3, 'O_Swing': 31.0, 'Z_Contact': 80.0},
        {'Name': 'Jung Hoo Lee', 'Hand': 'L', 'K_pct': 14.8, 'O_Swing': 22.0, 'Z_Contact': 91.0},
        {'Name': 'Jerar Encarnacion', 'Hand': 'R', 'K_pct': 22.7, 'O_Swing': 30.0, 'Z_Contact': 85.0},
        {'Name': 'Patrick Bailey', 'Hand': 'S', 'K_pct': 31.0, 'O_Swing': 32.0, 'Z_Contact': 75.0}
    ]

    env_data = {
        'Weather': {'temp': 72, 'dome': True},
        'Umpire': {'CS_pct': 16.5},
        'Catcher': {'Name': 'Patrick Bailey'}, # For McClanahan's side
        'ParkFactor': 0.95 # Tropicana is pitcher friendly
    }

    manager_data_ray = {'PitchLimit': 92}
    manager_data_shane = {'PitchLimit': 85}

    print("\n--- RUNNING K PROPHET V10.0 PREDICTION PROTOCOL ---\n")
    
    ray_proj = master.execute_pipeline(ray_data, rays_lineup, env_data, manager_data_ray)
    
    # Update catcher for Ray's side (TBR catcher)
    env_data['Catcher'] = {'Name': 'Nick Fortes'}
    shane_proj = master.execute_pipeline(mcclanahan_data, giants_lineup, env_data, manager_data_shane)

    def print_proj(name, proj):
        print(f"PITCHER: {name}")
        print(f"EXPECTED K: {proj['exact_k']} (Mean: {proj['mean_k']:.2f})")
        print(f"CONFIDENCE: {proj['confidence']*100:.1f}%")
        print(f"ARCHETYPE: {proj['telemetry']['Archetype']}")
        print("PROBABILITIES:")
        for line, p in proj['probabilities'].items():
            print(f"  Over {line}: {p['Over']*100:.1f}% | Under {line}: {p['Under']*100:.1f}%")
        print("-" * 40)

    print_proj("Robbie Ray", ray_proj)
    print_proj("Shane McClanahan", shane_proj)

if __name__ == "__main__":
    run_simulation()
