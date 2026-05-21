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
MLB QUANT-ELITE V9.0 — THE INTEGRATED ENGINE
Synthesis of V6.4 (Dynamic Hooks/Archetypes) and V8.0 (Bivariate Correlation/Circadian Logistics)
Includes: Tier C Attrition, Shadow Transition, Extension/Stuff+ Shrinkage
"""
import csv, random, math, statistics
from collections import Counter
import datetime

random.seed(2026_04_30)
N_SIMS = 100000

# ── 0. BIBLE CONSTANTS & ARCHETYPES (2026) ──────────────────────

ARCHETYPES = {
    'Paul Skenes': 'North-South',
    'Tarik Skubal': 'North-South',
    'Will Warren': 'North-South',
    'Gerrit Cole': 'North-South',
    'Spencer Strider': 'North-South',
    'Luis Castillo': 'Unicorn',
    'Logan Webb': 'Unicorn',
    'Jhoan Duran': 'Unicorn',
    'Clay Holmes': 'East-West',
    'Logan Gilbert': 'East-West',
    'Cole Ragans': 'North-South',
    'Jacob deGrom': 'Unicorn',
    'Spencer Arrighetti': 'Unicorn',
    'Connelly Early': 'North-South',
}

CATCHER_TIERS = {
    'Patrick Bailey': {'framing': 1.15, 'offensive_mod': 0},
    'Alejandro Kirk': {'framing': 1.10, 'offensive_mod': 0},
    'Austin Wells': {'framing': 1.10, 'offensive_mod': 0},
    'Cal Raleigh': {'framing': 1.08, 'offensive_mod': 0},
    'Will Smith': {'framing': 1.05, 'offensive_mod': 0},
    'Edgar Quero': {'framing': 0.85, 'offensive_mod': -12},
    'Yainer Diaz': {'framing': 1.02, 'offensive_mod': 0},
    'Connor Wong': {'framing': 1.03, 'offensive_mod': 0},
}

TURF_TEAMS = ['ARI', 'TEX', 'MIA', 'TOR', 'TB']

# ── 1. DATA PARSING & PLATOON LOGIC (V6.4 ROBUST) ───────────────

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
                        headers = [h.strip() for h in row]
                        continue
                    if headers and fv != '#' and len(row) >= len(headers):
                        sections[current_section].append(dict(zip(headers, row[:len(headers)])))
    except FileNotFoundError:
        return {}
    return sections

def fuzzy_find(name, players):
    if not players: return None
    name_l = name.lower()
    last = name_l.split()[-1].lower()
    for p in players:
        pn = p.get('Name','').lower()
        if name_l in pn or (last in pn and len(last) > 3): return p
    return None

def get_lineup_wrc(lineup_names, team, sections, opposing_sp_hand=None, catcher_name=None):
    if opposing_sp_hand == 'L' and 'Batting Splits LHP' in sections:
        batters = sections['Batting Splits LHP']
    elif opposing_sp_hand == 'R' and 'Batting Splits RHP' in sections:
        batters = sections['Batting Splits RHP']
    else:
        batters = sections.get('Batting Advanced', [])
        
    team_batters = [b for b in batters if b.get('Team') == team]
    all_batters = batters
    wrc_key = 'wRC+ wRC+ - Runs per PA scaled where 100 is average; both league and park adjusted; based on wOBA'
    
    wrcs = []
    for name, hand in lineup_names:
        match = fuzzy_find(name, team_batters) or fuzzy_find(name, all_batters)
        if not match and (opposing_sp_hand == 'L' or opposing_sp_hand == 'R'):
            adv_batters = sections.get('Batting Advanced', [])
            team_adv = [b for b in adv_batters if b.get('Team') == team]
            match = fuzzy_find(name, team_adv) or fuzzy_find(name, adv_batters)

        if match:
            val = match.get(wrc_key) or match.get('wRC+') or '100'
            try: base_wrc = float(val)
            except: base_wrc = 100.0
        else:
            base_wrc = 90.0 
        
        if name == catcher_name:
            c_data = CATCHER_TIERS.get(name, {})
            base_wrc += c_data.get('offensive_mod', 0)
        wrcs.append(base_wrc)
    return sum(wrcs) / len(wrcs) if wrcs else 100.0

def get_pitcher_stats(name, team, sections):
    pitchers = sections.get('Pitching Advanced', [])
    team_p = [p for p in pitchers if p.get('Team') == team]
    p = fuzzy_find(name, team_p) or fuzzy_find(name, pitchers)
    
    stuff_data = sections.get('Pitching +', [])
    stuff_p = fuzzy_find(name, stuff_data)
    
    sc_data = sections.get('Pitching Statcast', [])
    sc_p = fuzzy_find(name, sc_data)
    
    stats = {
        'xFIP': 4.15, 'IP': 15.0, 'K/9': 8.5, 'K%': 0.22, 'Stuff+': 100.0,
        'HardHit%': 38.0, 'Barrel%': 7.5, 'xERA': 4.15, 'Extension': 6.0
    }
    
    if p:
        stats['xFIP'] = float(p.get('xFIP xFIP - Expected Fielding Independent Pitching') or p.get('xFIP', 4.15))
        stats['IP'] = float(p.get('IP IP - Innings Pitched') or p.get('IP', 15.0))
        stats['K/9'] = float(p.get('K/9 K/9 - Strikeouts per 9 innings') or p.get('K/9', 8.5))
        
    if stuff_p:
        val = stuff_p.get('Stuff+ Stuff+ - Model based pitching metric where 100 is average') or stuff_p.get('Stuff+')
        try:
            if val and val.strip(): stats['Stuff+'] = float(val)
        except: pass
        
    if sc_p:
        try:
            val = sc_p.get('HardHit% HardHit% -  Percentage of batted balls with exit velocity of 95 mph or higher') or sc_p.get('HardHit%')
            if val and val.strip(): stats['HardHit%'] = float(val.strip('%'))
        except: pass
        try:
            val = sc_p.get('Barrel% Barrel% - Percentage of batted balls that are classified as barrels') or sc_p.get('Barrel%')
            if val and val.strip(): stats['Barrel%'] = float(val.strip('%'))
        except: pass
        try:
            val = sc_p.get('xERA xERA - Expected ERA') or sc_p.get('xERA')
            if val and val.strip(): stats['xERA'] = float(val)
        except: pass
        try:
            val = sc_p.get('Extension Extension - Average release point distance from rubber') or sc_p.get('Extension')
            if val and val.strip(): stats['Extension'] = float(val)
        except: pass
        
    return stats

# ── 2. DYNAMIC PITCHING & BULLPEN STATE ─────────────────────────

def get_bullpen_tiers(team, sp_name, sections):
    pitchers = [p for p in sections.get('Pitching Advanced', [])
                if p.get('Team') == team and p.get('Name','') != sp_name]
    xfips = []
    for p in pitchers:
        val = None
        for k, v in p.items():
            if 'xFIP' in k and 'xFIP-' not in k:
                try: val = float(v); break
                except: continue
        xfips.append(val if val is not None else 4.15)
        
    if not xfips: return {'A': 3.50, 'B': 5.00, 'C': 9.00, 'AVG': 4.15}
    xfips.sort()
    a_team = xfips[:2] if len(xfips) >= 2 else xfips
    b_team = xfips[-3:] if len(xfips) >= 3 else xfips
    c_team = xfips[-1:] if len(xfips) >= 1 else xfips
    
    return {
        'A': sum(a_team)/len(a_team),
        'B': sum(b_team)/len(b_team),
        'C': (sum(c_team)/len(c_team)) * 1.35, # Increased C-Tier penalty for V9
        'AVG': sum(xfips)/len(xfips)
    }

def bayesian_era_v9(stats, era_26):
    xfip = stats['xFIP']
    xera = stats['xERA']
    hh_pct = stats['HardHit%']
    barrel_pct = stats['Barrel%']
    extension = stats.get('Extension', 6.0)
    
    # Extension -> Perceived Velocity Adjustment
    ext_bonus = (extension - 6.0) * 1.5 * 0.5
    
    # Statcast Shrinkage (V6.4)
    sc_mod = 1.0
    if hh_pct > 42.0: sc_mod += (hh_pct - 42.0) * 0.0075
    if barrel_pct > 10.0: sc_mod += (barrel_pct - 10.0) * 0.01
    sc_mod = min(sc_mod, 1.15)
    
    base_blended = (xfip * 0.7 + era_26 * 0.3)
    final_era = ((base_blended * 0.6 + xera * 0.4) * sc_mod) - ext_bonus
    
    return max(1.50, min(final_era, 9.50))

def calc_expected_ip_v9(blended_era, opp_wrc, manager_hook=0.0):
    era_penalty = (blended_era - 4.0) * 0.5
    wrc_penalty = (opp_wrc - 100.0) * 0.02
    ip = 5.5 - era_penalty - wrc_penalty + manager_hook
    return max(2.5, min(ip, 7.0))

# ── 3. MATH & CIRCADIAN LOGIC ───────────────────────────────────

def poisson_rvs(lam):
    if lam <= 0: return 0
    if lam > 500: return max(0, int(random.gauss(lam, math.sqrt(lam))))
    L = math.exp(-lam); k=0; p=1.0
    while p > L: k+=1; p*=random.random()
    return k-1

def get_alpha_s(mu_a, mu_b, rho_target=0.15, alpha_tot=4.5):
    var_a = mu_a + (mu_a**2 / alpha_tot)
    var_b = mu_b + (mu_b**2 / alpha_tot)
    numerator = rho_target * math.sqrt(var_a * var_b)
    denominator = (mu_a * mu_b) / (alpha_tot**2)
    alpha_s = numerator / denominator if denominator != 0 else 0
    return min(alpha_s, alpha_tot * 0.9)

def get_ttop_multiplier(inning):
    if inning <= 2.2: return 1.0     # 1st time
    if inning <= 4.5: return 1.04    # 2nd time
    if inning <= 6.5: return 1.10    # 3rd time
    return 1.18                     # 4th time (V9 Aggressive Penalty)

def get_travel_penalty(away_team, home_team, game_time, is_game_1=True):
    west_coast = ['LAD', 'SF', 'SEA', 'SD', 'ARI', 'OAK']
    east_coast = ['NYY', 'NYM', 'BOS', 'PHI', 'WSH', 'BAL', 'MIA', 'ATL']
    penalty = 0.0
    if away_team in east_coast and home_team in west_coast and is_game_1:
        penalty += 0.22
    if away_team in west_coast and home_team in east_coast and '13:' in game_time:
        penalty += 0.18 # Morning wood penalty for WC teams
    return penalty

# ── 4. STATE ENGINE SIMULATOR (V9 INTEGRATED) ───────────────────

def simulate_game_v9(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                     away_wrc, home_wrc, env_factor, rain_intensity=0, runs_to_blowout=5,
                     away_drs=0, home_drs=0, umpire_zone='neutral', alpha_tot=4.5, rho_target=0.15):
    
    umpire_k_mod = 1.0; umpire_run_mod = 1.0
    if umpire_zone == 'tight':
        umpire_k_mod = 0.90; umpire_run_mod = 1.08
    elif umpire_zone == 'wide':
        umpire_k_mod = 1.10; umpire_run_mod = 0.92
        
    away_sp_stuff_mod = 1.0 - ((away_sp_stats['Stuff+'] - 100) * 0.005)
    home_sp_stuff_mod = 1.0 - ((home_sp_stats['Stuff+'] - 100) * 0.005)
    rain_grip_penalty = 1.0 + (rain_intensity * 0.15)
    
    away_drs_dampener = max(0.85, min(1.15, 1.0 - (home_drs * 0.015)))
    home_drs_dampener = max(0.85, min(1.15, 1.0 - (away_drs * 0.015)))
    
    # Baseline Hourly Rates
    away_sp_base_mu = (away_sp_stats['Blended'] / 9.0) * (home_wrc/100.0) * away_sp_stuff_mod * env_factor * rain_grip_penalty * home_drs_dampener * umpire_run_mod
    home_sp_base_mu = (home_sp_stats['Blended'] / 9.0) * (away_wrc/100.0) * home_sp_stuff_mod * env_factor * rain_grip_penalty * away_drs_dampener * umpire_run_mod
    
    # Correlation Alpha
    mu_a_total = away_sp_base_mu * away_sp_stats['Exp_IP'] + (away_bp['AVG']/9.0)*(9-away_sp_stats['Exp_IP'])
    mu_h_total = home_sp_base_mu * home_sp_stats['Exp_IP'] + (home_bp['AVG']/9.0)*(9-home_sp_stats['Exp_IP'])
    alpha_s = get_alpha_s(mu_a_total, mu_h_total, rho_target, alpha_tot)
    alpha_ind = alpha_tot - alpha_s

    away_total_runs = []; home_total_runs = []; away_sp_k_dist = []; home_sp_k_dist = []

    for _ in range(N_SIMS):
        gs = random.gammavariate(alpha_s, 1.0)
        ga = random.gammavariate(alpha_ind, 1.0)
        gh = random.gammavariate(alpha_ind, 1.0)
        scale_a = (gs + ga) / alpha_tot
        scale_h = (gs + gh) / alpha_tot
        
        # AWAY PITCHING (Home Batting)
        a_runs = 0; actual_a_ip = 0; a_sp_done = False; a_k_sim = 0
        for inn in range(1, 10):
            if not a_sp_done:
                ttop = get_ttop_multiplier(actual_a_ip)
                mu_inn = (away_sp_base_mu * ttop) * scale_a
                inn_runs = poisson_rvs(mu_inn)
                a_runs += inn_runs
                actual_a_ip += 1.0
                
                # Laboring Inefficiency (V6.4)
                est_ppi = 15.0 + (inn_runs * 2.2) + (away_sp_stats['K/9'] * 0.4)
                if est_ppi > 19.5: actual_a_ip -= 0.3
                
                if a_runs >= 4 or actual_a_ip >= away_sp_stats['Exp_IP']: a_sp_done = True
                
                # K-Sim
                k_mu = (away_sp_stats['K/9']/9.0) * (1.0 - ((home_wrc-100)*0.002)) * umpire_k_mod * scale_a
                a_k_sim += poisson_rvs(k_mu)
            else:
                tier = 'A'
                if a_runs >= runs_to_blowout: tier = 'C'
                elif actual_a_ip < 4.0: tier = 'B'
                bp_inn = (away_bp[tier] / 9.0) * scale_a
                a_runs += poisson_rvs(bp_inn)
        
        # HOME PITCHING (Away Batting)
        h_runs = 0; actual_h_ip = 0; h_sp_done = False; h_k_sim = 0
        for inn in range(1, 10):
            if not h_sp_done:
                ttop = get_ttop_multiplier(actual_h_ip)
                mu_inn = (home_sp_base_mu * ttop) * scale_h
                inn_runs = poisson_rvs(mu_inn)
                h_runs += inn_runs
                actual_h_ip += 1.0
                
                est_ppi = 15.0 + (inn_runs * 2.2) + (home_sp_stats['K/9'] * 0.4)
                if est_ppi > 19.5: actual_h_ip -= 0.3
                
                if h_runs >= 4 or actual_h_ip >= home_sp_stats['Exp_IP']: h_sp_done = True
                
                k_mu = (home_sp_stats['K/9']/9.0) * (1.0 - ((away_wrc-100)*0.002)) * umpire_k_mod * scale_h
                h_k_sim += poisson_rvs(k_mu)
            else:
                tier = 'A'
                if h_runs >= runs_to_blowout: tier = 'C'
                elif actual_h_ip < 4.0: tier = 'B'
                bp_inn = (home_bp[tier] / 9.0) * scale_h
                h_runs += poisson_rvs(bp_inn)

        away_total_runs.append(h_runs); home_total_runs.append(a_runs)
        away_sp_k_dist.append(a_k_sim); home_sp_k_dist.append(h_k_sim)
        
    return away_total_runs, home_total_runs, away_sp_k_dist, home_sp_k_dist

# ── 5. MASTER PROTOCOL ──────────────────────────────────────────

def run_v9_protocol(away_team, home_team, away_sp_name, home_sp_name,
                    away_sp_hand, home_sp_hand, away_era, home_era,
                    away_lineup, home_lineup, park_factor, is_dome, temp_f, wind_mph, wind_ang=90, 
                    humidity=50, altitude=0, rain_intensity=0,
                    away_drs=0, home_drs=0, away_manager_hook=0.0, home_manager_hook=0.0,
                    away_bp_pitches_d1=0, away_bp_pitches_d2=0, home_bp_pitches_d1=0, home_bp_pitches_d2=0,
                    umpire_zone='neutral', away_catcher='MISSING', home_catcher='MISSING', 
                    game_time='19:00', is_game_1=True):
    
    sections = parse_csv('MLB Stats')
    away_sp_stats = get_pitcher_stats(away_sp_name, away_team, sections)
    home_sp_stats = get_pitcher_stats(home_sp_name, home_team, sections)
    
    away_sp_stats['Blended'] = bayesian_era_v9(away_sp_stats, away_era)
    home_sp_stats['Blended'] = bayesian_era_v9(home_sp_stats, home_era)
    
    away_wrc = get_lineup_wrc(away_lineup, away_team, sections, home_sp_hand, away_catcher)
    home_wrc = get_lineup_wrc(home_lineup, home_team, sections, away_sp_hand, home_catcher)
    
    # Circadian/Travel Integration
    t_penalty = get_travel_penalty(away_team, home_team, game_time, is_game_1)
    away_wrc -= (t_penalty * 8.0) # Fatigue impact on contact
    
    away_sp_stats['Exp_IP'] = calc_expected_ip_v9(away_sp_stats['Blended'], home_wrc, manager_hook=away_manager_hook)
    home_sp_stats['Exp_IP'] = calc_expected_ip_v9(home_sp_stats['Blended'], away_wrc, manager_hook=home_manager_hook)
    
    away_bp = get_bullpen_tiers(away_team, away_sp_name, sections)
    home_bp = get_bullpen_tiers(home_team, home_sp_name, sections)
    
    # Fatigue Degradation
    if (away_bp_pitches_d1 * 1.0 + away_bp_pitches_d2 * 0.5) > 35:
        away_bp['A'] = away_bp['B']; away_bp['B'] = away_bp['C']
    if (home_bp_pitches_d1 * 1.0 + home_bp_pitches_d2 * 0.5) > 35:
        home_bp['A'] = home_bp['B']; home_bp['B'] = home_bp['C']
    
    # Physics & Environment
    pf = park_factor / 100.0
    surf_mod = 1.03 if home_team in TURF_TEAMS else 1.0
    t_adj = 1.0 if is_dome else 1.0 + ((temp_f - 72) * 0.0008)
    eff_wind = 0 if is_dome else wind_mph * math.cos(math.radians(wind_ang))
    h_adj = 1.0 + ((humidity - 50) * 0.0004)
    alt_adj = 1.0 + (altitude / 1000.0 * 0.01)
    
    if is_dome: w_adj = 1.0
    else:
        if eff_wind > 10: w_adj = 1.0 + (10*0.004) + (math.exp((eff_wind-10)*0.15)-1.0)*0.02
        elif eff_wind < -10: w_adj = 1.0 + (-10*0.004) - (math.exp((abs(eff_wind)-10)*0.15)-1.0)*0.02
        else: w_adj = 1.0 + (eff_wind*0.004)
            
    env_factor = pf * t_adj * w_adj * h_adj * alt_adj * surf_mod * (1.0 - rain_intensity*0.035)
    
    # Shadow Transition (V6.4)
    shadow_boost = 1.0
    if home_team in ['LAD', 'SF', 'SEA', 'SD', 'ARI', 'OAK'] and '16:' in game_time:
        shadow_boost = 1.12
    
    # Archetype Modifiers
    def get_arch_mod(p_name, lineup_wrc):
        arch = ARCHETYPES.get(p_name, 'Standard')
        if arch == 'North-South' and lineup_wrc > 105: return 1.15
        if arch == 'Unicorn': return 1.10
        return 1.0

    # Framing
    away_cadj = CATCHER_TIERS.get(away_catcher, {}).get('framing', 1.0)
    home_cadj = CATCHER_TIERS.get(home_catcher, {}).get('framing', 1.0)
    
    away_sp_stats['K/9'] *= get_arch_mod(away_sp_name, home_wrc) * away_cadj * shadow_boost
    home_sp_stats['K/9'] *= get_arch_mod(home_sp_name, away_wrc) * home_cadj * shadow_boost
    
    ar, hr, a_k, h_k = simulate_game_v9(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                                        away_wrc, home_wrc, env_factor, rain_intensity, 5,
                                        away_drs, home_drs, umpire_zone)
                                         
    n = len(ar)
    tr = [ar[i]+hr[i] for i in range(n)]
    aw = sum(1 for i in range(n) if ar[i]>hr[i]); hw = sum(1 for i in range(n) if hr[i]>ar[i]); ties = n-aw-hw
    apct = (aw + ties*0.48)/n*100; hpct = (hw + ties*0.52)/n*100
    away_mu = sum(ar)/n; home_mu = sum(hr)/n; total_mu = sum(tr)/n
    ak_med = statistics.median(a_k); hk_med = statistics.median(h_k)
    blowout_prob = sum(1 for r in tr if r > 12) / n * 100
    
    print(f"╔══════════════════════════════════════════════════════════════════╗")
    print(f"║        MLB QUANT-ELITE V9.0 | THE INTEGRATED ENGINE        ║")
    print(f"║        {away_team} @ {home_team} | BIVARIATE SIMS (RHO 0.15)      ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝\n")
    print(f"  {away_team}: {away_mu:.3f} runs  |  {home_team}: {home_mu:.3f} runs")
    print(f"  TOTAL: {total_mu:.3f} runs | BLOWOUT PROB: {blowout_prob:.1f}%")
    print(f"  WIN PROBABILITY: {away_team} {apct:.1f}% | {home_team} {hpct:.1f}%")
    print(f"  K-PROJECTIONS: {away_sp_name}: {ak_med} | {home_sp_name}: {hk_med}")
    print(f"  BIVARIATE RHO (ACTUAL): {statistics.correlation(ar, hr):.4f}")
    
    return ar, hr, a_k, h_k

if __name__ == '__main__':
    # Placeholder for direct execution
    pass