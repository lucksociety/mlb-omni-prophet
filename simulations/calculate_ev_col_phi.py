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
import statistics
import random
from datetime import datetime

from omni_prophet_v16 import OmniProphetV18
import quant_elite_v6_6 as qe

def calculate_ev(prob, american_odds):
    if american_odds >= 100:
        decimal_odds = 1.0 + (american_odds / 100.0)
    else:
        decimal_odds = 1.0 + (100.0 / abs(american_odds))
    return (prob * decimal_odds) - 1.0

def get_k_prob(mu, line, over=True):
    # Using Monte Carlo simulation for K distribution
    sims = 100000
    under_count = 0
    for _ in range(sims):
        # We use poisson_rvs from quant_elite_v6_6 to generate simulation outcomes
        k = qe.poisson_rvs(mu)
        if k <= line:
            under_count += 1
    prob_under = under_count / sims
    return 1.0 - prob_under if over else prob_under

def run_ev_analysis():
    # Game Data Setup
    away_lineup = [
        {'Name': 'Jordan Beck', 'Hand': 'R', 'K_pct': 29.4, 'O_Swing': 32.5, 'Z_Contact': 80.0, 'wOBA': 0.295},
        {'Name': 'Tyler Freeman', 'Hand': 'R', 'K_pct': 13.9, 'O_Swing': 25.0, 'Z_Contact': 88.0, 'wOBA': 0.300},
        {'Name': 'Hunter Goodman', 'Hand': 'R', 'K_pct': 29.1, 'O_Swing': 34.0, 'Z_Contact': 78.0, 'wOBA': 0.345},
        {'Name': 'Willi Castro', 'Hand': 'S', 'K_pct': 24.0, 'O_Swing': 30.0, 'Z_Contact': 84.0, 'wOBA': 0.315},
        {'Name': 'Brenton Doyle', 'Hand': 'R', 'K_pct': 27.8, 'O_Swing': 33.0, 'Z_Contact': 81.0, 'wOBA': 0.310},
        {'Name': 'Mickey Moniak', 'Hand': 'L', 'K_pct': 25.0, 'O_Swing': 35.0, 'Z_Contact': 79.0, 'wOBA': 0.425},
        {'Name': 'Kyle Karros', 'Hand': 'R', 'K_pct': 22.0, 'O_Swing': 28.0, 'Z_Contact': 85.0, 'wOBA': 0.310},
        {'Name': 'Ezequiel Tovar', 'Hand': 'R', 'K_pct': 27.6, 'O_Swing': 31.0, 'Z_Contact': 82.0, 'wOBA': 0.290},
        {'Name': 'Jake McCarthy', 'Hand': 'L', 'K_pct': 18.0, 'O_Swing': 26.0, 'Z_Contact': 89.0, 'wOBA': 0.340}
    ]
    
    home_lineup = [
        {'Name': 'Trea Turner', 'Hand': 'R', 'K_pct': 17.6, 'O_Swing': 31.0, 'Z_Contact': 86.0, 'wOBA': 0.345},
        {'Name': 'Kyle Schwarber', 'Hand': 'L', 'K_pct': 29.8, 'O_Swing': 22.0, 'Z_Contact': 82.0, 'wOBA': 0.385},
        {'Name': 'Bryce Harper', 'Hand': 'L', 'K_pct': 21.2, 'O_Swing': 28.0, 'Z_Contact': 84.0, 'wOBA': 0.395},
        {'Name': 'Adolis Garcia', 'Hand': 'R', 'K_pct': 25.0, 'O_Swing': 33.0, 'Z_Contact': 80.0, 'wOBA': 0.300},
        {'Name': 'Brandon Marsh', 'Hand': 'L', 'K_pct': 25.6, 'O_Swing': 30.0, 'Z_Contact': 83.0, 'wOBA': 0.355},
        {'Name': 'J.T. Realmuto', 'Hand': 'R', 'K_pct': 22.8, 'O_Swing': 32.0, 'Z_Contact': 84.0, 'wOBA': 0.325},
        {'Name': 'Bryson Stott', 'Hand': 'L', 'K_pct': 14.3, 'O_Swing': 24.0, 'Z_Contact': 91.0, 'wOBA': 0.325},
        {'Name': 'Alec Bohm', 'Hand': 'R', 'K_pct': 18.0, 'O_Swing': 27.0, 'Z_Contact': 87.0, 'wOBA': 0.340},
        {'Name': 'Justin Crawford', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 85.0, 'wOBA': 0.310}
    ]

    game_data = {
        'away_team': 'COL', 'home_team': 'PHI',
        'away_sp_name': 'Tomoyuki Sugano', 'home_sp_name': 'Cristopher Sanchez',
        'away_sp_hand': 'R', 'home_sp_hand': 'L',
        'away_sp_era': 3.41, 'home_sp_era': 2.42,
        'away_sp_statcast': {
            'Name': 'Tomoyuki Sugano', 'Hand': 'R', 'Stuff': 92, 'K_pct': 15.6, 'BB_pct': 5.0,
            'VAA': -4.3, 'IP': 37.0, 'Starts': 5, 'ERA': 3.41, 'xERA': 3.60, 'LastPitchCount': 90
        },
        'home_sp_statcast': {
            'Name': 'Cristopher Sanchez', 'Hand': 'L', 'Stuff': 105, 'K_pct': 32.7, 'BB_pct': 6.5,
            'VAA': -4.6, 'IP': 48.1, 'Starts': 6, 'ERA': 2.42, 'xERA': 3.10, 'LastPitchCount': 95
        },
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'away_lineup_hands': [b['Hand'] for b in away_lineup],
        'away_lineup_statcast': away_lineup,
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'home_lineup_hands': [b['Hand'] for b in home_lineup],
        'home_lineup_statcast': home_lineup,
        'park_factor': 112, 'is_dome': False,
        'away_drs': -2, 'home_drs': 2,
        'away_manager_hook': 0, 'home_manager_hook': 0,
        'away_bp_pitches_d1': 20, 'away_bp_pitches_d2': 10,
        'home_bp_pitches_d1': 15, 'home_bp_pitches_d2': 5,
        'away_catcher': 'Hunter Goodman', 'home_catcher': 'J.T. Realmuto',
        'game_time': '13:35',
        'env': {
            'Weather': {'temp': 79, 'wind_speed': 8, 'wind_dir': 0, 'humidity': 45},
            'altitude': 40, 'rain_intensity': 0.0, 'Umpire': {'name': 'Unknown', 'zone_type': 'neutral'}
        }
    }

    # Market Odds
    markets = [
        {'name': 'Rockies Moneyline', 'odds': 245, 'type': 'ML', 'side': 'away'},
        {'name': 'Phillies Moneyline', 'odds': -305, 'type': 'ML', 'side': 'home'},
        {'name': 'Rockies +1.5 Runline', 'odds': 115, 'type': 'RL', 'side': 'away', 'line': 1.5},
        {'name': 'Phillies -1.5 Runline', 'odds': -135, 'type': 'RL', 'side': 'home', 'line': -1.5},
        {'name': 'Total Over 8.5', 'odds': -105, 'type': 'Total', 'line': 8.5, 'over': True},
        {'name': 'Total Under 8.5', 'odds': -115, 'type': 'Total', 'line': 8.5, 'over': False},
        {'name': 'YRFI (Yes)', 'odds': -110, 'type': 'YRFI', 'yes': True},
        {'name': 'NRFI (No)', 'odds': -120, 'type': 'YRFI', 'yes': False},
        {'name': 'Sugano Over 3.5 K', 'odds': 115, 'type': 'K', 'player': 'Tomoyuki Sugano', 'line': 3.5, 'over': True},
        {'name': 'Sugano Under 3.5 K', 'odds': -150, 'type': 'K', 'player': 'Tomoyuki Sugano', 'line': 3.5, 'over': False},
        {'name': 'Sanchez Over 7.5 K', 'odds': -105, 'type': 'K', 'player': 'Cristopher Sanchez', 'line': 7.5, 'over': True},
        {'name': 'Sanchez Under 7.5 K', 'odds': -125, 'type': 'K', 'player': 'Cristopher Sanchez', 'line': 7.5, 'over': False},
        {'name': 'Kyle Schwarber HR', 'odds': 210, 'type': 'HR', 'player': 'Kyle Schwarber'},
        {'name': 'Rockies by 4 or more runs', 'odds': 750, 'type': 'Margin', 'side': 'away', 'min': 4},
    ]

    # Initialize Engine
    omni = OmniProphetV18()
    
    # Run full Omni for probabilities
    sim_results = omni.run_omni_simulation(game_data, market_odds={'Total Over 8.5': -105}, auto_record=False)
    
    # Re-run simulation logic to get distributions (since run_omni_simulation doesn't return ar/hr)
    away_sp_stats = game_data['away_sp_statcast'].copy()
    home_sp_stats = game_data['home_sp_statcast'].copy()
    away_sp_stats['Blended'] = away_sp_stats['ERA']
    home_sp_stats['Blended'] = home_sp_stats['ERA']
    away_sp_stats['Exp_IP'] = 5.5
    home_sp_stats['Exp_IP'] = 6.0
    away_sp_stats['K/9'] = (away_sp_stats['K_pct']/100.0) * 8.5 # fallback
    home_sp_stats['K/9'] = (home_sp_stats['K_pct']/100.0) * 8.5 # fallback
    away_sp_stats['Stuff+'] = away_sp_stats['Stuff']
    home_sp_stats['Stuff+'] = home_sp_stats['Stuff']
    away_bp = {'A': 2.5, 'B': 6.0, 'C': 6.0, 'AVG': 4.1}
    home_bp = {'A': 2.6, 'B': 6.7, 'C': 6.7, 'AVG': 4.1}
    env_factor = 1.16
    
    results = qe.simulate_game_v6_5(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                                   101.8, 102.8, env_factor)
    ar, hr, ak, hk = results
    n = len(ar)
    
    # Distribution-based probabilities
    sim_probs = {
        'ML_away': sum(1 for i in range(n) if ar[i] > hr[i]) / n,
        'ML_home': sum(1 for i in range(n) if hr[i] > ar[i]) / n,
        'RL_away_1.5': sum(1 for i in range(n) if ar[i] + 1.5 > hr[i]) / n,
        'RL_home_1.5': sum(1 for i in range(n) if hr[i] - 1.5 > ar[i]) / n,
        'Total_O8.5': sum(1 for i in range(n) if ar[i] + hr[i] > 8.5) / n,
        'Total_U8.5': sum(1 for i in range(n) if ar[i] + hr[i] < 8.5) / n,
        'Margin_away_4': sum(1 for i in range(n) if ar[i] - hr[i] >= 4) / n,
        'YRFI': sim_results['yrfi_prob'] / 100.0,
        'NRFI': 1.0 - (sim_results['yrfi_prob'] / 100.0),
    }

    # K Projections
    away_k_mu = sim_results['away_k']
    if isinstance(away_k_mu, dict): away_k_mu = away_k_mu.get('mu', 4.0)
    home_k_mu = sim_results['home_k']
    if isinstance(home_k_mu, dict): home_k_mu = home_k_mu.get('mu', 6.0)

    hr_dict = {p['player']: p['prob'] for p in sim_results['hr_picks']}

    ev_list = []
    for m in markets:
        prob = 0
        if m['type'] == 'ML':
            prob = sim_probs[f"ML_{m['side']}"]
        elif m['type'] == 'RL':
            prob = sim_probs[f"RL_{m['side']}_{abs(m['line'])}"]
        elif m['type'] == 'Total':
            prob = sim_probs[f"Total_{'O' if m['over'] else 'U'}{m['line']}"]
        elif m['type'] == 'YRFI':
            prob = sim_probs['YRFI' if m['yes'] else 'NRFI']
        elif m['type'] == 'K':
            mu = away_k_mu if m['player'] == 'Tomoyuki Sugano' else home_k_mu
            prob = get_k_prob(mu, m['line'], m['over'])
        elif m['type'] == 'HR':
            prob = hr_dict.get(m['player'], 0.05)
        elif m['type'] == 'Margin':
            prob = sim_probs[f"Margin_{m['side']}_{m['min']}"]
            
        ev = calculate_ev(prob, m['odds'])
        ev_list.append({'name': m['name'], 'odds': m['odds'], 'prob': prob, 'ev': ev})

    ev_list.sort(key=lambda x: x['ev'], reverse=True)
    
    print("\n" + "="*50)
    print("TOP 10 HIGHEST EV BETS (COL @ PHI)")
    print("="*50)
    for i, res in enumerate(ev_list[:10]):
        print(f"{i+1}. {res['name']} ({res['odds']})")
        print(f"   Prob: {res['prob']:.1%}, EV: {res['ev']:.1%}")
    print("="*50)

if __name__ == '__main__':
    run_ev_analysis()