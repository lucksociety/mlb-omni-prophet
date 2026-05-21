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
import random, math

def poisson_rvs(lam):
    if lam <= 0: return 0
    L = math.exp(-lam); k=0; p=1.0
    while p > L: k+=1; p*=random.random()
    return k-1

def nbinom_rvs(n, mu):
    if mu <= 0: return 0
    p = n / (n + mu)
    return poisson_rvs(random.gammavariate(n, (1.0-p)/p))

# Mock data
away_sp_mu = 3.0
h_bp_mu = 2.0
sp_k = 20.0

runs = []
for _ in range(1000):
    sp_runs = nbinom_rvs(sp_k, away_sp_mu)
    bp_runs = poisson_rvs(h_bp_mu)
    runs.append(sp_runs + bp_runs)

print(f"Average runs: {sum(runs)/len(runs)}")