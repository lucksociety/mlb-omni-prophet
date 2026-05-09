#!/usr/bin/env python3
"""
MLB QUANT-ELITE V6.4 — THE COMPREHENSIVE ENGINE
Fixes: Statcast Shrinkage, DRS Dampeners, Dynamic Hook Logic, Bullpen Fatigue, Umpire Variance
"""
import csv, random, math, statistics
from collections import Counter
import datetime

random.seed(2026_04_24)
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
}

CATCHER_TIERS = {
    'Patrick Bailey': 1.15,  # God tier framing
    'Alejandro Kirk': 1.10,
    'Austin Wells': 1.10,
    'Cal Raleigh': 1.08,     # The Architect
    'Will Smith': 1.05,
    'Edgar Quero': 0.85,     # Leakage
}

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
                        # V6.2 Fix: Use full header name or strip more carefully to avoid wRC vs wRC+ collisions
                        headers = [h.strip() for h in row]
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
    last = name_l.split()[-1].lower()
    for p in players:
        pn = p.get('Name','').lower()
        if name_l in pn or (last in pn and len(last) > 3): return p
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
    
    wrc_key = 'wRC+ wRC+ - Runs per PA scaled where 100 is average; both league and park adjusted; based on wOBA'
    
    wrcs = []
    for name, hand in lineup_names:
        match = fuzzy_find(name, team_batters) or fuzzy_find(name, all_batters)
        
        # Fallback to Advanced if not found in splits
        if not match and (opposing_sp_hand == 'L' or opposing_sp_hand == 'R'):
            adv_batters = sections.get('Batting Advanced', [])
            team_adv = [b for b in adv_batters if b.get('Team') == team]
            match = fuzzy_find(name, team_adv) or fuzzy_find(name, adv_batters)

        if match:
            # Try various potential keys for wRC+
            val = match.get(wrc_key) or match.get('wRC+') or '100'
            try:
                wrcs.append(float(val))
            except: wrcs.append(100.0)
        else:
            wrcs.append(90.0) 
    
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
        'HardHit%': 38.0, 'Barrel%': 7.5, 'xERA': 4.15
    }
    
    xfip_key = 'xFIP xFIP - Expected Fielding Independent Pitching'
    k9_key = 'K/9 K/9 - Strikeouts per 9 innings'
    
    if p:
        stats['xFIP'] = float(p.get(xfip_key) or p.get('xFIP', 4.15))
        stats['IP'] = float(p.get('IP IP - Innings Pitched') or p.get('IP', 15.0))
        stats['K/9'] = float(p.get(k9_key) or p.get('K/9', 8.5))
        
    if stuff_p:
        val = stuff_p.get('Stuff+ Stuff+ - Model based pitching metric where 100 is average') or stuff_p.get('Stuff+')
        try:
            if val and val.strip():
                stats['Stuff+'] = float(val)
        except: pass
        
    if sc_p:
        hh_key = 'HardHit% HardHit% -  Percentage of batted balls with exit velocity of 95 mph or higher'
        br_key = 'Barrel% Barrel% - Percentage of batted balls that are classified as barrels'
        xera_key = 'xERA xERA - Expected ERA'
        
        try:
            val = sc_p.get(hh_key) or sc_p.get('HardHit%')
            if val and val.strip():
                stats['HardHit%'] = float(val.strip('%'))
        except: pass
        try:
            val = sc_p.get(br_key) or sc_p.get('Barrel%')
            if val and val.strip():
                stats['Barrel%'] = float(val.strip('%'))
        except: pass
        try:
            val = sc_p.get(xera_key) or sc_p.get('xERA')
            if val and val.strip():
                stats['xERA'] = float(val)
        except: pass
        
    return stats

# ── 2. DYNAMIC PITCHING & BULLPEN STATE ─────────────────────────

def get_bullpen_tiers(team, sp_name, sections):
    pitchers = [p for p in sections.get('Pitching Advanced', [])
                if p.get('Team') == team and p.get('Name','') != sp_name]
    
    xfips = []
    for p in pitchers:
        val = None
        # Try finding a key that contains 'xFIP' but is NOT 'xFIP-'
        for k, v in p.items():
            if 'xFIP' in k and 'xFIP-' not in k:
                try:
                    val = float(v)
                    break
                except: continue
        if val is not None:
            xfips.append(val)
        else:
            xfips.append(4.15) # Default fallback
        
    if not xfips:
        return {'A': 3.50, 'B': 5.00, 'C': 9.00, 'AVG': 4.15}
        
    xfips.sort()
    a_team = xfips[:2] if len(xfips) >= 2 else xfips
    b_team = xfips[-3:] if len(xfips) >= 3 else xfips
    c_team = xfips[-1:] if len(xfips) >= 1 else xfips
    
    return {
        'A': sum(a_team)/len(a_team),
        'B': sum(b_team)/len(b_team),
        'C': (sum(c_team)/len(c_team)) * 1.30,
        'AVG': sum(xfips)/len(xfips)
    }

def bayesian_era_v6_4(stats, era_26):
    xfip = stats['xFIP']
    ip = stats['IP']
    xera = stats['xERA']
    hh_pct = stats['HardHit%']
    barrel_pct = stats['Barrel%']
    
    w26 = min(0.45, ip / 50.0)
    sc_mod = 1.0
    if hh_pct > 42.0: sc_mod += (hh_pct - 42.0) * 0.0075
    if barrel_pct > 10.0: sc_mod += (barrel_pct - 10.0) * 0.01
    sc_mod = min(sc_mod, 1.15) # Shrinkage Cap
    
    base_blended = (1-w26)*xfip + w26*era_26
    final_era = (base_blended * 0.7 + xera * 0.3) * sc_mod
    
    return max(1.50, min(final_era, 9.50))

def calc_expected_ip(blended_era, opp_wrc, manager_hook=0.0, base_ip=5.5):
    era_penalty = (blended_era - 4.0) * 0.5
    wrc_penalty = (opp_wrc - 100.0) * 0.02
    ip = base_ip - era_penalty - wrc_penalty + manager_hook
    return max(2.5, min(ip, 7.0))

# ── 3. MATH DISTRIBUTION GENERATORS ─────────────────────────────

def poisson_rvs(lam):
    if lam <= 0: return 0
    if lam > 500: return max(0, int(random.gauss(lam, math.sqrt(lam))))
    L = math.exp(-lam); k=0; p=1.0
    while p > L: k+=1; p*=random.random()
    return k-1

def nbinom_rvs(n, mu):
    if mu <= 0: return 0
    p = n / (n + mu)
    return poisson_rvs(random.gammavariate(n, (1.0-p)/p))

# ── 4. STATE ENGINE SIMULATOR ───────────────────────────────────

def simulate_game_v6_4(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                       away_wrc, home_wrc, env_factor, rain_intensity=0, runs_to_blowout=6,
                       away_drs=0, home_drs=0, umpire_zone='neutral'):
    
    # Apply Umpire Variance
    umpire_k_mod = 1.0
    umpire_run_mod = 1.0
    if umpire_zone == 'tight':
        umpire_k_mod = 0.92
        umpire_run_mod = 1.05 # more walks leading to runs
    elif umpire_zone == 'wide':
        umpire_k_mod = 1.08
        umpire_run_mod = 0.95
        
    away_sp_stuff_mod = 1.0 - ((away_sp_stats['Stuff+'] - 100) * 0.005)
    home_sp_stuff_mod = 1.0 - ((home_sp_stats['Stuff+'] - 100) * 0.005)
    rain_grip_penalty = 1.0 + (rain_intensity * 0.15)
    
    # DRS Dampeners
    away_drs_dampener = 1.0 - (home_drs * 0.015)
    home_drs_dampener = 1.0 - (away_drs * 0.015)
    away_drs_dampener = max(0.85, min(1.15, away_drs_dampener))
    home_drs_dampener = max(0.85, min(1.15, home_drs_dampener))
    
    away_sp_mu = (away_sp_stats['Blended'] / 9.0) * away_sp_stats['Exp_IP'] * (home_wrc/100.0) * away_sp_stuff_mod * env_factor * rain_grip_penalty * home_drs_dampener * umpire_run_mod
    home_sp_mu = (home_sp_stats['Blended'] / 9.0) * home_sp_stats['Exp_IP'] * (away_wrc/100.0) * home_sp_stuff_mod * env_factor * rain_grip_penalty * away_drs_dampener * umpire_run_mod

    away_total_runs = []; home_total_runs = []; away_sp_k_dist = []; home_sp_k_dist = []
    sp_k = 20.0 # Capped NB for Fat-Tail Bias (was 15.0)
    if rain_intensity > 0.4: sp_k = 15.0

    for _ in range(N_SIMS):
        # Away Batting
        h_sp_runs = nbinom_rvs(sp_k, home_sp_mu)
        actual_h_ip = home_sp_stats['Exp_IP']
        
        # Chapter 9.2: Laboring Inefficiency Check
        est_ppi = 15.0 + (h_sp_runs * 2.2) + (home_sp_stats['K/9'] * 0.4)
        if est_ppi > 19.5:
            labor_mod = (est_ppi - 19.5) * 0.4
            actual_h_ip = max(2.0, actual_h_ip - labor_mod)

        if h_sp_runs >= 4:
            actual_h_ip = max(2.0, actual_h_ip - (h_sp_runs - 3)*0.5) # Dynamic Hook
        if random.random() < 0.02:
            actual_h_ip = random.uniform(0.1, 2.0); h_sp_runs += poisson_rvs(2.0)
        
        bp_innings = 9.0 - actual_h_ip
        if h_sp_runs >= runs_to_blowout or actual_h_ip < 4.0:
            tm = 1.25 if actual_h_ip < 4.0 else 1.0
            h_bp_mu = (home_bp['C'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty * tm * home_drs_dampener * umpire_run_mod
        elif actual_h_ip < home_sp_stats['Exp_IP']:
            h_bp_mu = (home_bp['B'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty * home_drs_dampener * umpire_run_mod
        else:
            h_bp_mu = (home_bp['A'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty * home_drs_dampener * umpire_run_mod
        a_runs = h_sp_runs + poisson_rvs(h_bp_mu)
        
        # Home Batting
        a_sp_runs = nbinom_rvs(sp_k, away_sp_mu)
        actual_a_ip = away_sp_stats['Exp_IP']
        
        # Chapter 9.2: Laboring Inefficiency Check
        # Estimate pitch count based on runs and expected K rate
        est_ppi = 15.0 + (a_sp_runs * 2.2) + (away_sp_stats['K/9'] * 0.4)
        if est_ppi > 19.5:
            labor_mod = (est_ppi - 19.5) * 0.4
            actual_a_ip = max(2.0, actual_a_ip - labor_mod)

        if a_sp_runs >= 4:
            actual_a_ip = max(2.0, actual_a_ip - (a_sp_runs - 3)*0.5) # Dynamic Hook
        if random.random() < 0.02:
            actual_a_ip = random.uniform(0.1, 2.0); a_sp_runs += poisson_rvs(2.0)
            
        bp_innings = 9.0 - actual_a_ip
        if a_sp_runs >= runs_to_blowout or actual_a_ip < 4.0:
            tm = 1.25 if actual_a_ip < 4.0 else 1.0
            a_bp_mu = (away_bp['C'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty * tm * away_drs_dampener * umpire_run_mod
        elif actual_a_ip < away_sp_stats['Exp_IP']:
            a_bp_mu = (away_bp['B'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty * away_drs_dampener * umpire_run_mod
        else:
            a_bp_mu = (away_bp['A'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty * away_drs_dampener * umpire_run_mod
        h_runs = a_sp_runs + poisson_rvs(a_bp_mu)

        away_total_runs.append(a_runs); home_total_runs.append(h_runs)
        
        # K-Decay Calibrated with Umpire Zone
        base_a_k_mu = (away_sp_stats['K/9']/9.0)*actual_a_ip
        wrc_k_adj_a = max(0.7, 1.0 - ((home_wrc - 100) * 0.002))
        raw_a_k_mu = base_a_k_mu * wrc_k_adj_a * umpire_k_mod
        away_sp_k_dist.append(poisson_rvs(raw_a_k_mu))
        
        base_h_k_mu = (home_sp_stats['K/9']/9.0)*actual_h_ip
        wrc_k_adj_h = max(0.7, 1.0 - ((away_wrc - 100) * 0.002))
        raw_h_k_mu = base_h_k_mu * wrc_k_adj_h * umpire_k_mod
        home_sp_k_dist.append(poisson_rvs(raw_h_k_mu))
        
    return away_total_runs, home_total_runs, away_sp_k_dist, home_sp_k_dist

def run_v6_4_protocol(away_team, home_team, away_sp_name, home_sp_name,
                      away_sp_hand, home_sp_hand, away_era, home_era,
                      away_lineup, home_lineup, park_factor, is_dome, temp_f, wind_mph, wind_ang=90, 
                      humidity=50, altitude=0, rain_intensity=0,
                      away_drs=0, home_drs=0, away_manager_hook=0.0, home_manager_hook=0.0,
                      away_bp_pitches_d1=0, away_bp_pitches_d2=0, home_bp_pitches_d1=0, home_bp_pitches_d2=0,
                      umpire_zone='neutral', away_catcher='MISSING', home_catcher='MISSING', game_time='19:00'):
    
    sections = parse_csv('MLB Stats')
    away_sp_stats = get_pitcher_stats(away_sp_name, away_team, sections)
    home_sp_stats = get_pitcher_stats(home_sp_name, home_team, sections)
    
    away_sp_stats['Blended'] = bayesian_era_v6_4(away_sp_stats, away_era)
    home_sp_stats['Blended'] = bayesian_era_v6_4(home_sp_stats, home_era)
    
    away_wrc = get_lineup_wrc(away_lineup, away_team, sections, home_sp_hand)
    home_wrc = get_lineup_wrc(home_lineup, home_team, sections, away_sp_hand)
    
    away_sp_stats['Exp_IP'] = calc_expected_ip(away_sp_stats['Blended'], home_wrc, manager_hook=away_manager_hook)
    home_sp_stats['Exp_IP'] = calc_expected_ip(home_sp_stats['Blended'], away_wrc, manager_hook=home_manager_hook)
    
    away_bp = get_bullpen_tiers(away_team, away_sp_name, sections)
    home_bp = get_bullpen_tiers(home_team, home_sp_name, sections)
    
    print(f"  [DEBUG] {away_team} Bullpen: {away_bp}")
    print(f"  [DEBUG] {home_team} Bullpen: {home_bp}")
    
    # Bullpen Fatigue Downgrade
    away_bp_usage = (away_bp_pitches_d1 * 1.0) + (away_bp_pitches_d2 * 0.5)
    if away_bp_usage > 30:
        away_bp['A'] = away_bp['B']
        away_bp['B'] = away_bp['C']
    
    home_bp_usage = (home_bp_pitches_d1 * 1.0) + (home_bp_pitches_d2 * 0.5)
    if home_bp_usage > 30:
        home_bp['A'] = home_bp['B']
        home_bp['B'] = home_bp['C']
    
    pf = park_factor / 100.0
    t_adj = 1.0 if is_dome else 1.0 + ((temp_f - 72) * 0.0008)
    eff_wind = 0 if is_dome else wind_mph * math.cos(math.radians(wind_ang))
    h_adj = 1.0 + ((humidity - 50) * 0.0004)
    alt_adj = 1.0 + (altitude / 1000.0 * 0.01)
    
    if is_dome: w_adj = 1.0
    else:
        if eff_wind > 10: w_adj = 1.0 + (10*0.004) + (math.exp((eff_wind-10)*0.15)-1.0)*0.02
        elif eff_wind < -10: w_adj = 1.0 + (-10*0.004) - (math.exp((abs(eff_wind)-10)*0.15)-1.0)*0.02
        else: w_adj = 1.0 + (eff_wind*0.004)
            
    env_factor = pf * t_adj * w_adj * h_adj * alt_adj * (1.0 - rain_intensity*0.035)
    
    print(f"  [DEBUG] Env Factor: {env_factor:.3f} (PF:{pf} T:{t_adj:.3f} W:{w_adj:.3f} H:{h_adj:.3f} Alt:{alt_adj:.3f})")
    print(f"  [DEBUG] {away_team}: Blended ERA {away_sp_stats['Blended']:.2f}, wRC+ {away_wrc:.1f}, Exp IP {away_sp_stats['Exp_IP']:.2f}")
    print(f"  [DEBUG] {home_team}: Blended ERA {home_sp_stats['Blended']:.2f}, wRC+ {home_wrc:.1f}, Exp IP {home_sp_stats['Exp_IP']:.2f}")
    
    # K-Prophet Bible: Shadow Transition Logic
    shadow_boost = 1.0
    west_coast = ['LAD', 'SF', 'SEA', 'SD', 'ARI', 'OAK']
    if home_team in west_coast and '16:' in game_time:
        shadow_boost = 1.12 # Biological impossibility of adjustment
        print(f"  [BIBLE] Shadow Transition Active for {home_team} @ {game_time}. K-Boost applied.")

    # K-Prophet Bible: Archetype Multipliers
    def get_archetype_mod(pitcher, lineup_wrc):
        arch = ARCHETYPES.get(pitcher, 'Standard')
        if arch == 'North-South' and lineup_wrc > 110: # High power/uppercut lineups
            return 1.15
        if arch == 'East-West' and lineup_wrc < 90: # Slap hitter lineups
            return 0.90
        if arch == 'Unicorn':
            return 1.10
        return 1.0

    away_arch_mod = get_archetype_mod(away_sp_name, home_wrc)
    home_arch_mod = get_archetype_mod(home_sp_name, away_wrc)

    # K-Prophet Bible: Catcher Adjustment
    away_cadj = CATCHER_TIERS.get(away_catcher, 1.0)
    home_cadj = CATCHER_TIERS.get(home_catcher, 1.0)

    # Update K/9 with Bible modifiers
    away_sp_stats['K/9'] *= away_arch_mod * away_cadj * shadow_boost
    home_sp_stats['K/9'] *= home_arch_mod * home_cadj * shadow_boost
    
    ar, hr, a_k, h_k = simulate_game_v6_4(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                                          away_wrc, home_wrc, env_factor, rain_intensity, 6,
                                          away_drs, home_drs, umpire_zone)
                                         
    n = len(ar)
    tr = [ar[i]+hr[i] for i in range(n)]
    aw = sum(1 for i in range(n) if ar[i]>hr[i]); hw = sum(1 for i in range(n) if hr[i]>ar[i]); ties = n-aw-hw
    apct = (aw + ties*0.48)/n*100; hpct = (hw + ties*0.52)/n*100
    away_mu = sum(ar)/n; home_mu = sum(hr)/n; total_mu = sum(tr)/n
    ak_mean = sum(a_k)/n; hk_mean = sum(h_k)/n
    ak_med = statistics.median(a_k); hk_med = statistics.median(h_k)
    blowout_prob = sum(1 for r in tr if r > 13) / n * 100
    run_diff = abs(away_mu - home_mu)

    print(f"╔══════════════════════════════════════════════════════════════════╗")
    print(f"║        MLB QUANT-ELITE V6.4 | THE COMPREHENSIVE ENGINE        ║")
    print(f"║        {away_team} @ {home_team} | DETERMINISTIC STATE ENGINE         ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝\n")
    print(f"── 1. STATE ENGINE EXPECTANCY ({N_SIMS:,} SIMS) ───────────────────")
    print(f"  {away_team}: {away_mu:.3f} runs  |  {home_team}: {home_mu:.3f} runs")
    print(f"  TOTAL: {total_mu:.3f} runs")
    print(f"  WIN PROBABILITY: {away_team} {apct:.1f}% | {home_team} {hpct:.1f}%")
    print(f"  BLOWOUT PROBABILITY (>13 RUNS): {blowout_prob:.1f}%")
    
    print(f"\n── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────")
    print(f"  {away_sp_name} - {ak_mean:.2f} K's - Final Prediction: {int(ak_med)} K's")
    print(f"  {home_sp_name} - {hk_mean:.2f} K's - Final Prediction: {int(hk_med)} K's")
    
    print(f"\n── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────")
    if run_diff < 0.5:
        print(f"  [WARNING] Run Diff {run_diff:.2f} < 0.5. TOSS-UP: FADE MONEYLINE.")
        print(f"  [ACTION] Focus on Game Totals or Pitcher Unders.")
    elif run_diff >= 1.4:
        fav = away_team if away_mu > home_mu else home_team
        print(f"  [EDGE DETECTED] Run Diff {run_diff:.2f} >= 1.4. MASSIVE EDGE: CONSIDER RUNLINE (-1.5) FOR {fav}.")
    else:
        fav = away_team if away_mu > home_mu else home_team
        print(f"  [EDGE DETECTED] Run Diff {run_diff:.2f}. CONSIDER MONEYLINE FOR {fav}.")

    print(f"\n==================================================================")
    print(f"  V6.4 FINAL: {away_team} {away_mu:.2f} — {home_team} {home_mu:.2f}")
    print(f"==================================================================")
    
    return ar, hr, a_k, h_k

if __name__ == '__main__':
    # Test LAA @ KC failure state
    laa_lineup = [('Neto', 'R'), ('Trout', 'R'), ('Adell', 'R'), ('Soler', 'R'), ('Peraza', 'R'), ('Schanuel', 'L'), ('Grissom', 'R'), ('O\'Hoppe', 'R'), ('Teodosio', 'R')]
    kcr_lineup = [('Garcia', 'R'), ('Witt', 'R'), ('Pasquantino', 'L'), ('Perez', 'R'), ('Jensen', 'L'), ('Massey', 'L'), ('Caglianone', 'L'), ('Collins', 'S'), ('Isbel', 'L')]
    run_v6_4_protocol('LAA', 'KCR', 'Walbert Urena', 'Cole Ragans', 'R', 'L',
                      2.35, 6.00, laa_lineup, kcr_lineup, 101, False, 62, 9, 60, 50, 912, 0.0)
