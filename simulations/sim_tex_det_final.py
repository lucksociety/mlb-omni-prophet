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

import os
import math
import random

# Mock stats based on research
TEX_SP = {'Name': 'MacKenzie Gore', 'Hand': 'L', 'ERA': 4.35, 'xFIP': 3.22, 'IP': 5.2, 'K/9': 12.19, 'Stuff+': 105}
DET_SP = {'Name': 'Jack Flaherty', 'Hand': 'R', 'ERA': 5.33, 'xFIP': 4.27, 'IP': 5.0, 'K/9': 8.5, 'Stuff+': 98}

TEX_LINEUP_WRC = 110.1
DET_LINEUP_WRC = 121.1

# Bullpen Tiers (using research from prior turn)
TEX_BP = {'A': 2.45, 'B': 3.50, 'C': 4.50}
DET_BP = {'A': 3.50, 'B': 4.80, 'C': 6.00}

# Environment
PARK_FACTOR = 0.98
TEMP_ADJ = 1.0 + ((50 - 72) * 0.0008) # 50 degrees
WIND_ADJ = 1.0 + (-10 * 0.004) # 10mph in
ENV_FACTOR = PARK_FACTOR * TEMP_ADJ * WIND_ADJ

def poisson_rvs(lam):
    if lam <= 0: return 0
    L = math.exp(-lam); k=0; p=1.0
    while p > L: k+=1; p*=random.random()
    return k-1

def simulate_game(n=100000):
    tex_runs = []
    det_runs = []
    for _ in range(n):
        # TEX Batting vs DET
        h_sp_mu = (DET_SP['xFIP'] / 9.0) * DET_SP['IP'] * (TEX_LINEUP_WRC/100.0) * ENV_FACTOR
        h_bp_mu = (DET_BP['B'] / 9.0) * (9.0 - DET_SP['IP']) * (TEX_LINEUP_WRC/100.0) * ENV_FACTOR
        tex_runs.append(poisson_rvs(h_sp_mu) + poisson_rvs(h_bp_mu))
        
        # DET Batting vs TEX
        a_sp_mu = (TEX_SP['xFIP'] / 9.0) * TEX_SP['IP'] * (DET_LINEUP_WRC/100.0) * ENV_FACTOR
        a_bp_mu = (TEX_BP['A'] / 9.0) * (9.0 - TEX_SP['IP']) * (DET_LINEUP_WRC/100.0) * ENV_FACTOR
        det_runs.append(poisson_rvs(a_sp_mu) + poisson_rvs(a_bp_mu))
        
    return sum(tex_runs)/n, sum(det_runs)/n

avg_tex, avg_det = simulate_game()
print(f"TEX Avg: {avg_tex:.2f}")
print(f"DET Avg: {avg_det:.2f}")
print(f"Total: {avg_tex + avg_det:.2f}")