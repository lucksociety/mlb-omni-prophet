#!/usr/bin/env python3
"""
MLB RECORD GAME — Non-Interactive Results Recorder
Called programmatically by agents to record game results without interactive prompts.

Usage:
  py record_game.py --away NYY --home MIL --away_score 3 --home_score 4 --away_sp_k 10 --home_sp_k 5
  py record_game.py --away NYY --home MIL --away_score 3 --home_score 4 --date 2026-05-10

Optional: --box_score "raw box score text" to also process player-level game logs.
"""
import argparse
import csv
import json
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import glob
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREDICTIONS_CSV = os.path.join(BASE_DIR, 'data', 'predictions_history.csv')
K_TRACKER_CSV = os.path.join(BASE_DIR, 'models', 'K Prophet', 'performance_tracker.csv')
AUDITS_DIR = os.path.join(BASE_DIR, 'output', 'audits')
MLB_STATS_FILE = os.path.join(BASE_DIR, 'data', 'MLB Stats')


def find_and_update_prediction(date_str, away, home, away_score, home_score):
    """Find matching prediction row and fill in results."""
    if not os.path.exists(PREDICTIONS_CSV):
        print(f"  [ERROR] {PREDICTIONS_CSV} not found.")
        return False

    rows = []
    headers = None
    updated = False

    with open(PREDICTIONS_CSV, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
            rows.append(row)

    if not headers:
        print("  [ERROR] Empty predictions file.")
        return False

    h = {name: idx for idx, name in enumerate(headers)}
    winner = away if away_score > home_score else home
    total = away_score + home_score

    for i, row in enumerate(rows):
        if i == 0:
            continue
        if (row[h.get('Date', 0)] == date_str and
            row[h.get('Away_Team', 1)] == away and
            row[h.get('Home_Team', 2)] == home and
            not row[h.get('Result_Away_Score', -1)]):

            for col_name, val in [
                ('Result_Away_Score', str(away_score)),
                ('Result_Home_Score', str(home_score)),
                ('Result_Winner', winner),
                ('Result_Total', str(total)),
            ]:
                if col_name in h:
                    rows[i][h[col_name]] = val
            updated = True
            print(f"  [OK] predictions_history.csv: {away} {away_score} - {home} {home_score}")
            break

    if not updated:
        print(f"  [WARN] No pending prediction found for {away}@{home} on {date_str}")
        return False

    with open(PREDICTIONS_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return True


def find_and_update_k_tracker(date_str, pitcher_name, actual_k):
    """Find matching K-prop row and fill in actual."""
    if not os.path.exists(K_TRACKER_CSV):
        print(f"  [WARN] K tracker not found at {K_TRACKER_CSV}")
        return False

    rows = []
    headers = None
    updated = False

    with open(K_TRACKER_CSV, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
            rows.append(row)

    if not headers:
        return False

    h = {name: idx for idx, name in enumerate(headers)}
    pitcher_lower = pitcher_name.lower()

    for i, row in enumerate(rows):
        if i == 0:
            continue
        name_col = row[h.get('Name', 3)] if 'Name' in h else ''
        actual_col = row[h.get('Actual', 11)] if 'Actual' in h else ''
        date_col = row[h.get('Date', 0)] if 'Date' in h else ''

        if (date_col == date_str and
            pitcher_lower in name_col.lower() and
            actual_col in ('TBD', '', 'None')):

            if 'Actual' in h:
                rows[i][h['Actual']] = str(actual_k)

            # Calculate result if bet was placed
            bet = row[h.get('Bet', -1)] if 'Bet' in h else ''
            if bet and bet not in ('TBD', ''):
                odds = row[h.get('Odds', -1)] if 'Odds' in h else ''
                result, pnl = _calc_pnl(bet, odds, actual_k)
                if 'Result' in h:
                    rows[i][h['Result']] = result
                if 'PNL' in h:
                    rows[i][h['PNL']] = str(pnl)
                print(f"  [OK] K tracker: {pitcher_name} = {actual_k} K's ({result}, {pnl:+.2f}u)")
            else:
                print(f"  [OK] K tracker: {pitcher_name} = {actual_k} K's")
            updated = True
            break

    if updated:
        with open(K_TRACKER_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    else:
        print(f"  [WARN] No pending K-prop found for {pitcher_name} on {date_str}")

    return updated


def update_audit_json(away, home, date_str, away_score, home_score,
                      away_sp_k=None, home_sp_k=None):
    """Update audit JSON with results."""
    pattern = os.path.join(AUDITS_DIR, f"audit_{away}_{home}_{date_str}*.json")
    files = glob.glob(pattern)
    if not files:
        print(f"  [WARN] No audit file found matching {pattern}")
        return

    for filepath in files:
        try:
            with open(filepath, 'r') as f:
                audit = json.load(f)

            if 'results' not in audit:
                audit['results'] = {}

            audit['results']['away_score'] = away_score
            audit['results']['home_score'] = home_score
            audit['results']['total'] = away_score + home_score
            audit['results']['winner'] = away if away_score > home_score else home
            audit['results']['status'] = 'COMPLETE'
            audit['results']['recorded_at'] = datetime.now().isoformat()

            if away_sp_k is not None:
                audit['results']['away_sp_k_actual'] = away_sp_k
            if home_sp_k is not None:
                audit['results']['home_sp_k_actual'] = home_sp_k

            with open(filepath, 'w') as f:
                json.dump(audit, f, indent=2, default=str)

            print(f"  [OK] audit: {os.path.basename(filepath)}")
        except Exception as e:
            print(f"  [ERROR] Failed to update {filepath}: {e}")


def append_box_score_to_stats(box_score_text, date_str):
    """Parse raw box score text and append to MLB Stats."""
    import re
    lines = box_score_text.splitlines()
    batting_records = []
    pitching_records = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            parts = next_line.split('\t')
            if len(parts) >= 8 and parts[0].replace('.', '', 1).isdigit():
                name = line
                name = re.sub(r'\(.*?\)', '', name).strip()
                name = re.sub(r'1-Ran.*', '', name).strip()
                name = re.sub(r'a-.*', '', name).strip()
                if len(parts) == 8:
                    if '.' in parts[6] or '.' in parts[7]:
                        if '.' in parts[0]:
                            pitching_records.append([name] + parts)
                        elif len(parts[6]) > 0 and parts[6][0] == '.' and len(parts[7]) > 0 and (parts[7][0] == '.' or '.' in parts[7]):
                            batting_records.append([name] + parts)
                        else:
                            pitching_records.append([name] + parts)
                i += 1
        i += 1

    if batting_records or pitching_records:
        with open(MLB_STATS_FILE, 'a', encoding='utf-8') as f:
            if batting_records:
                f.write(f'\nBatting Game Logs ({date_str})\n')
                f.write('Name,AB,R,H,RBI,BB,SO,AVG,OPS\n')
                for rec in batting_records:
                    f.write(','.join(rec) + '\n')
            if pitching_records:
                f.write(f'\nPitching Game Logs ({date_str})\n')
                f.write('Name,IP,H,R,ER,BB,SO,HR,ERA\n')
                for rec in pitching_records:
                    f.write(','.join(rec) + '\n')
        print(f"  [OK] MLB Stats: {len(batting_records)} batting + {len(pitching_records)} pitching logs appended for {date_str}")
    else:
        print(f"  [WARN] No parseable stat lines found in box score text.")


def _calc_pnl(bet_str, odds_str, actual_k):
    """Calculate PNL from bet string."""
    if not bet_str or bet_str in ('TBD', ''):
        return 'N/A', 0.0
    parts = bet_str.strip().split()
    if len(parts) < 2:
        return 'N/A', 0.0
    direction = parts[0].lower()
    try:
        line = float(parts[1])
    except ValueError:
        return 'N/A', 0.0

    if direction == 'over':
        won = actual_k > line
    elif direction == 'under':
        won = actual_k < line
    else:
        return 'N/A', 0.0

    result = 'Win' if won else ('Push' if actual_k == line else 'Loss')
    if result == 'Win':
        try:
            odds_val = float(odds_str)
            pnl = odds_val / 100.0 if odds_val >= 100 else 100.0 / abs(odds_val)
        except:
            pnl = 0.0
    elif result == 'Push':
        pnl = 0.0
    else:
        pnl = -1.0
    return result, pnl


def main():
    parser = argparse.ArgumentParser(description='Record MLB game results (non-interactive)')
    parser.add_argument('--away', required=True, help='Away team abbreviation')
    parser.add_argument('--home', required=True, help='Home team abbreviation')
    parser.add_argument('--away_score', required=True, type=int, help='Away team final score')
    parser.add_argument('--home_score', required=True, type=int, help='Home team final score')
    parser.add_argument('--away_sp_k', type=int, default=None, help='Away SP strikeout total')
    parser.add_argument('--home_sp_k', type=int, default=None, help='Home SP strikeout total')
    parser.add_argument('--away_sp', default=None, help='Away SP name (for K tracker lookup)')
    parser.add_argument('--home_sp', default=None, help='Home SP name (for K tracker lookup)')
    parser.add_argument('--date', default=None, help='Game date (YYYY-MM-DD), default today')
    parser.add_argument('--box_score', default=None, help='Raw box score text (or path to file)')
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime('%Y-%m-%d')
    print(f"\n=== RECORD GAME: {args.away} {args.away_score} - {args.home} {args.home_score} ({date_str}) ===\n")

    # 1. Update predictions_history.csv
    find_and_update_prediction(date_str, args.away, args.home, args.away_score, args.home_score)

    # 2. Update K tracker
    if args.away_sp and args.away_sp_k is not None:
        find_and_update_k_tracker(date_str, args.away_sp, args.away_sp_k)
    if args.home_sp and args.home_sp_k is not None:
        find_and_update_k_tracker(date_str, args.home_sp, args.home_sp_k)

    # 3. Update audit JSON
    update_audit_json(args.away, args.home, date_str,
                      args.away_score, args.home_score,
                      args.away_sp_k, args.home_sp_k)

    # 4. Process box score if provided
    if args.box_score:
        if os.path.isfile(args.box_score):
            with open(args.box_score, 'r', encoding='utf-8') as f:
                box_text = f.read()
        else:
            box_text = args.box_score
        append_box_score_to_stats(box_text, date_str)

    print(f"\n=== RECORDING COMPLETE ===")


if __name__ == '__main__':
    main()