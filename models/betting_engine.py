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
"""
MLB BETTING ENGINE — SYNDICATE UTILITIES
Implements Kelly Criterion and CLV Tracking (Chapter 1 & 11)
"""

def calculate_kelly(prob, odds, fraction=0.25):
    """
    Calculates the optimal bet size using Fractional Kelly.
    
    Args:
        prob (float): Estimated probability of winning (0.0 to 1.0).
        odds (int): American odds (e.g., -110, +130).
        fraction (float): Kelly fraction (1.0 for Full, 0.25 for Quarter, 0.125 for Eighth).
        
    Returns:
        float: Percentage of bankroll to wager.
    """
    if odds < 0:
        b = 100 / abs(odds)
    else:
        b = odds / 100
    
    q = 1.0 - prob
    # Full Kelly: f = (bp - q) / b
    f_full = (b * prob - q) / b
    
    # Fractional Kelly
    f_fractional = f_full * fraction
    
    return max(0, f_fractional)

def get_implied_prob(odds):
    """Converts American odds to implied probability."""
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    else:
        return 100 / (odds + 100)

def calculate_clv(bet_odds, closing_odds):
    """
    Calculates Closing Line Value (CLV).
    A positive result means you beat the closing line.
    """
    p_bet = get_implied_prob(bet_odds)
    p_close = get_implied_prob(closing_odds)
    
    if p_close == 0: return 0
    return (p_close / p_bet) - 1.0

if __name__ == "__main__":
    # Example usage from the Bible
    # Yankees at -150 (60% implied), model says 65% chance.
    proj_prob = 0.65
    book_odds = -150
    
    print(f"Projected Prob: {proj_prob*100:.1f}%")
    print(f"Book Odds: {book_odds}")
    
    q_kelly = calculate_kelly(proj_prob, book_odds, fraction=0.25)
    print(f"Quarter-Kelly Bet Size: {q_kelly*100:.2f}% of bankroll")
    
    # CLV check
    clv = calculate_clv(-150, -170)
    print(f"CLV if line moves to -170: {clv*100:.2f}%")