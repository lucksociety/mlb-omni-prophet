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
MLB QUANT-ELITE V5.0 — GOD-TIER SIMULATION ENGINE
===================================================
Fixes from V4:
  1. Uses CONFIRMED probable starters from Rotowire (not lowest-ERA guess)
  2. Real park factors from FanGraphs (not 100 for every park)
  3. Real weather from live forecasts (not 68F/8mph everywhere)
  4. Better dispersion: k=5.5 (realistic MLB variance, not k=1.2 chaos)
  5. xFIP-anchored Bayesian blending with Stuff+ modifier
  6. Home-field advantage (+3% run boost for home team)
  7. Dome/retractable roof handling (nullify weather in controlled environments)
"""

import csv
import random
import math
from collections import Counter
import datetime

random.seed(42)
N_SIMS = 100000  # Full 100K iterations

# ═══════════════════════════════════════════════════════════════
# 1. CONFIRMED PROBABLE STARTERS (Rotowire, Apr 22 2026)
# ═══════════════════════════════════════════════════════════════
MATCHUPS = [
    # (away_team, home_team, away_sp_name, home_sp_name, away_sp_era, home_sp_era, venue_key)
    ('STL', 'MIA', 'Kyle Leahy',       'Janson Junk',       5.21, 4.50, 'MIA'),
    ('HOU', 'CLE', 'Peter Lambert',    'Tanner Bibee',      7.20, 4.81, 'CLE'),
    ('CIN', 'TBR', 'Brandon Williamson','Nick Martinez',     4.35, 2.45, 'TBR'),
    ('BAL', 'KCR', 'Chris Bassitt',    'Michael Wacha',     6.19, 1.00, 'KCR'),
    ('TOR', 'LAA', 'Eric Lauer',       'José Soriano',      7.13, 0.28, 'LAA'),
    ('ATH', 'SEA', 'Aaron Civale',     'Logan Gilbert',     3.54, 4.03, 'SEA'),
    ('MIL', 'DET', 'Chad Patrick',     'Casey Mize',        0.95, 2.78, 'DET'),
    ('ATL', 'WSN', 'Martin Perez',     'Zack Littell',      2.21, 7.11, 'WSN'),
    ('NYY', 'BOS', 'Max Fried',        'Ranger Suarez',     2.97, 3.22, 'BOS'),
    ('MIN', 'NYM', 'Kendry Rojas',     'Clay Holmes',       0.00, 1.96, 'NYM'),
    ('PHI', 'CHC', 'Taijuan Walker',   'Matthew Boyd',      9.16, 6.75, 'CHC'),
    ('PIT', 'TEX', 'Braxton Ashcraft', 'Jack Leiter',       2.38, 4.87, 'TEX'),
    ('SDP', 'COL', 'Walker Buehler',   'Tomoyuki Sugano',   4.58, 3.92, 'COL'),
    ('CHW', 'ARI', 'Anthony Kay',      'Eduardo Rodriguez', 2.60, 1.96, 'ARI'),
    ('LAD', 'SFG', 'Shohei Ohtani',    'Tyler Mahle',       0.50, 7.23, 'SFG'),
]

# ═══════════════════════════════════════════════════════════════
# 2. REAL PARK FACTORS (FanGraphs 3-year rolling, Runs)
# ═══════════════════════════════════════════════════════════════
PARK_FACTORS = {
    'MIA': 95,   # loanDepot Park (pitcher-friendly, roof)
    'CLE': 97,   # Progressive Field
    'TBR': 93,   # Tropicana Field (dome, pitcher-friendly)
    'KCR': 101,  # Kauffman Stadium
    'LAA': 99,   # Angel Stadium
    'SEA': 94,   # T-Mobile Park (retractable roof, pitcher-friendly)
    'DET': 98,   # Comerica Park
    'WSN': 100,  # Nationals Park
    'BOS': 107,  # Fenway Park (hitter-friendly)
    'NYM': 96,   # Citi Field
    'CHC': 103,  # Wrigley Field (slightly hitter-friendly)
    'TEX': 104,  # Globe Life Field (roof closed)
    'COL': 114,  # Coors Field (extreme hitter-friendly)
    'ARI': 104,  # Chase Field (retractable roof, hitter-friendly)
    'SFG': 93,   # Oracle Park (pitcher-friendly)
}

# ═══════════════════════════════════════════════════════════════
# 3. REAL WEATHER (searched Apr 22 2026)
# ═══════════════════════════════════════════════════════════════
# (temp_F, wind_mph, wind_angle_from_CF, is_dome_or_roof_closed)
WEATHER = {
    'MIA': (75, 0, 90, True),     # Retractable roof closed
    'CLE': (58, 8, 90, False),    # Partly cloudy
    'TBR': (72, 0, 90, True),     # Dome
    'KCR': (75, 11, 90, False),   # Partly cloudy
    'LAA': (72, 6, 90, False),    # Partly cloudy
    'SEA': (56, 5, 90, True),     # Retractable roof likely closed
    'DET': (72, 8, 90, False),    # Mostly sunny
    'WSN': (62, 7, 90, False),    # Overcast
    'BOS': (48, 10, 135, False),  # Cold, light rain
    'NYM': (55, 8, 90, False),    # Cool, light rain
    'CHC': (56, 12, 45, False),   # Wrigley wind blowing in
    'TEX': (74, 0, 90, True),     # Globe Life roof closed
    'COL': (80, 21, 90, False),   # Hot, high winds
    'ARI': (87, 5, 90, True),     # Roof likely closed
    'SFG': (59, 12, 180, False),  # Cool, wind blowing out to CF
}

# ═══════════════════════════════════════════════════════════════
# 4. CORE SABERMETRIC ENGINE
# ═══════════════════════════════════════════════════════════════

def bayesian_era(sp_xfip, sp_era_2026, ip_2026, league_avg=4.15):
    """
    Bayesian true-talent estimator.
    Anchor to xFIP (peripherals-based), then blend in 2026 ERA
    weighted by innings pitched. For pitchers with very low IP,
    we heavily regress toward xFIP.
    """
    if ip_2026 <= 0 or sp_era_2026 <= 0:
        # Debut or no 2026 data: use xFIP with regression to league avg
        return sp_xfip * 0.7 + league_avg * 0.3

    # Weight of 2026 data scales with IP (maxes at 35%)
    w_2026 = min(0.35, ip_2026 / 60.0)
    w_xfip = 1.0 - w_2026

    blended = (w_xfip * sp_xfip) + (w_2026 * sp_era_2026)

    # Cap extreme outliers
    return max(1.50, min(blended, 8.00))


def stuff_plus_modifier(stuff_plus):
    """
    Stuff+ adjusts the pitcher's expected run rate.
    100 = average. >100 = better stuff = fewer runs.
    Each point above/below 100 modifies ERA by ~0.5%.
    """
    if stuff_plus is None or stuff_plus == 'N/A':
        return 1.0
    try:
        s = float(stuff_plus)
        return 1.0 - ((s - 100) * 0.005)
    except (ValueError, TypeError):
        return 1.0


def model_full_game_era(starter_era, bullpen_xfip, starter_ip=5.5):
    """Blend starter and bullpen for full 9 innings."""
    bp_ip = max(0, 9.0 - starter_ip)
    return ((starter_era * starter_ip) + (bullpen_xfip * bp_ip)) / 9.0


def park_factor_mult(pf):
    return pf / 100.0


def wind_adjustment(wind_speed, wind_angle, is_dome):
    if is_dome:
        return 1.0
    effective = wind_speed * math.cos(math.radians(wind_angle))
    return 1.0 + (effective * 0.004)


def temp_adjustment(temp_f, is_dome):
    if is_dome:
        return 1.0
    return 1.0 + ((temp_f - 72) * 0.0008)


HOME_FIELD_ADV = 1.03  # Home teams score ~3% more runs historically


def poisson_rvs(lam):
    if lam > 500:
        return max(0, int(random.gauss(lam, math.sqrt(lam))))
    L = math.exp(-lam)
    k, p_val = 0, 1.0
    while p_val > L:
        k += 1
        p_val *= random.random()
    return k - 1


def nbinom_rvs(n, p):
    scale = (1.0 - p) / p
    lam = random.gammavariate(n, scale)
    return poisson_rvs(lam)


def run_simulation(away_mu, home_mu, k=5.5, n_sims=N_SIMS):
    """
    Negative binomial simulation.
    k = dispersion parameter. Higher k = less variance.
    k=5.5 gives realistic MLB-like run distributions (std ~2.8-3.5 for a team).
    """
    away_p = k / (k + away_mu)
    home_p = k / (k + home_mu)
    away_runs = [nbinom_rvs(k, away_p) for _ in range(n_sims)]
    home_runs = [nbinom_rvs(k, home_p) for _ in range(n_sims)]
    return away_runs, home_runs


# ═══════════════════════════════════════════════════════════════
# 5. CSV PARSER
# ═══════════════════════════════════════════════════════════════

def parse_multi_csv(filepath):
    sections = {}
    current_section = None
    headers = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not any(row):
                continue
            first_val = row[0].strip()
            if first_val in ["Batting Advanced", "Batting Stat Cast",
                             "Pitching Advanced", "Pitching +", "Pitching Statcast"]:
                current_section = first_val
                sections[current_section] = []
                headers = []
                continue
            if current_section:
                if first_val == '#' and not headers:
                    # Extract just the stat abbreviation (first word)
                    # e.g. "wRC+ wRC+ - Runs per PA..." → "wRC+"
                    headers = []
                    for h in row:
                        h = h.strip()
                        if ' ' in h:
                            headers.append(h.split()[0])
                        else:
                            headers.append(h)
                    continue
                if headers and first_val != '#':
                    if len(row) >= len(headers):
                        row_dict = dict(zip(headers, row[:len(headers)]))
                        sections[current_section].append(row_dict)
    return sections


def fuzzy_match(name, candidates):
    """Match a pitcher name to CSV data, handling accents and abbreviations."""
    name_lower = name.lower().strip()
    last_name = name_lower.split()[-1] if name_lower else ''

    for c in candidates:
        c_name = c.get('Name', '').lower().strip()
        if name_lower == c_name:
            return c
        if last_name and last_name in c_name:
            return c
    return None


def get_sp_data(sections, sp_name, team):
    """Find a starter's advanced stats from the CSV."""
    pitchers = sections.get('Pitching Advanced', [])

    # First try: exact team + name match
    team_pitchers = [p for p in pitchers if p.get('Team', '') == team]
    match = fuzzy_match(sp_name, team_pitchers)
    if match:
        return match

    # Second try: all pitchers (pitcher may have changed teams)
    match = fuzzy_match(sp_name, pitchers)
    if match:
        return match

    return None


def get_stuff_plus(sections, sp_name):
    pitchers = sections.get('Pitching +', [])
    match = fuzzy_match(sp_name, pitchers)
    if match:
        return match.get('Stuff+', None)
    return None


def get_team_wrc(sections, team):
    batters = [b for b in sections.get('Batting Advanced', []) if b.get('Team') == team]
    batters.sort(key=lambda x: int(x.get('PA', '0') or '0'), reverse=True)
    top_9 = batters[:9]
    if not top_9:
        return 100.0
    wrcs = []
    for b in top_9:
        try:
            wrcs.append(float(b.get('wRC+', '100')))
        except (ValueError, TypeError):
            wrcs.append(100.0)
    return sum(wrcs) / len(wrcs)


def get_bp_xfip(sections, team, sp_name):
    """Bullpen xFIP: average xFIP of all pitchers on the team except the starter."""
    pitchers = [p for p in sections.get('Pitching Advanced', [])
                if p.get('Team') == team and p.get('Name', '') != sp_name]
    if not pitchers:
        return 4.15
    xfips = []
    for p in pitchers:
        try:
            xfips.append(float(p.get('xFIP', '4.15')))
        except (ValueError, TypeError):
            pass
    return sum(xfips) / len(xfips) if xfips else 4.15


# ═══════════════════════════════════════════════════════════════
# 6. ANALYSIS & REPORTING
# ═══════════════════════════════════════════════════════════════

def calc_mean(arr): return sum(arr) / len(arr)
def calc_std(arr):
    m = calc_mean(arr)
    return math.sqrt(sum((x - m) ** 2 for x in arr) / len(arr))
def calc_pctl(arr, p):
    s = sorted(arr)
    return s[min(int(len(s) * p / 100), len(s) - 1)]


def analyze_and_print(away_runs, home_runs, away_mu, home_mu, meta):
    away = meta['away_team']
    home = meta['home_team']
    n = len(away_runs)
    total_runs = [away_runs[i] + home_runs[i] for i in range(n)]

    scores = Counter(zip(away_runs, home_runs))
    mode, mode_ct = scores.most_common(1)[0]

    away_w = sum(1 for i in range(n) if away_runs[i] > home_runs[i])
    home_w = sum(1 for i in range(n) if home_runs[i] > away_runs[i])
    ties = n - away_w - home_w
    away_pct = (away_w + ties * 0.48) / n * 100
    home_pct = (home_w + ties * 0.52) / n * 100

    rl_away = sum(1 for i in range(n) if away_runs[i] - home_runs[i] > 1.5) / n * 100
    rl_home = sum(1 for i in range(n) if home_runs[i] - away_runs[i] > 1.5) / n * 100

    total_mean = calc_mean(total_runs)
    total_std = calc_std(total_runs)
    p25, p75 = calc_pctl(total_runs, 25), calc_pctl(total_runs, 75)

    print("╔══════════════════════════════════════════════════════════════╗")
    print(f"║  MLB QUANT-ELITE V5.0 | 100K MONTE CARLO | {away} @ {home}  ║")
    print(f"║  {datetime.datetime.now().strftime('%Y-%m-%d')} | CONFIRMED LINEUPS + REAL WEATHER       ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    print(f"\n  AWAY SP: {meta['away_sp']}  |  Blended ERA: {meta['away_blended']:.2f}")
    print(f"       xFIP: {meta.get('away_xfip','N/A')}  |  Stuff+: {meta.get('away_stuff','N/A')}")
    print(f"  HOME SP: {meta['home_sp']}  |  Blended ERA: {meta['home_blended']:.2f}")
    print(f"       xFIP: {meta.get('home_xfip','N/A')}  |  Stuff+: {meta.get('home_stuff','N/A')}")

    w = WEATHER[meta['venue']]
    dome_str = "DOME/ROOF CLOSED" if w[3] else f"{w[0]}°F | Wind {w[1]}mph"
    print(f"\n  Park Factor: {PARK_FACTORS[meta['venue']]}  |  Weather: {dome_str}")
    print(f"  Lineup wRC+: {away} {meta['away_wrc']:.1f} | {home} {meta['home_wrc']:.1f}")
    print(f"  Bullpen xFIP: {away} {meta['away_bp']:.2f} | {home} {meta['home_bp']:.2f}")

    print(f"\n── PROJECTED SCORE ─────────────────────────────────────────────")
    print(f"  ⚾ {away}: {away_mu:.3f}  |  {home}: {home_mu:.3f}  |  Total: {away_mu+home_mu:.3f}")
    print(f"  MODE: {mode[0]}-{mode[1]} ({mode_ct/n*100:.1f}% of sims)")
    for s, c in scores.most_common(5)[1:]:
        print(f"        {s[0]}-{s[1]} ({c/n*100:.1f}%)")

    print(f"\n── WIN PROBABILITY ─────────────────────────────────────────────")
    fav = away if away_pct > home_pct else home
    fav_pct = max(away_pct, home_pct)
    print(f"  {away}: {away_pct:.1f}%  |  {home}: {home_pct:.1f}%  →  EDGE: {fav} ({fav_pct:.1f}%)")
    print(f"  Run Line: {away} -1.5 → {rl_away:.1f}%  |  {home} -1.5 → {rl_home:.1f}%")

    print(f"\n── O/U TABLE ───────────────────────────────────────────────────")
    for line in [6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]:
        over = sum(1 for t in total_runs if t > line) / n * 100
        if 20 < over < 80:
            print(f"  O/U {line:5.1f}:  Over {over:5.1f}%  |  Under {100-over:5.1f}%")

    print(f"\n── VOLATILITY ──────────────────────────────────────────────────")
    chaos = 'HIGH' if total_std > 3.8 else 'MODERATE' if total_std > 3.0 else 'LOW'
    print(f"  Std Dev: {total_std:.2f} [{chaos}]  |  IQR: {p25}-{p75} total runs")
    print("")
    print("=" * 64)
    print("")


# ═══════════════════════════════════════════════════════════════
# 7. MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════

def main():
    sections = parse_multi_csv('MLB Stats')

    print("=" * 64)
    print("  MLB QUANT-ELITE V5.0 — FULL SLATE — APRIL 22, 2026")
    print("  100,000 ITERATIONS PER GAME | CONFIRMED STARTERS + WEATHER")
    print("=" * 64)
    print("")

    summary = []

    for (away, home, away_sp_name, home_sp_name,
         away_sp_era_26, home_sp_era_26, venue) in MATCHUPS:

        # Get pitcher stats from CSV
        away_sp_data = get_sp_data(sections, away_sp_name, away)
        home_sp_data = get_sp_data(sections, home_sp_name, home)

        # xFIP (true-talent anchor)
        away_xfip = float(away_sp_data.get('xFIP', '4.15')) if away_sp_data else 4.15
        home_xfip = float(home_sp_data.get('xFIP', '4.15')) if home_sp_data else 4.15

        # IP for Bayesian weighting
        away_ip = float(away_sp_data.get('IP', '15')) if away_sp_data else 15.0
        home_ip = float(home_sp_data.get('IP', '15')) if home_sp_data else 15.0

        # Bayesian blend
        away_blended = bayesian_era(away_xfip, away_sp_era_26, away_ip)
        home_blended = bayesian_era(home_xfip, home_sp_era_26, home_ip)

        # Stuff+ modifier
        away_stuff = get_stuff_plus(sections, away_sp_name)
        home_stuff = get_stuff_plus(sections, home_sp_name)

        # Lineup wRC+
        away_wrc = get_team_wrc(sections, away)
        home_wrc = get_team_wrc(sections, home)

        # Bullpen xFIP
        away_bp = get_bp_xfip(sections, away, away_sp_name)
        home_bp = get_bp_xfip(sections, home, home_sp_name)

        # Projected starter IP (better pitchers go deeper)
        away_proj_ip = 5.5 if away_blended < 4.0 else 5.0
        home_proj_ip = 5.5 if home_blended < 4.0 else 5.0

        # Full-game ERA
        away_scoring_era = model_full_game_era(home_blended, home_bp, home_proj_ip)
        home_scoring_era = model_full_game_era(away_blended, away_bp, away_proj_ip)

        # Environmental multipliers
        pf = park_factor_mult(PARK_FACTORS[venue])
        temp, wind_spd, wind_ang, is_dome = WEATHER[venue]
        w_adj = wind_adjustment(wind_spd, wind_ang, is_dome)
        t_adj = temp_adjustment(temp, is_dome)
        env = pf * w_adj * t_adj

        # Expected runs
        away_mu = away_scoring_era * (away_wrc / 100.0) * stuff_plus_modifier(home_stuff) * env
        home_mu = home_scoring_era * (home_wrc / 100.0) * stuff_plus_modifier(away_stuff) * env * HOME_FIELD_ADV

        # Clamp
        away_mu = max(2.0, min(away_mu, 10.0))
        home_mu = max(2.0, min(home_mu, 10.0))

        # Simulate
        away_runs, home_runs = run_simulation(away_mu, home_mu)

        meta = {
            'away_team': away, 'home_team': home,
            'away_sp': away_sp_name, 'home_sp': home_sp_name,
            'away_blended': away_blended, 'home_blended': home_blended,
            'away_xfip': away_xfip, 'home_xfip': home_xfip,
            'away_stuff': away_stuff, 'home_stuff': home_stuff,
            'away_wrc': away_wrc, 'home_wrc': home_wrc,
            'away_bp': away_bp, 'home_bp': home_bp,
            'venue': venue,
        }

        analyze_and_print(away_runs, home_runs, away_mu, home_mu, meta)

        n = len(away_runs)
        away_w = sum(1 for i in range(n) if away_runs[i] > home_runs[i])
        home_w = sum(1 for i in range(n) if home_runs[i] > away_runs[i])
        ties = n - away_w - home_w
        away_pct = (away_w + ties * 0.48) / n * 100
        home_pct = 100 - away_pct

        summary.append((away, home, away_mu, home_mu, away_pct, home_pct))

    # Print summary table
    print("\n" + "=" * 64)
    print("  FINAL SCORE PREDICTIONS — QUANT-ELITE V5.0")
    print("=" * 64)
    print(f"  {'MATCHUP':<20} {'AWAY':>6} {'HOME':>6} {'TOTAL':>6} {'FAVORED':>10}")
    print("  " + "-" * 50)
    for away, home, a_mu, h_mu, a_pct, h_pct in summary:
        total = a_mu + h_mu
        fav = f"{away} {a_pct:.0f}%" if a_pct > h_pct else f"{home} {h_pct:.0f}%"
        print(f"  {away+'@'+home:<20} {a_mu:>6.2f} {h_mu:>6.2f} {total:>6.2f} {fav:>10}")
    print("=" * 64)


if __name__ == '__main__':
    main()