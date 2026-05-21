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
import math, random, statistics
from quant_elite_v6_5 import simulate_game_v6_5, ARCHETYPES, CATCHER_TIERS

# MLB QUANT-PROPHET V13.0: CWS @ SD 2026-05-02
# FORENSIC DATA OVERRIDE (Verified 2026 Statcast Telemetry)

def run_forensic_sim():
    random.seed(20260502)
    N_SIMS = 100000

    # 1. Pitcher Forensic Data
    # Sean Burke (CWS) - North-South
    away_sp_stats = {
        'Name': 'Sean Burke',
        'Hand': 'R',
        'Blended': 3.45, # Blended 2026 ERA (3.21) and xERA (3.74)
        'Exp_IP': 5.8,   # Research suggests deeper leash for Burke today
        'K/9': 7.8,      # Adjusted 2026 K/9
        'Stuff+': 111,
        'Archetype': 'North-South'
    }

    # Michael King (SD) - East-West
    home_sp_stats = {
        'Name': 'Michael King',
        'Hand': 'R',
        'Blended': 2.95, # Blended 2026 ERA (2.41) and xERA (3.62)
        'Exp_IP': 6.2,   # King workhorse status
        'K/9': 10.2,     # Elite K rate verified
        'Stuff+': 108,
        'Archetype': 'East-West'
    }

    # 2. Lineup Matrix
    # CWS wRC+ vs E-W: 92 (Adjusted for recent slump)
    away_wrc = 92
    # SD wRC+ vs N-S: 108 (High rank vs Vertical Curve)
    home_wrc = 108

    # 3. Environmental Factor
    # Park 96, Temp 67, Humidity 81, Wind 10 (L-R)
    # ADI 98.5
    env_factor = 0.94 # Combined atmospheric and park dampening

    # 4. Bullpen Tiers
    # CWS: Dominguez available but thin middle
    away_bp = {'A': 3.20, 'B': 4.80, 'C': 7.50}
    # SD: Elite rest, Mason Miller active
    home_bp = {'A': 2.10, 'B': 3.80, 'C': 5.50}

    # 5. Umpire & Catcher
    umpire_zone = 'tight' # Sean Barber
    # Catcher framing mods (from V6.5 Bible)
    # Quero: 0.85, Campusano: 1.0 (Neutral)
    away_cadj = 0.85
    home_cadj = 1.0
    
    # Shadow Boost (5:40 PM PT start)
    shadow_boost = 1.05 # Late afternoon shadows at Petco
    
    # Apply Mods to K/9
    away_sp_stats['K/9'] *= away_cadj * shadow_boost
    home_sp_stats['K/9'] *= home_cadj * shadow_boost

    # Execute Chaos Engine
    ar, hr, a_k, h_k = simulate_game_v6_5(
        away_sp_stats, home_sp_stats, away_bp, home_bp,
        away_wrc, home_wrc, env_factor, 
        rain_intensity=0.0, runs_to_blowout=6,
        away_drs=0, home_drs=3, umpire_zone=umpire_zone
    )

    # Statistical Synthesis
    n = len(ar)
    aw = sum(1 for i in range(n) if ar[i] > hr[i])
    hw = sum(1 for i in range(n) if hr[i] > ar[i])
    total_runs = [ar[i] + hr[i] for i in range(n)]
    
    print(f"--- V13.0 FORENSIC SIMULATION RESULTS ---")
    print(f"Away (CWS): {sum(ar)/n:.2f} runs | Win Prob: {aw/n*100:.1f}%")
    print(f"Home (SD): {sum(hr)/n:.2f} runs | Win Prob: {hw/n*100:.1f}%")
    print(f"Total Combined: {sum(total_runs)/n:.2f} runs")
    print(f"Strikeout Medians: {away_sp_stats['Name']} {statistics.median(a_k)} | {home_sp_stats['Name']} {statistics.median(h_k)}")
    print(f"------------------------------------------")

if __name__ == '__main__':
    run_forensic_sim()