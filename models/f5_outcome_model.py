"""
MLB F5 OUTCOME MODEL V1.0
=========================
Isolates the first 15 outs (5 innings) of a game to provide 
high-precision F5 Moneyline and Spread projections.

Key Logic:
- Starters are assumed to have a 'settled-in' bonus in the F5.
- TTT (Third Time Through) penalty is drastically reduced for F5.
- Bullpen is only used if Starter's Exp_IP < 5.
"""
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


import math
import random
import statistics
from typing import Dict, List, Any

# Mocking parts of QE for standalone functionality if needed, 
# but ideally it imports from quant_elite.
import quant_elite_v6_6 as qe
from intelligence_hub import HUB

class F5Engine:
    def __init__(self, n_sims: int = 25000):
        self.n_sims = n_sims

    def simulate_f5(self, away_sp_stats: Dict[str, Any], home_sp_stats: Dict[str, Any],
                    away_bp: Dict[str, Any], home_bp: Dict[str, Any],
                    away_wrc: float, home_wrc: float, env_factor: float,
                    game_id: str = None) -> Dict[str, Any]:
        
        ar_f5 = []
        hr_f5 = []
        
        # V20 SYNC: Dynamic Performance Boost based on K-Prophet Stuff+
        # Whiff-heavy pitchers (high Stuff+) are more reliable in F5
        away_p_name = away_sp_stats.get('Name', 'AwaySP')
        home_p_name = home_sp_stats.get('Name', 'HomeSP')
        
        away_stuff = HUB.get(f"Stuff_{away_p_name}", 100, game_id=game_id)
        home_stuff = HUB.get(f"Stuff_{home_p_name}", 100, game_id=game_id)
        
        # Standard boost is 0.92 (lower = more effective)
        away_boost = 0.92 - ((away_stuff - 100) * 0.001)
        home_boost = 0.92 - ((home_stuff - 100) * 0.001)
        
        # Adjusted Mu for F5 (scaled to 5 innings)
        away_f5_mu = (away_sp_stats['Blended'] / 9.0) * 5.0 * (home_wrc / 100.0) * env_factor * away_boost
        home_f5_mu = (home_sp_stats['Blended'] / 9.0) * 5.0 * (away_wrc / 100.0) * env_factor * home_boost
        
        for _ in range(self.n_sims):
            # Away Pitcher vs Home Lineup (Home Runs)
            h_runs = qe.nbinom_rvs(40, away_f5_mu)
            
            # Home Pitcher vs Away Lineup (Away Runs)
            a_runs = qe.nbinom_rvs(40, home_f5_mu)
            
            # Bullpen intervention if starter expected to go < 5
            # (Heuristic: if they get shelled in the first 5, they might leave early)
            if a_runs >= 4 and away_sp_stats['Exp_IP'] < 5.0:
                # Add a bit of bullpen chaos for the last inning(s)
                a_runs += qe.poisson_rvs(away_bp['B'] / 9.0 * 1.5)
            
            if h_runs >= 4 and home_sp_stats['Exp_IP'] < 5.0:
                h_runs += qe.poisson_rvs(home_bp['B'] / 9.0 * 1.5)
                
            ar_f5.append(a_runs)
            hr_f5.append(h_runs)
            
        aw = sum(1 for i in range(self.n_sims) if ar_f5[i] > hr_f5[i])
        hw = sum(1 for i in range(self.n_sims) if hr_f5[i] > ar_f5[i])
        ties = self.n_sims - aw - hw
        
        # V20.1 Fix: Ensure Win Probs are attributed to the correct team (Away=Mariners, Home=Astros)
        # aw = Away Wins (Mariners scored more), hw = Home Wins (Astros scored more)
        return {
            'away_mu': sum(ar_f5) / self.n_sims,
            'home_mu': sum(hr_f5) / self.n_sims,
            'away_win_prob': (aw + (ties * 0.48)) / self.n_sims * 100,
            'home_win_prob': (hw + (ties * 0.52)) / self.n_sims * 100,
            'tie_prob': (ties / self.n_sims) * 100
        }

if __name__ == "__main__":
    # Test Logic
    engine = F5Engine()
    # Mock data
    away_sp = {'Blended': 3.50, 'Exp_IP': 5.8}
    home_sp = {'Blended': 4.20, 'Exp_IP': 5.2}
    away_bp = {'B': 4.50}
    home_bp = {'B': 4.80}
    
    res = engine.simulate_f5(away_sp, home_sp, away_bp, home_bp, 105, 95, 1.0)
    print(f"F5 Projection: {res['away_mu']:.2f} - {res['home_mu']:.2f}")
    print(f"F5 ML: Away {res['away_win_prob']:.1f}% | Home {res['home_win_prob']:.1f}%")