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
import math

def nb_prob(k, mu, r):
    p = r / (r + mu)
    log_p = (math.lgamma(k + r) - math.lgamma(k + 1) - math.lgamma(r)
             + r * math.log(p) + k * math.log(1 - p))
    return math.exp(log_p)

def over_under_prob(line, mu, r):
    exact = nb_prob(int(line), mu, r)
    under_p = sum(nb_prob(k, mu, r) for k in range(int(line)))
    over_p = 1.0 - under_p - exact
    return over_p, under_p, exact

mu_sugano = 3.33
r = 5.0
print("Sugano:")
for line in [2.5, 3.5, 4.5]:
    over, under, _ = over_under_prob(line, mu_sugano, r)
    print(f"O/U {line}: Over {over*100:.1f}% / Under {under*100:.1f}%")