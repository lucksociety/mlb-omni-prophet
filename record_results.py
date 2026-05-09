#!/usr/bin/env python3
"""
MLB RECORD RESULTS — Post-Game Data Entry Tool
Updates predictions_history.csv, K Prophet/performance_tracker.csv, 
and audit JSON files with actual game results.

Usage:
  python3 record_results.py                    # Interactive mode
  python3 record_results.py --date 2026-05-02  # Show pending for specific date
"""
import csv
import json
import os
import sys
import glob
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICTIONS_CSV = os.path.join(BASE_DIR, 'predictions_history.csv')
K_TRACKER_CSV = os.path.join(BASE_DIR, 'K Prophet', 'performance_tracker.csv')
AUDITS_DIR = os.path.join(BASE_DIR, 'audits')


def find_pending_predictions(date_filter=None):
    """Find predictions without results filled in."""
    pending = []
    if not os.path.exists(PREDICTIONS_CSV):
        return pending

    with open(PREDICTIONS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if not row.get('Result_Away_Score') and not row.get('Result_Winner'):
                if date_filter and row.get('Date') != date_filter:
                    continue
                pending.append({'row_index': i + 1, **row})  # +1 for header
    return pending


def find_pending_k_props(date_filter=None):
    """Find K-prop predictions without actuals."""
    pending = []
    if not os.path.exists(K_TRACKER_CSV):
        return pending

    with open(K_TRACKER_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            actual_val = row.get('Actual')
            actual = str(actual_val).strip() if actual_val is not None else ''
            if actual in ('TBD', '', 'None'):
                if row.get('Type') != 'Pitcher Prop':
                    continue
                if date_filter and row.get('Date') != date_filter:
                    continue
                pending.append({'row_index': i + 1, **row})
    return pending


def update_predictions_csv(row_index, away_score, home_score):
    """Update a specific row in predictions_history.csv with results."""
    rows = []
    headers = None

    with open(PREDICTIONS_CSV, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
            rows.append(row)

    if row_index >= len(rows):
        print(f"  ❌ Row {row_index} not found.")
        return False

    # Find column indices
    h = {name: idx for idx, name in enumerate(headers)}
    winner = rows[row_index][h.get('Away_Team', 1)] if away_score > home_score else rows[row_index][h.get('Home_Team', 2)]
    total = away_score + home_score

    # Update results columns — handle both old and new format
    for col_name, val in [
        ('Result_Away_Score', str(away_score)),
        ('Result_Home_Score', str(home_score)),
        ('Result_Winner', winner),
        ('Result_Total', str(total)),
    ]:
        if col_name in h:
            rows[row_index][h[col_name]] = val

    with open(PREDICTIONS_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return True


def update_k_tracker(row_index, actual_k, bet='', odds='', result='', pnl='0.0'):
    """Update a specific row in performance_tracker.csv with K actual."""
    rows = []
    headers = None

    with open(K_TRACKER_CSV, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
            rows.append(row)

    if row_index >= len(rows):
        print(f"  ❌ Row {row_index} not found.")
        return False

    h = {name: idx for idx, name in enumerate(headers)}

    for col_name, val in [
        ('Actual', str(actual_k)),
        ('Bet', bet),
        ('Odds', str(odds)),
        ('Result', result),
        ('PNL', str(pnl)),
    ]:
        if col_name in h and val:
            rows[row_index][h[col_name]] = val

    with open(K_TRACKER_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return True


def update_audit_json(away_team, home_team, date_str, away_score, home_score,
                      away_sp_k=None, home_sp_k=None):
    """Update audit JSON with results."""
    pattern = os.path.join(AUDITS_DIR, f"audit_{away_team}_{home_team}_{date_str}*.json")
    files = glob.glob(pattern)

    for filepath in files:
        with open(filepath, 'r') as f:
            audit = json.load(f)

        winner = away_team if away_score > home_score else home_team
        audit['results'] = {
            'status': 'COMPLETE',
            'away_score': away_score,
            'home_score': home_score,
            'winner': winner,
            'total': away_score + home_score,
            'away_sp_k_actual': away_sp_k,
            'home_sp_k_actual': home_sp_k,
            'recorded_at': datetime.now().isoformat(),
        }

        # Calculate accuracy metrics
        pred_away = audit.get('outputs', {}).get('score_projection', {}).get('away_mu', 0)
        pred_home = audit.get('outputs', {}).get('score_projection', {}).get('home_mu', 0)
        audit['accuracy'] = {
            'away_error': away_score - pred_away,
            'home_error': home_score - pred_home,
            'total_error': (away_score + home_score) - (pred_away + pred_home),
            'ml_correct': (pred_away > pred_home) == (away_score > home_score),
        }

        if away_sp_k is not None:
            pred_k = audit.get('outputs', {}).get('k_projections', {}).get('away', {}).get('final_k', 0)
            audit['accuracy']['away_k_error'] = away_sp_k - pred_k
        if home_sp_k is not None:
            pred_k = audit.get('outputs', {}).get('k_projections', {}).get('home', {}).get('final_k', 0)
            audit['accuracy']['home_k_error'] = home_sp_k - pred_k

        with open(filepath, 'w') as f:
            json.dump(audit, f, indent=2, default=str)

        print(f"  ✅ Updated audit: {os.path.basename(filepath)}")


def calc_pnl(bet_str, odds, actual_k):
    """Calculate PNL from bet string, odds, and actual K count."""
    if not bet_str or bet_str == 'TBD':
        return 'N/A', 0.0

    parts = bet_str.strip().split()
    if len(parts) < 2:
        return 'N/A', 0.0

    direction = parts[0]  # Over or Under
    try:
        line = float(parts[1])
    except ValueError:
        return 'N/A', 0.0

    if direction.lower() == 'over':
        won = actual_k > line
    elif direction.lower() == 'under':
        won = actual_k < line
    else:
        return 'N/A', 0.0

    result = 'Win' if won else ('Push' if actual_k == line else 'Loss')

    if result == 'Win':
        try:
            odds_val = float(odds)
            if odds_val >= 100:
                pnl = odds_val / 100.0
            else:
                pnl = 100.0 / abs(odds_val)
        except (ValueError, ZeroDivisionError):
            pnl = 0.0
    elif result == 'Push':
        pnl = 0.0
    else:
        pnl = -1.0

    return result, pnl


def interactive_mode():
    """Interactive CLI for entering results."""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║          MLB OMNI-PROPHET V15.0 | RESULTS ENTRY                ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")

    date_str = input("  Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # ── GAME RESULTS ───────────────────────────────────────────
    pending_games = find_pending_predictions(date_str)
    if pending_games:
        print(f"\n── PENDING GAME PREDICTIONS ({len(pending_games)}) ─────────────────")
        for p in pending_games:
            away = p.get('Away_Team', '?')
            home = p.get('Home_Team', '?')
            pred_a = p.get('Pred_Away_Score', '?')
            pred_h = p.get('Pred_Home_Score', '?')
            print(f"\n  {away} @ {home} (Predicted: {pred_a} — {pred_h})")

            score_input = input(f"    Enter final score ({away} {home}, e.g. '3 5') or 's' to skip: ").strip()
            if score_input.lower() == 's':
                continue
            try:
                parts = score_input.split()
                away_score = int(parts[0])
                home_score = int(parts[1])
                update_predictions_csv(p['row_index'], away_score, home_score)
                update_audit_json(away, home, date_str, away_score, home_score)
                print(f"    ✅ Recorded: {away} {away_score} — {home} {home_score}")
            except (ValueError, IndexError):
                print(f"    ❌ Invalid input. Skipping.")
    else:
        print(f"\n  No pending game predictions for {date_str}")

    # ── K-PROP RESULTS ─────────────────────────────────────────
    pending_ks = find_pending_k_props(date_str)
    if pending_ks:
        print(f"\n── PENDING K-PROP PREDICTIONS ({len(pending_ks)}) ───────────────────")
        for p in pending_ks:
            name = p.get('Name', '?')
            proj = p.get('Projection', '?')
            matchup = p.get('Matchup', '?')
            print(f"\n  {name} ({matchup}) — Projected: {proj}")

            k_input = input(f"    Enter actual K's or 's' to skip: ").strip()
            if k_input.lower() == 's':
                continue
            try:
                actual_k = int(k_input)
                bet = input(f"    Bet placed (e.g. 'Over 4.5') or Enter to skip: ").strip()
                odds = ''
                result = 'N/A'
                pnl = 0.0

                if bet and bet.lower() != 's':
                    odds = input(f"    Odds (e.g. -130): ").strip()
                    result, pnl = calc_pnl(bet, odds, actual_k)
                    print(f"    → {result} ({pnl:+.2f} units)")

                update_k_tracker(p['row_index'], actual_k, bet, odds, result, pnl)

                # Also update audit JSON with K results
                parts = matchup.split('@')
                if len(parts) == 2:
                    away_t, home_t = parts[0].strip(), parts[1].strip()
                    # Determine which SP this is
                    update_audit_json(away_t, home_t, date_str, 0, 0,
                                      away_sp_k=actual_k if p.get('Name') else None)

                print(f"    ✅ Recorded: {name} = {actual_k} K's")
            except ValueError:
                print(f"    ❌ Invalid input. Skipping.")

    elif not pending_games:
        print(f"\n  No pending K-prop predictions for {date_str}")

    print(f"\n{'='*66}")
    print(f"  Results entry complete. Calibration data updated for next simulation.")


if __name__ == '__main__':
    if '--date' in sys.argv:
        idx = sys.argv.index('--date')
        if idx + 1 < len(sys.argv):
            date_filter = sys.argv[idx + 1]
            pending_g = find_pending_predictions(date_filter)
            pending_k = find_pending_k_props(date_filter)
            print(f"Pending for {date_filter}: {len(pending_g)} games, {len(pending_k)} K-props")
            sys.exit(0)
    interactive_mode()
