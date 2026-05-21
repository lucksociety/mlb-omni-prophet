import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)
#!/usr/bin/env python3
import statistics
from quant_elite_v8 import simulate_game_v8, get_alpha_s

def validate_correlation():
    print("--- V8.0 CORRELATION VALIDATION ---")
    
    # Test Case 1: Symmetric Matchup (League Average)
    mu_a, mu_b = 4.5, 4.5
    sp_stats = {'Blended': 4.5, 'Exp_IP': 5.5, 'Stuff+': 100, 'K/9': 8.5}
    bp = {'A': 3.5, 'B': 4.5, 'C': 7.0, 'AVG': 4.15}
    
    ar, hr, _, _ = simulate_game_v8(sp_stats, sp_stats, bp, bp, 100, 100, 1.0)
    r = statistics.correlation(ar, hr)
    print(f"Symmetric Matchup (mu=4.5): Pearson r = {r:.4f} (Target 0.15)")

    # Test Case 2: Asymmetric Matchup (Ace vs Gas Can)
    mu_a_low, mu_b_high = 2.5, 6.5
    sp_a = {'Blended': 2.5, 'Exp_IP': 6.5, 'Stuff+': 115, 'K/9': 10.5}
    sp_b = {'Blended': 6.5, 'Exp_IP': 4.5, 'Stuff+': 85, 'K/9': 6.5}
    
    ar, hr, _, _ = simulate_game_v8(sp_a, sp_b, bp, bp, 110, 90, 1.0)
    r = statistics.correlation(ar, hr)
    print(f"Asymmetric Matchup (2.5 vs 6.5): Pearson r = {r:.4f} (Target 0.15)")

    # Test Case 3: High Run Environment (Coors Style)
    ar, hr, _, _ = simulate_game_v8(sp_stats, sp_stats, bp, bp, 120, 120, 1.35)
    r = statistics.correlation(ar, hr)
    print(f"High Environment (Park Factor 1.35): Pearson r = {r:.4f} (Target 0.15)")

if __name__ == '__main__':
    validate_correlation()