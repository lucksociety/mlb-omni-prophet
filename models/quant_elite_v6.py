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
MLB QUANT-ELITE V6.0 — DETERMINISTIC STATE ENGINE
Focus: Dynamic IP, Situational Bullpens, Platoon Splits, and Cascade Failures
"""
import csv, random, math
from collections import Counter
import datetime

random.seed(2026_04_23)
N_SIMS = 100000

# ── 1. CORE DATA PARSING & PLATOON LOGIC ────────────────────────

def parse_csv(filepath):
    sections = {}
    current_section = None
    headers = []
    try:
        with open(filepath, 'r') as f:
            for row in csv.reader(f):
                if not row or not any(row): continue
                fv = row[0].strip()
                if fv in ["Batting Advanced", "Batting Stat Cast", "Pitching Advanced", 
                          "Pitching +", "Pitching Statcast", "Batting Splits LHP", "Batting Splits RHP"]:
                    current_section = fv; sections[fv] = []; headers = []; continue
                if current_section:
                    if fv == '#' and not headers:
                        headers = [h.split()[0] if h.strip() else f'c{i}' for i,h in enumerate(row)]
                        continue
                    if headers and fv != '#' and len(row) >= len(headers):
                        sections[current_section].append(dict(zip(headers, row[:len(headers)])))
    except FileNotFoundError:
        print(f"⚠ ERROR: Could not find '{filepath}'. Ensure the FanGraphs export is in the same directory.")
        return {}
    return sections

def fuzzy_find(name, players):
    if not players: return None
    name_l = name.lower()
    last = name_l.split()[-1]
    for p in players:
        pn = p.get('Name','').lower()
        if last in pn: return p
    return None

def get_lineup_wrc(lineup_names, team, sections, opposing_sp_hand=None):
    """
    Get wRC+ considering Platoon Splits if available.
    opposing_sp_hand should be 'L' or 'R'.
    """
    # Check if we have split data
    if opposing_sp_hand == 'L' and 'Batting Splits LHP' in sections:
        batters = sections['Batting Splits LHP']
    elif opposing_sp_hand == 'R' and 'Batting Splits RHP' in sections:
        batters = sections['Batting Splits RHP']
    else:
        batters = sections.get('Batting Advanced', [])
        
    team_batters = [b for b in batters if b.get('Team') == team]
    all_batters = batters
    
    wrcs = []
    for name, hand in lineup_names:
        match = fuzzy_find(name, team_batters) or fuzzy_find(name, all_batters)
        if match:
            try:
                wrcs.append(float(match.get('wRC+', '100')))
            except: wrcs.append(95.0)
        else:
            wrcs.append(85.0) # Penalty for unknowns
    
    return sum(wrcs) / len(wrcs) if wrcs else 100.0

def get_pitcher_stats(name, team, sections):
    pitchers = sections.get('Pitching Advanced', [])
    team_p = [p for p in pitchers if p.get('Team') == team]
    p = fuzzy_find(name, team_p) or fuzzy_find(name, pitchers)
    
    stuff_data = sections.get('Pitching +', [])
    stuff_p = fuzzy_find(name, stuff_data)
    
    stats = {
        'xFIP': 4.15, 'IP': 15.0, 'K/9': 8.5, 'K%': 0.22, 'Stuff+': 100.0
    }
    if p:
        try: stats['xFIP'] = float(p.get('xFIP', 4.15))
        except: pass
        try: stats['IP'] = float(p.get('IP', 15.0))
        except: pass
        try: stats['K/9'] = float(p.get('K/9', 8.5))
        except: pass
        try: 
            k_pct_str = p.get('K%', '22.0%').strip('%')
            stats['K%'] = float(k_pct_str) / 100.0
        except: pass
        
    if stuff_p:
        try: stats['Stuff+'] = float(stuff_p.get('Stuff+', 100.0))
        except: pass
        
    return stats

# ── 2. DYNAMIC PITCHING & BULLPEN STATE ─────────────────────────

def get_bullpen_tiers(team, sp_name, sections):
    """
    Splits the bullpen into A-Team (High Lev), B-Team (Low Lev/Mop-Up), and Average.
    """
    pitchers = [p for p in sections.get('Pitching Advanced', [])
                if p.get('Team') == team and p.get('Name','') != sp_name]
    
    xfips = []
    for p in pitchers:
        try: xfips.append(float(p.get('xFIP', 4.15)))
        except: pass
        
    if not xfips:
        return {'A': 3.50, 'B': 5.00, 'C': 7.50, 'AVG': 4.15}
        
    xfips.sort()
    
    # Top 2 relievers are A-Team
    a_team = xfips[:2] if len(xfips) >= 2 else xfips
    # Bottom 3 relievers are B-Team
    b_team = xfips[-3:] if len(xfips) >= 3 else xfips
    # Absolute worst reliever for Emergency/Position Player Tier C
    c_team = xfips[-1:] if len(xfips) >= 1 else xfips
    
    return {
        'A': sum(a_team)/len(a_team),
        'B': sum(b_team)/len(b_team),
        'C': (sum(c_team)/len(c_team)) * 1.5,
        'AVG': sum(xfips)/len(xfips)
    }

def bayesian_era(xfip, era_26, ip):
    if ip <= 0 or era_26 <= 0: return xfip * 0.7 + 4.15 * 0.3
    w26 = min(0.35, ip / 60.0)
    return max(1.50, min((1-w26)*xfip + w26*era_26, 8.00))

def calc_expected_ip(blended_era, opp_wrc, base_ip=5.5):
    """Dynamic Expected IP based on pitcher quality and opponent strength."""
    era_penalty = (blended_era - 4.0) * 0.4
    wrc_penalty = (opp_wrc - 100.0) * 0.015
    ip = base_ip - era_penalty - wrc_penalty
    return max(3.0, min(ip, 7.0)) # Bounded

# ── 3. MATH DISTRIBUTION GENERATORS ─────────────────────────────

def poisson_rvs(lam):
    if lam <= 0: return 0
    if lam > 500: return max(0, int(random.gauss(lam, math.sqrt(lam))))
    L = math.exp(-lam); k=0; p=1.0
    while p > L: k+=1; p*=random.random()
    return k-1

def nbinom_rvs(n, p):
    if p >= 1.0 or p <= 0: return 0
    return poisson_rvs(random.gammavariate(n, (1.0-p)/p))

# ── 4. STATE ENGINE SIMULATOR ───────────────────────────────────

def simulate_game_v6(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                     away_wrc, home_wrc, env_factor, runs_to_blowout=4):
    """
    Executes a 2-stage Monte Carlo state engine modeling blowouts and K-prop attrition.
    """
    
    # 1. Base expected runs for Starters
    # Mu = ERA / 9 * IP * wRC * Env * Stuff
    away_sp_stuff_mod = 1.0 - ((away_sp_stats['Stuff+'] - 100) * 0.005)
    home_sp_stuff_mod = 1.0 - ((home_sp_stats['Stuff+'] - 100) * 0.005)
    
    # Home Team Batting (Away SP)
    away_sp_mu = (away_sp_stats['Blended'] / 9.0) * away_sp_stats['Exp_IP'] * (home_wrc/100.0) * away_sp_stuff_mod * env_factor
    # Away Team Batting (Home SP)
    home_sp_mu = (home_sp_stats['Blended'] / 9.0) * home_sp_stats['Exp_IP'] * (away_wrc/100.0) * home_sp_stuff_mod * env_factor

    away_total_runs = []
    home_total_runs = []
    away_sp_k_dist = []
    home_sp_k_dist = []
    
    # Dynamic Variance Injection
    chaos_multiplier = 1.0
    if env_factor > 1.08:
        chaos_multiplier = 0.6
    elif env_factor < 0.95:
        chaos_multiplier = 1.3
        
    sp_k = 4.5 * chaos_multiplier
    
    ap_ap = sp_k / (sp_k + home_sp_mu) if home_sp_mu > 0 else 0.99
    hp_ap = sp_k / (sp_k + away_sp_mu) if away_sp_mu > 0 else 0.99

    for _ in range(N_SIMS):
        # -- SIMULATE HOME SP (AWAY BATTING) --
        h_sp_runs = nbinom_rvs(sp_k, ap_ap)
        actual_h_ip = home_sp_stats['Exp_IP']
        
        # Cascade Failure Check (Blowout)
        if h_sp_runs >= runs_to_blowout:
            actual_h_ip = max(1.0, home_sp_stats['Exp_IP'] - 2.5) # Hooked early
            bp_innings = 9.0 - actual_h_ip
            
            if actual_h_ip < 3.0:
                h_bp_mu = (home_bp['C'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor
            else:
                h_bp_mu = (home_bp['B'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor
        else:
            bp_innings = 9.0 - actual_h_ip
            # High Leverage Bullpen enters
            h_bp_mu = (home_bp['A'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor
            
        a_runs = h_sp_runs + poisson_rvs(h_bp_mu)
        
        # K-Prop generation based on *actual* IP
        h_sp_k_mu = (home_sp_stats['K/9'] / 9.0) * actual_h_ip
        home_sp_k_dist.append(poisson_rvs(h_sp_k_mu))
        
        # -- SIMULATE AWAY SP (HOME BATTING) --
        a_sp_runs = nbinom_rvs(sp_k, hp_ap)
        actual_a_ip = away_sp_stats['Exp_IP']
        
        if a_sp_runs >= runs_to_blowout:
            actual_a_ip = max(1.0, away_sp_stats['Exp_IP'] - 2.5)
            bp_innings = 9.0 - actual_a_ip
            
            if actual_a_ip < 3.0:
                a_bp_mu = (away_bp['C'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor
            else:
                a_bp_mu = (away_bp['B'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor
        else:
            bp_innings = 9.0 - actual_a_ip
            a_bp_mu = (away_bp['A'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor
            
        h_runs = a_sp_runs + poisson_rvs(a_bp_mu * 1.03) # 3% HFA for home team
        
        # K-Prop generation
        a_sp_k_mu = (away_sp_stats['K/9'] / 9.0) * actual_a_ip
        away_sp_k_dist.append(poisson_rvs(a_sp_k_mu))
        
        away_total_runs.append(a_runs)
        home_total_runs.append(h_runs)
        
    return away_total_runs, home_total_runs, away_sp_k_dist, home_sp_k_dist

# ── EXPORTED PROTOCOL ─────────────────────────────────────────
def run_v6_protocol(away_team, home_team, away_sp_name, home_sp_name,
                    away_sp_hand, home_sp_hand, away_era, home_era,
                    away_lineup, home_lineup, park_factor, is_dome, temp_f, wind_mph, wind_ang=90):
    
    sections = parse_csv('MLB Stats')
    
    away_sp_stats = get_pitcher_stats(away_sp_name, away_team, sections)
    home_sp_stats = get_pitcher_stats(home_sp_name, home_team, sections)
    
    away_sp_stats['Blended'] = bayesian_era(away_sp_stats['xFIP'], away_era, away_sp_stats['IP'])
    home_sp_stats['Blended'] = bayesian_era(home_sp_stats['xFIP'], home_era, home_sp_stats['IP'])
    
    # Platoon Logic
    away_wrc = get_lineup_wrc(away_lineup, away_team, sections, home_sp_hand)
    home_wrc = get_lineup_wrc(home_lineup, home_team, sections, away_sp_hand)
    
    # Dynamic IP
    away_sp_stats['Exp_IP'] = calc_expected_ip(away_sp_stats['Blended'], home_wrc)
    home_sp_stats['Exp_IP'] = calc_expected_ip(home_sp_stats['Blended'], away_wrc)
    
    # Situational Bullpens
    away_bp = get_bullpen_tiers(away_team, away_sp_name, sections)
    home_bp = get_bullpen_tiers(home_team, home_sp_name, sections)
    
    # Environmental
    pf = park_factor / 100.0
    t_adj = 1.0 if is_dome else 1.0 + ((temp_f - 72) * 0.0008)
    eff_wind = 0 if is_dome else wind_mph * math.cos(math.radians(wind_ang))
    
    if is_dome:
        w_adj = 1.0
    else:
        if eff_wind > 10:
            base_wind = 10 * 0.004
            extra_wind = eff_wind - 10
            w_adj = 1.0 + base_wind + (math.exp(extra_wind * 0.15) - 1.0) * 0.02
        elif eff_wind < -10:
            base_wind = -10 * 0.004
            extra_wind = abs(eff_wind) - 10
            w_adj = 1.0 + base_wind - (math.exp(extra_wind * 0.15) - 1.0) * 0.02
            w_adj = max(0.85, w_adj)
        else:
            w_adj = 1.0 + (eff_wind * 0.004)
            
    if pf >= 1.10:
        pf_mod = 1.0 + ((pf - 1.0) * 1.5)
    else:
        pf_mod = pf
        
    env_factor = pf_mod * t_adj * w_adj
    
    ar, hr, a_k, h_k = simulate_game_v6(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                                        away_wrc, home_wrc, env_factor)
                                        
    # Data Aggregation
    n = len(ar)
    tr = [ar[i]+hr[i] for i in range(n)]
    
    aw = sum(1 for i in range(n) if ar[i]>hr[i])
    hw = sum(1 for i in range(n) if hr[i]>ar[i])
    ties = n-aw-hw
    apct = (aw + ties*0.48)/n*100
    hpct = (hw + ties*0.52)/n*100
    
    away_mu = sum(ar)/n
    home_mu = sum(hr)/n
    total_mu = sum(tr)/n
    
    ak_mean = sum(a_k)/n
    hk_mean = sum(h_k)/n
    
    # ── REPORTING ──
    print(f"╔══════════════════════════════════════════════════════════════════╗")
    print(f"║        MLB QUANT-ELITE V6.0 | DETERMINISTIC STATE ENGINE       ║")
    print(f"║        {away_team} @ {home_team} | MICRO-SIMULATION                 ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝\n")
    
    print(f"── 1. DYNAMIC PITCHER ATTRITION ─────────────────────────────────")
    print(f"  {away_sp_name} ({away_sp_hand})")
    print(f"    Blended ERA: {away_sp_stats['Blended']:.2f}")
    print(f"    Opponent wRC+ (vs {away_sp_hand}): {home_wrc:.1f}")
    print(f"    Expected IP: {away_sp_stats['Exp_IP']:.2f}")
    print(f"    Projected Ks: {ak_mean:.2f} (Adjusted for blowout risk)")
    print()
    print(f"  {home_sp_name} ({home_sp_hand})")
    print(f"    Blended ERA: {home_sp_stats['Blended']:.2f}")
    print(f"    Opponent wRC+ (vs {home_sp_hand}): {away_wrc:.1f}")
    print(f"    Expected IP: {home_sp_stats['Exp_IP']:.2f}")
    print(f"    Projected Ks: {hk_mean:.2f} (Adjusted for blowout risk)")
    
    print(f"\n── 2. SITUATIONAL BULLPEN TIERS ─────────────────────────────────")
    print(f"  {away_team} Bullpen -> High Lev: {away_bp['A']:.2f} | Mop-Up: {away_bp['B']:.2f}")
    print(f"  {home_team} Bullpen -> High Lev: {home_bp['A']:.2f} | Mop-Up: {home_bp['B']:.2f}")
    
    print(f"\n── 3. STATE ENGINE EXPECTANCY ({N_SIMS:,} SIMS) ───────────────────")
    fav = away_team if apct > hpct else home_team
    fav_pct = max(apct, hpct)
    print(f"  {away_team}: {away_mu:.3f} runs  |  {home_team}: {home_mu:.3f} runs")
    print(f"  TOTAL: {total_mu:.3f} runs")
    print(f"  WIN PROBABILITY: {away_team} {apct:.1f}% | {home_team} {hpct:.1f}% -> EDGE: {fav} ({fav_pct:.1f}%)")
    
    print(f"\n── 4. K-PROP ANALYSIS (V6 FIX) ──────────────────────────────────")
    for k_val in [2.5, 3.5, 4.5, 5.5, 6.5, 7.5]:
        a_over = sum(1 for k in a_k if k > k_val)/n*100
        h_over = sum(1 for k in h_k if k > k_val)/n*100
        print(f"  O/U {k_val:3.1f} Ks -> {away_team} SP Over: {a_over:4.1f}% | {home_team} SP Over: {h_over:4.1f}%")
        
    print(f"\n==================================================================")
    print(f"  V6 FINAL: {away_team} {away_mu:.2f} — {home_team} {home_mu:.2f}")
    print(f"==================================================================")

if __name__ == '__main__':
    # Test execution for CWS @ ARI from April 22 (The blowout that broke V5)
    CWS_LINEUP = [('A', 'R')]*9 # Mock
    ARI_LINEUP = [('B', 'R')]*9 # Mock
    run_v6_protocol('CHW', 'ARI', 'Anthony Kay', 'Eduardo Rodriguez', 'L', 'L',
                    10.50, 4.50, CWS_LINEUP, ARI_LINEUP, 104, True, 75, 0)