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
MLB QUANT-ELITE V6.1 — GOD-LIKE DETERMINISTIC STATE ENGINE
New: Rain/Humidity Physics, Altitude Modifiers, and Multi-Stage Delay Logic
"""
import csv, random, math
from collections import Counter
import datetime

random.seed(2026_04_24)
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
            wrcs.append(85.0) 
    
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
    pitchers = [p for p in sections.get('Pitching Advanced', [])
                if p.get('Team') == team and p.get('Name','') != sp_name]
    
    xfips = []
    for p in pitchers:
        try: xfips.append(float(p.get('xFIP', 4.15)))
        except: pass
        
    if not xfips:
        return {'A': 3.50, 'B': 5.00, 'C': 7.50, 'AVG': 4.15}
        
    xfips.sort()
    a_team = xfips[:2] if len(xfips) >= 2 else xfips
    b_team = xfips[-3:] if len(xfips) >= 3 else xfips
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
    era_penalty = (blended_era - 4.0) * 0.4
    wrc_penalty = (opp_wrc - 100.0) * 0.015
    ip = base_ip - era_penalty - wrc_penalty
    return max(3.0, min(ip, 7.0))

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

def simulate_game_v6_1(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                       away_wrc, home_wrc, env_factor, rain_intensity=0, runs_to_blowout=4):
    """
    V6.1 Engine: Includes Rain Intensity (0-1) and Attrition Cascades.
    """
    
    # 1. Base expected runs for Starters
    away_sp_stuff_mod = 1.0 - ((away_sp_stats['Stuff+'] - 100) * 0.005)
    home_sp_stuff_mod = 1.0 - ((home_sp_stats['Stuff+'] - 100) * 0.005)
    
    # Rain Grip Penalty (Lower K%, Higher Mu)
    rain_grip_penalty = 1.0 + (rain_intensity * 0.12) # Up to 12% boost to runs due to command loss
    
    # Home Team Batting (Away SP)
    away_sp_mu = (away_sp_stats['Blended'] / 9.0) * away_sp_stats['Exp_IP'] * (home_wrc/100.0) * away_sp_stuff_mod * env_factor * rain_grip_penalty
    # Away Team Batting (Home SP)
    home_sp_mu = (home_sp_stats['Blended'] / 9.0) * home_sp_stats['Exp_IP'] * (away_wrc/100.0) * home_sp_stats_mod * env_factor * rain_grip_penalty

    away_total_runs = []
    home_total_runs = []
    away_sp_k_dist = []
    home_sp_k_dist = []
    
    # Variance Injection
    sp_k = 4.5
    if rain_intensity > 0.5: sp_k = 3.5 # Higher variance in rain
    
    ap_ap = sp_k / (sp_k + home_sp_mu) if home_sp_mu > 0 else 0.99
    hp_ap = sp_k / (sp_k + away_sp_mu) if away_sp_mu > 0 else 0.99

    for _ in range(N_SIMS):
        # -- SIMULATE HOME SP (AWAY BATTING) --
        h_sp_runs = nbinom_rvs(sp_k, ap_ap)
        actual_h_ip = home_sp_stats['Exp_IP']
        
        # Rain Delay Hook Check
        if rain_intensity > 0.7 and random.random() < 0.2: # 20% chance of rain hook
            actual_h_ip = min(actual_h_ip, random.uniform(1.0, 4.0))
            
        # Cascade Failure Check (Blowout)
        if h_sp_runs >= runs_to_blowout or actual_h_ip < home_sp_stats['Exp_IP']:
            bp_innings = 9.0 - actual_h_ip
            if actual_h_ip < 3.0:
                h_bp_mu = (home_bp['C'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty
            else:
                h_bp_mu = (home_bp['B'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty
        else:
            bp_innings = 9.0 - actual_h_ip
            h_bp_mu = (home_bp['A'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty
            
        a_runs = h_sp_runs + poisson_rvs(h_bp_mu)
        
        # K-Prop (Rain Penalty)
        h_sp_k_mu = (home_sp_stats['K/9'] / 9.0) * actual_h_ip * (1.0 - rain_intensity * 0.1)
        home_sp_k_dist.append(poisson_rvs(h_sp_k_mu))
        
        # -- SIMULATE AWAY SP (HOME BATTING) --
        a_sp_runs = nbinom_rvs(sp_k, hp_ap)
        actual_a_ip = away_sp_stats['Exp_IP']
        
        if rain_intensity > 0.7 and random.random() < 0.2:
            actual_a_ip = min(actual_a_ip, random.uniform(1.0, 4.0))

        if a_sp_runs >= runs_to_blowout or actual_a_ip < away_sp_stats['Exp_IP']:
            bp_innings = 9.0 - actual_a_ip
            if actual_a_ip < 3.0:
                a_bp_mu = (away_bp['C'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty
            else:
                a_bp_mu = (away_bp['B'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty
        else:
            bp_innings = 9.0 - actual_a_ip
            a_bp_mu = (away_bp['A'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty
            
        h_runs = a_sp_runs + poisson_rvs(a_bp_mu * 1.03) 
        
        # K-Prop
        a_sp_k_mu = (away_sp_stats['K/9'] / 9.0) * actual_a_ip * (1.0 - rain_intensity * 0.1)
        away_sp_k_dist.append(poisson_rvs(a_sp_k_mu))
        
        away_total_runs.append(a_runs)
        home_total_runs.append(h_runs)
        
    return away_total_runs, home_total_runs, away_sp_k_dist, home_sp_k_dist

# ── EXPORTED PROTOCOL ─────────────────────────────────────────
def run_v6_1_protocol(away_team, home_team, away_sp_name, home_sp_name,
                      away_sp_hand, home_sp_hand, away_era, home_era,
                      away_lineup, home_lineup, park_factor, is_dome, temp_f, wind_mph, wind_ang=90, 
                      humidity=50, altitude=0, rain_intensity=0):
    
    sections = parse_csv('MLB Stats')
    
    away_sp_stats = get_pitcher_stats(away_sp_name, away_team, sections)
    home_sp_stats = get_pitcher_stats(home_sp_name, home_team, sections)
    
    away_sp_stats['Blended'] = bayesian_era(away_sp_stats['xFIP'], away_era, away_sp_stats['IP'])
    home_sp_stats['Blended'] = bayesian_era(home_sp_stats['xFIP'], home_era, home_sp_stats['IP'])
    
    away_wrc = get_lineup_wrc(away_lineup, away_team, sections, home_sp_hand)
    home_wrc = get_lineup_wrc(home_lineup, home_team, sections, away_sp_hand)
    
    away_sp_stats['Exp_IP'] = calc_expected_ip(away_sp_stats['Blended'], home_wrc)
    home_sp_stats['Exp_IP'] = calc_expected_ip(home_sp_stats['Blended'], away_wrc)
    
    away_bp = get_bullpen_tiers(away_team, away_sp_name, sections)
    home_bp = get_bullpen_tiers(home_team, home_sp_name, sections)
    
    # V6.1 Physics Adjustments
    pf = park_factor / 100.0
    t_adj = 1.0 if is_dome else 1.0 + ((temp_f - 72) * 0.0008)
    eff_wind = 0 if is_dome else wind_mph * math.cos(math.radians(wind_ang))
    
    # Humidity logic (High humidity = less dense air = more carry)
    h_adj = 1.0 + ((humidity - 50) * 0.0004)
    # Altitude logic (1% boost per 1000ft)
    alt_adj = 1.0 + (altitude / 1000.0 * 0.01)
    
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
            
    # Rain Distance Penalty (Damp ball)
    rain_dist_penalty = 1.0 - (rain_intensity * 0.03)
            
    env_factor = pf * t_adj * w_adj * h_adj * alt_adj * rain_dist_penalty
    
    # Variable rename fix for home_sp_stats_mod in simulate_game
    global home_sp_stats_mod # Not ideal but quick fix for the sim function
    home_sp_stats_mod = home_sp_stuff_mod = 1.0 - ((home_sp_stats['Stuff+'] - 100) * 0.005)

    ar, hr, a_k, h_k = simulate_game_v6_1(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                                          away_wrc, home_wrc, env_factor, rain_intensity)
                                         
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
    
    print(f"╔══════════════════════════════════════════════════════════════════╗")
    print(f"║        MLB QUANT-ELITE V6.1 | GOD-LIKE STATE ENGINE            ║")
    print(f"║        {away_team} @ {home_team} | RAIN-ADJUSTED SIMULATION         ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝\n")
    
    print(f"── 1. ENVIRONMENTAL SENSORS ─────────────────────────────────────")
    print(f"    Temp: {temp_f}F | Humidity: {humidity}% | Altitude: {altitude}ft")
    print(f"    Rain Intensity: {rain_intensity*100:.0f}% {'(HIGH RISK)' if rain_intensity > 0.5 else ''}")
    print(f"    Effective Env Factor: {env_factor:.3f}")
    print()
    print(f"── 2. DYNAMIC PITCHER ATTRITION ─────────────────────────────────")
    print(f"  {away_sp_name} ({away_sp_hand}) -> Projected Ks: {ak_mean:.2f}")
    print(f"  {home_sp_name} ({home_sp_hand}) -> Projected Ks: {hk_mean:.2f}")
    
    print(f"\n── 3. STATE ENGINE EXPECTANCY ({N_SIMS:,} SIMS) ───────────────────")
    print(f"  {away_team}: {away_mu:.3f} runs  |  {home_team}: {home_mu:.3f} runs")
    print(f"  TOTAL: {total_mu:.3f} runs")
    print(f"  WIN PROBABILITY: {away_team} {apct:.1f}% | {home_team} {hpct:.1f}%")
    
    print(f"\n==================================================================")
    print(f"  V6.1 FINAL: {away_team} {away_mu:.2f} — {home_team} {home_mu:.2f}")
    print(f"==================================================================")

if __name__ == '__main__':
    # Test DET @ CIN with Rain
    run_v6_1_protocol('DET', 'CIN', 'Framber Valdez', 'Andrew Abbott', 'L', 'L',
                      3.30, 5.84, [('A','R')]*9, [('B','R')]*9, 122, False, 81, 10, 90, 75, 500, 0.6)