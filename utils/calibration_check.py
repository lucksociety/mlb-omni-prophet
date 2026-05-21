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
MLB CALIBRATION CHECK — PRE-SIMULATION FEEDBACK LOOP
Reads predictions_history.csv and K Prophet/performance_tracker.csv
to detect systematic biases before running new simulations.
"""
import csv
import os
import statistics
from datetime import datetime

BASE_DIR = ROOT_DIR
DATA_DIR = os.path.join(ROOT_DIR, 'data')

def load_predictions_history(filepath=None):
    """Load game total predictions and actuals."""
    if filepath is None:
        filepath = os.path.join(DATA_DIR, os.path.join(ROOT_DIR, 'data', 'predictions_history.csv'))
    if not os.path.exists(filepath):
        return []
    results = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                results.append({
                    'date': row.get('Date', ''),
                    'matchup': f"{row.get('Away_Team', '?')} @ {row.get('Home_Team', '?')}",
                    'pred_away': float(row.get('Pred_Away_Score', 0)),
                    'pred_home': float(row.get('Pred_Home_Score', 0)),
                    'pred_total': float(row.get('Pred_Total', 0)),
                    'actual_away': float(row.get('Result_Away_Score', 0)),
                    'actual_home': float(row.get('Result_Home_Score', 0)),
                    'actual_total': float(row.get('Result_Total', 0)),
                    'ml_edge': row.get('ML_Edge', ''),
                    'result_winner': row.get('Result_Winner', ''),
                })
            except (ValueError, TypeError):
                continue
    return results

def load_k_tracker(filepath=None):
    """Load K-prop prediction results."""
    if filepath is None:
        filepath = os.path.join(ROOT_DIR, 'models', 'K Prophet', 'performance_tracker.csv')
    if not os.path.exists(filepath):
        return []
    results = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Type') != 'Pitcher Prop':
                continue
            try:
                actual = row.get('Actual', 'TBD')
                if actual == 'TBD' or not actual:
                    continue
                projection = float(row.get('Projection', 0))
                actual_k = int(actual)
                result = row.get('Result', 'N/A')
                pnl = float(row.get('PNL', 0))
                results.append({
                    'date': row.get('Date', ''),
                    'name': row.get('Name', '?'),
                    'matchup': row.get('Matchup', ''),
                    'projection': projection,
                    'actual': actual_k,
                    'error': projection - actual_k,
                    'abs_error': abs(projection - actual_k),
                    'bet': row.get('Bet', ''),
                    'result': result,
                    'pnl': pnl,
                })
            except (ValueError, TypeError):
                continue
    return results

def classify_game_archetype(away_era, home_era, away_ip=100, home_ip=100):
    """V19: Classify game into archetype for context-aware calibration.
    Added rookie_debut for starters with minimal IP."""
    avg_era = (away_era + home_era) / 2.0
    era_diff = abs(away_era - home_era)
    
    if away_ip < 10 or home_ip < 10:
        return 'rookie_debut'
    if away_era < 3.50 and home_era < 3.50:
        return 'ace_duel'
    elif away_era > 4.50 and home_era > 4.50:
        return 'slugfest'
    elif era_diff > 1.50:
        return 'mismatch'
    else:
        return 'standard'

# V19: Per-archetype calibration modifiers
ARCHETYPE_MODIFIERS = {
    'rookie_debut': -0.75, # Conservative on debut runs due to short leash
    'ace_duel': -1.5,     # Cap total down hard — aces suppress runs
    'slugfest': +1.0,     # Floor total up — bad pitchers yield runs
    'mismatch': 0.0,      # No flat mod — let the ERA diff do the work
    'standard': 0.0,      # No mod — engine should handle these
}

def analyze_total_bias(history, n_recent=10):
    """V17: Context-aware bias detection. No more flat modifiers."""
    recent = history[-n_recent:] if len(history) >= n_recent else history
    if not recent:
        return {'bias': 'INSUFFICIENT_DATA', 'modifier': 0.0, 'n': 0}
    
    errors = [g['actual_total'] - g['pred_total'] for g in recent]
    mean_error = statistics.mean(errors)
    
    under_count = sum(1 for e in errors if e > 0)
    over_count = sum(1 for e in errors if e < 0)
    
    # V17: Detect if errors are truly systematic or just high-variance
    if len(errors) >= 3:
        error_stdev = statistics.stdev(errors)
    else:
        error_stdev = 0.0
    
    bias = 'NEUTRAL'
    modifier = 0.0
    
    # V17: Only apply flat modifier if BOTH directional AND low-variance
    # High variance = bidirectional errors = flat modifier is useless
    if error_stdev > 3.0:
        bias = 'HIGH_VARIANCE'
        modifier = 0.0  # Don't apply flat mod — it won't help
    elif mean_error > 1.5:
        bias = 'SYSTEMATIC_UNDER'
        modifier = min(mean_error * 0.10, 0.75)
    elif mean_error < -1.5:
        bias = 'SYSTEMATIC_OVER'
        modifier = max(mean_error * 0.10, -0.75)
    elif under_count >= n_recent * 0.7:
        bias = 'DIRECTIONAL_UNDER'
        modifier = 0.15
    elif over_count >= n_recent * 0.7:
        bias = 'DIRECTIONAL_OVER'
        modifier = -0.15
    
    return {
        'bias': bias,
        'modifier': modifier,
        'mean_error': mean_error,
        'mae': statistics.mean([abs(e) for e in errors]),
        'error_stdev': error_stdev,
        'under_pct': under_count / len(recent) * 100,
        'over_pct': over_count / len(recent) * 100,
        'n': len(recent),
        'archetype_modifiers': ARCHETYPE_MODIFIERS,
    }

def analyze_k_bias(k_results, n_recent=20):
    """Detect systematic bias on K-prop projections."""
    recent = k_results[-n_recent:] if len(k_results) >= n_recent else k_results
    if not recent:
        return {'bias': 'INSUFFICIENT_DATA', 'k9_modifier': 1.0, 'n': 0}
    
    errors = [r['error'] for r in recent]  # positive = we overshot
    mean_signed_error = statistics.mean(errors)
    mae = statistics.mean([abs(e) for e in errors])
    
    # Win/Loss tracking
    wins = sum(1 for r in recent if r['result'] == 'Win')
    losses = sum(1 for r in recent if r['result'] == 'Loss')
    hit_rate = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0
    
    # PNL
    total_pnl = sum(r['pnl'] for r in recent)
    
    # Exact hit rate
    exact_hits = sum(1 for r in recent if abs(r['error']) < 1.0)
    within_one = sum(1 for r in recent if abs(r['error']) <= 1.5)
    
    k9_modifier = 1.0
    bias = 'NEUTRAL'
    if mean_signed_error > 1.0:
        bias = 'SYSTEMATIC_OVER'
        k9_modifier = 1.0 - (mean_signed_error * 0.03)  # Reduce K/9 by 3% per unit of overshoot
        k9_modifier = max(0.90, k9_modifier)
    elif mean_signed_error < -1.0:
        bias = 'SYSTEMATIC_UNDER'
        k9_modifier = 1.0 + (abs(mean_signed_error) * 0.02)
        k9_modifier = min(1.10, k9_modifier)
    
    # Over/Under bet-type breakdown
    over_bets = [r for r in recent if r['bet'] and 'over' in r['bet'].lower()]
    under_bets = [r for r in recent if r['bet'] and 'under' in r['bet'].lower()]
    over_wins = sum(1 for r in over_bets if r['result'] == 'Win')
    under_wins = sum(1 for r in under_bets if r['result'] == 'Win')
    
    return {
        'bias': bias,
        'k9_modifier': k9_modifier,
        'mean_signed_error': mean_signed_error,
        'mae': mae,
        'hit_rate': hit_rate,
        'exact_hit_pct': exact_hits / len(recent) * 100,
        'within_1_5_pct': within_one / len(recent) * 100,
        'total_pnl': total_pnl,
        'wins': wins,
        'losses': losses,
        'over_record': f"{over_wins}/{len(over_bets)}" if over_bets else 'N/A',
        'under_record': f"{under_wins}/{len(under_bets)}" if under_bets else 'N/A',
        'n': len(recent),
    }

def analyze_ml_accuracy(history, n_recent=10):
    """Analyze moneyline direction accuracy."""
    recent = history[-n_recent:] if len(history) >= n_recent else history
    if not recent:
        return {'accuracy': 0, 'correct': 0, 'total': 0, 'n': 0}
    
    correct = 0
    total = 0
    for g in recent:
        if g['ml_edge'] and g['result_winner']:
            total += 1
            if g['ml_edge'] == g['result_winner']:
                correct += 1
    
    return {
        'accuracy': correct / total * 100 if total > 0 else 0,
        'correct': correct,
        'total': total,
        'n': len(recent),
    }


def analyze_pitcher_k_history(k_results):
    """Analyze per-pitcher K prediction accuracy to find repeat offenders."""
    from collections import defaultdict
    pitcher_data = defaultdict(list)
    
    for r in k_results:
        pitcher_data[r['name']].append({
            'date': r['date'],
            'projection': r['projection'],
            'actual': r['actual'],
            'error': r['error'],
            'abs_error': r['abs_error'],
        })
    
    # Find pitchers with multiple appearances and consistent bias
    repeat_offenders = []
    worst_misses = []
    
    for name, entries in pitcher_data.items():
        if len(entries) >= 2:
            avg_error = sum(e['error'] for e in entries) / len(entries)
            avg_abs_error = sum(e['abs_error'] for e in entries) / len(entries)
            if abs(avg_error) >= 1.5 or avg_abs_error >= 2.5:
                repeat_offenders.append({
                    'name': name,
                    'n': len(entries),
                    'avg_error': avg_error,
                    'avg_abs_error': avg_abs_error,
                    'direction': 'OVER-PROJ' if avg_error > 0 else 'UNDER-PROJ',
                })
        
        # Track worst single misses
        for e in entries:
            if e['abs_error'] >= 5:
                worst_misses.append({
                    'name': name,
                    'date': e['date'],
                    'projection': e['projection'],
                    'actual': e['actual'],
                    'error': e['error'],
                })
    
    repeat_offenders.sort(key=lambda x: x['avg_abs_error'], reverse=True)
    worst_misses.sort(key=lambda x: abs(x['error']), reverse=True)
    
    return {
        'repeat_offenders': repeat_offenders[:10],
        'worst_misses': worst_misses[:10],
        'total_pitchers_tracked': len(pitcher_data),
    }


def run_calibration_check():
    """Execute the full calibration check and return modifiers."""
    print("====================================================================")
    print("          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ")
    print("====================================================================\n")
    
    history = load_predictions_history()
    k_results = load_k_tracker()
    
    # 1. Total Bias
    total_analysis = analyze_total_bias(history)
    print(f"-- 1. GAME TOTAL BIAS ANALYSIS (last {total_analysis['n']} games) ----------")
    if total_analysis['n'] > 0:
        print(f"  Bias Detected: {total_analysis['bias']}")
        print(f"  Mean Error (Actual - Predicted): {total_analysis['mean_error']:+.2f} runs")
        print(f"  MAE: {total_analysis['mae']:.2f} runs")
        print(f"  Undershot: {total_analysis['under_pct']:.0f}% | Overshot: {total_analysis['over_pct']:.0f}%")
        print(f"  -> CALIBRATION MODIFIER: {total_analysis['modifier']:+.2f} runs to total")
    else:
        print("  [INSUFFICIENT DATA]")
    
    # 2. K-Prop Bias
    k_analysis = analyze_k_bias(k_results)
    print(f"\n-- 2. K-PROP BIAS ANALYSIS (last {k_analysis['n']} props) ---------------")
    if k_analysis['n'] > 0:
        print(f"  Bias Detected: {k_analysis['bias']}")
        print(f"  Mean Signed Error: {k_analysis['mean_signed_error']:+.2f} K's")
        print(f"  MAE: {k_analysis['mae']:.2f} K's")
        print(f"  Bet Record: {k_analysis['wins']}W - {k_analysis['losses']}L ({k_analysis['hit_rate']:.1f}%)")
        print(f"  Total PNL: {k_analysis['total_pnl']:+.2f} units")
        print(f"  Exact Hit %: {k_analysis['exact_hit_pct']:.1f}% | Within ±1.5: {k_analysis['within_1_5_pct']:.1f}%")
        print(f"  Over Bets: {k_analysis.get('over_record', 'N/A')} | Under Bets: {k_analysis.get('under_record', 'N/A')}")
        print(f"  -> K/9 MODIFIER: {k_analysis['k9_modifier']:.3f}x")
    else:
        print("  [INSUFFICIENT DATA]")
    
    # 3. ML Direction
    ml_analysis = analyze_ml_accuracy(history)
    print(f"\n-- 3. MONEYLINE DIRECTION ACCURACY ------------------------------")
    if ml_analysis['total'] > 0:
        print(f"  Direction Correct: {ml_analysis['correct']}/{ml_analysis['total']} ({ml_analysis['accuracy']:.1f}%)")
    else:
        print("  [INSUFFICIENT DATA]")
    
    # 4. Per-Pitcher K Intelligence
    pitcher_intel = analyze_pitcher_k_history(k_results)
    print(f"\n-- 4. PER-PITCHER K INTELLIGENCE ({pitcher_intel['total_pitchers_tracked']} pitchers tracked) --")
    
    if pitcher_intel['repeat_offenders']:
        print("  REPEAT OFFENDERS (consistent mis-projection):")
        for p in pitcher_intel['repeat_offenders'][:5]:
            print(f"    {p['name']:20s} | {p['n']} starts | Avg Error: {p['avg_error']:+.1f} K's | {p['direction']}")
    
    if pitcher_intel['worst_misses']:
        print("  WORST SINGLE MISSES (>=5 K error):")
        for m in pitcher_intel['worst_misses'][:5]:
            print(f"    Pred: {m['projection']:.1f} -> Actual: {m['actual']} | Error: {m['error']:+.1f}")
    
    print(f"\n{'='*66}")
    
    return {
        'total_modifier': total_analysis.get('modifier', 0.0),
        'k9_modifier': k_analysis.get('k9_modifier', 1.0),
        'total_bias': total_analysis.get('bias', 'NEUTRAL'),
        'k_bias': k_analysis.get('bias', 'NEUTRAL'),
        'pitcher_offenders': pitcher_intel.get('repeat_offenders', []),
        'archetype_modifiers': total_analysis.get('archetype_modifiers', ARCHETYPE_MODIFIERS),
        'error_stdev': total_analysis.get('error_stdev', 0.0),
    }

if __name__ == '__main__':
    modifiers = run_calibration_check()
    print(f"\n  ACTIVE MODIFIERS FOR NEXT SIMULATION:")
    print(f"    Total Adj:  {modifiers['total_modifier']:+.2f}")
    print(f"    K/9 Factor: {modifiers['k9_modifier']:.3f}x")