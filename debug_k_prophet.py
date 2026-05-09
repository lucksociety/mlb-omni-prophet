
import sys
import os
import statistics

# Add the directory to path
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB/K Prophet')

from engine import KProphetEngine

def debug_k_prophet():
    engine = KProphetEngine()
    
    pitcher = {
        'Name': 'Yoshinobu Yamamoto',
        'Hand': 'R',
        'Stuff': 112,
        'K_pct': 21.8,
        'BB_pct': 6.1,
        'VAA': -4.3,
        'IP': 37.2,
        'xERA': 3.98
    }
    
    lineup = [
        {'Name': 'Carlos Correa', 'Hand': 'R', 'K_pct': 20, 'O_Swing': 26, 'Z_Contact': 88},
        {'Name': 'Yordan Alvarez', 'Hand': 'L', 'K_pct': 18, 'O_Swing': 24, 'Z_Contact': 86},
        {'Name': 'Isaac Paredes', 'Hand': 'R', 'K_pct': 14, 'O_Swing': 22, 'Z_Contact': 90},
        {'Name': 'Christian Walker', 'Hand': 'R', 'K_pct': 22, 'O_Swing': 28, 'Z_Contact': 84},
        {'Name': 'Jose Altuve', 'Hand': 'R', 'K_pct': 15, 'O_Swing': 32, 'Z_Contact': 92},
        {'Name': 'Brice Matthews', 'Hand': 'R', 'K_pct': 25, 'O_Swing': 30, 'Z_Contact': 82},
        {'Name': 'Cam Smith', 'Hand': 'R', 'K_pct': 24, 'O_Swing': 29, 'Z_Contact': 85},
        {'Name': 'Zach Cole', 'Hand': 'L', 'K_pct': 23, 'O_Swing': 26, 'Z_Contact': 84},
        {'Name': 'Christian Vazquez', 'Hand': 'R', 'K_pct': 18, 'O_Swing': 35, 'Z_Contact': 88}
    ]
    
    env = {
        'Weather': {'temp': 72, 'wind_speed': 0, 'wind_dir': 0},
        'Umpire': {'CS_pct': 17.5, 'zone_type': 'neutral'}
    }
    
    print("--- DEBUGGING K-PROPHET ---")
    
    # Test solve_physics_pk
    physics_pk = engine.solve_physics_pk(pitcher, lineup[0], env)
    print(f"Physics pK (Batter 0): {physics_pk:.4f}")
    
    # Test hyper_dimensional_monte_carlo
    exact_k, conf, metrics = engine.hyper_dimensional_monte_carlo(pitcher, lineup, env)
    print(f"Exact K: {exact_k}")
    print(f"Mean K: {metrics['mean_k']:.2f}")
    print(f"Expected BF: {metrics['expected_bf']:.1f}")
    print(f"Archetype: {metrics['Archetype']}")
    
    # Test scaling
    anchored_k_base = pitcher.get('K_pct', 22.7) / 100.0
    print(f"Anchored K Base: {anchored_k_base:.4f}")

if __name__ == "__main__":
    debug_k_prophet()
