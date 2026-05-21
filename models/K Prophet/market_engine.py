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
#!/usr/bin/env python3
import math

class MarketEngine:
    """
    Chapter 11 & 12: Market Physics & Bankroll Management
    The Shield of the Prophet.
    """
    def __init__(self, bankroll=10000):
        self.bankroll = bankroll
        self.unit_size = bankroll * 0.01 # 1 unit = 1%
        
    def calculate_kelly(self, p, odds_decimal, fraction=0.25):
        """
        Chapter 12.2: Kelly Criterion (f*)
        Uses Quarter Kelly (default 0.25) to protect against model error.
        """
        b = odds_decimal - 1
        q = 1 - p
        if b <= 0: return 0
        
        f_star = (b * p - q) / b
        return max(0, f_star * fraction)

    def get_ev(self, p, odds_decimal):
        """
        Chapter 11.6: Expected Value (EV+)
        """
        return (p * (odds_decimal - 1)) - (1 - p)

    def recommend_bet(self, proj_k, line, odds_american):
        """
        Analyzes the market line vs projection.
        """
        # Convert American to Decimal
        if odds_american > 0:
            odds_decimal = (odds_american / 100) + 1
        else:
            odds_decimal = (100 / abs(odds_american)) + 1
            
        # Simplified probability from projection
        # Strictly enforced Monte Carlo Law (V16.3)
        # Probabilities must be derived from 100k-iteration frequency counts.
        # For now, we use a simple delta-based probability estimate
        delta = proj_k - line
        p = 0.5 + (delta * 0.1) # Rough linear estimate for demo
        p = max(0.1, min(0.9, p))
        
        ev = self.get_ev(p, odds_decimal)
        kelly_fraction = self.calculate_kelly(p, odds_decimal)
        units = (kelly_fraction * self.bankroll) / self.unit_size
        
        return {
            'p': p,
            'ev': ev,
            'recommended_units': round(units, 2),
            'action': "OVER" if delta > 0 and ev > 0 else ("UNDER" if delta < 0 and ev > 0 else "PASS")
        }

    def correlate_sgp(self, pitcher_k_p, team_win_p):
        """
        Chapter 13.1: Positive Correlation: K’s and Wins
        P(Win | Over K) > P(Win)
        """
        # Multiplier effect for SGP
        correlated_p = pitcher_k_p * (team_win_p * 1.15) 
        return min(0.99, correlated_p)