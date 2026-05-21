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

from quant_elite_v6_4 import run_v6_4_protocol

# LAA @ KCR test (from the model's own test case)
laa_lineup = [('Neto', 'R'), ('Trout', 'R'), ('Adell', 'R'), ('Soler', 'R'), ('Peraza', 'R'), ('Schanuel', 'L'), ('Grissom', 'R'), ('O\'Hoppe', 'R'), ('Teodosio', 'R')]
kcr_lineup = [('Garcia', 'R'), ('Witt', 'R'), ('Pasquantino', 'L'), ('Perez', 'R'), ('Jensen', 'L'), ('Massey', 'L'), ('Caglianone', 'L'), ('Collins', 'S'), ('Isbel', 'L')]

print("🚀 RUNNING QUANT-ELITE V6.4 PREFLIGHT...")
try:
    run_v6_4_protocol('LAA', 'KCR', 'Walbert Urena', 'Cole Ragans', 'R', 'L',
                      2.35, 6.00, laa_lineup, kcr_lineup, 101, False, 62, 9, 60, 50, 912, 0.0)
    print("\n✅ PREFLIGHT SUCCESSFUL: V6.4 ENGINE OPERATIONAL.")
except Exception as e:
    print(f"\n❌ PREFLIGHT FAILED: {str(e)}")
    sys.exit(1)