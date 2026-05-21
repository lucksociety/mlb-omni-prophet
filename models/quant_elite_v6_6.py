import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

"""
MLB QUANT-ELITE V6.7 — POST-AUDIT ENGINE
Fixes V6.6: Ace K/9 floor expansion, recent-form ERA weighting,
game archetype detection, HardHit% integration in run calcs.
"""

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import csv, random, math, statistics
from collections import Counter
import datetime
import os, sys
import nrfi_yrfi_model as yrfi

random.seed()

# Auto-import calibration if available
try:
    from calibration_check import run_calibration_check
    HAS_CALIBRATION = True
except ImportError:
    HAS_CALIBRATION = False
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
    'Chris Sale': 'North-South',
    'Chase Dollander': 'North-South',
    # V6.6 Additions — pitchers that caused misses on 5/2
    'Emerson Hancock': 'North-South',
    'Reid Detmers': 'North-South',
    'Brock Burke': 'East-West',
    'Shota Imanaga': 'Unicorn',
    'Dylan Cease': 'North-South',
    'Yoshinobu Sasaki': 'Unicorn',
    'Michael King': 'North-South',
    'Max McLean': 'North-South',
    'Andrew Painter': 'North-South',
    'Cade Cavalli': 'North-South',
    'Kyle Harrison': 'North-South',
    'Spencer Arrighetti': 'North-South',
    'Seth Lugo': 'East-West',
    'Corbin Burnes': 'Unicorn',
    'Zack Wheeler': 'Unicorn',
    'Tyler Glasnow': 'North-South',
    'Shohei Ohtani': 'North-South',
    'Matthew Liberatore': 'North-South',
    'J.T. Ginn': 'East-West',
}

# V6.6: Career K/9 floors — prevents catastrophic under-projections
# Floor = ~75% of career K/9, representing absolute minimum expectation
CAREER_K9_FLOORS = {
    'Chris Sale': 8.5,       # Career 10.8 K/9 — predicting 2 Ks is insane
    'Reid Detmers': 7.5,     # High-K lefty, career ~9 K/9
    'Emerson Hancock': 6.0,  # Emerging K arm
    'Jacob deGrom': 9.0,     # Career 10.6 K/9
    'Gerrit Cole': 8.5,      # Career 10.6 K/9
    'Paul Skenes': 9.0,      # Elite K rate
    'Tarik Skubal': 8.0,     # Career ~9.5 K/9
    'Spencer Strider': 9.5,  # Career 12+ K/9
    'Dylan Cease': 8.0,      # Career 10.3 K/9
    'Tyler Glasnow': 8.5,    # Career 11.3 K/9
    'Shohei Ohtani': 8.5,    # Career 11.4 K/9
    'Yoshinobu Sasaki': 8.0, # NPB elite, MLB adaptation
    'Shota Imanaga': 7.5,    # High K lefty
    'Cole Ragans': 8.0,      # Career 10.5 K/9
    'Logan Gilbert': 7.0,    # Career ~8.5 K/9
    'Andrew Painter': 7.5,   # Elite prospect K rate
    'Cade Cavalli': 7.0,     # High K stuff
    'Michael King': 7.0,     # Career ~8.5 K/9
    'Spencer Arrighetti': 7.5,# High K rate
    'Max McLean': 6.5,       # Developing arm
    'Kyle Harrison': 7.0,    # High K lefty
    'Corbin Burnes': 7.5,    # Career 10.0 K/9
    'Zack Wheeler': 7.5,     # Career 9.3 K/9
    'Brock Burke': 5.5,      # Lower tier but not 2
    'Luis Castillo': 7.5,    # Career 9.7 K/9
    'Shane McClanahan': 8.0, # Career 10.5 K/9
    'Freddy Peralta': 8.0,   # Career 10.5 K/9
    'Kevin Gausman': 7.5,    # Career 9.5 K/9
    'Max Scherzer': 8.0,     # Career 10.6 K/9
    'Blake Snell': 8.0,      # Career 11.3 K/9
    'Ranger Suarez': 6.5,    # Moderate K arm
    'Seth Lugo': 6.0,        # Contact-oriented
    'Logan Webb': 5.5,       # Low K, high contact
    # V6.6.1 Additions — 2026-05-03 post-mortem
    'Jack Leiter': 7.0,      # 2026 K/9 9.08, SwStr% 13.4% — QE projected 1 K, actual 10
    'MacKenzie Gore': 8.5,   # Career 10.5 K/9
    'José Soriano': 8.0,     # 2026 K/9 11.67, elite stuff
    'Aaron Nola': 7.5,       # Career 8.6 K/9
    'Cristopher Sánchez': 7.0, # Emerging K arm
    'Gavin Williams': 8.0,   # Career 10+ K/9
    'Joey Cantillo': 7.5,    # High K lefty
    'Parker Messick': 7.5,   # Elite K rate
    'Nolan McLean': 8.5,     # 2026 K/9 12.65
    'Cam Schlittler': 8.0,   # 2026 K/9 11.7
    'Ryan Weathers': 7.5,    # 2026 K/9 11.1
    'Will Warren': 7.5,      # 2026 K/9 10.91
    'Chase Burns': 7.5,      # Elite K stuff
    'Braxton Ashcraft': 7.5, # 2026 K/9 10.49
    'Jacob Misiorowski': 9.0,# 2026 K/9 14.14, elite
    'Robbie Ray': 7.5,       # Career 10.4 K/9
    'Garrett Crochet': 7.5,  # Career 10+ K/9
    'Michael Soroka': 7.5,   # 2026 K/9 11.25
    'Nathan Eovaldi': 6.5,   # Career 8.3 K/9
    'Landen Roupp': 7.5,     # 2026 K/9 10.26
    'Chase Dollander': 7.5,  # 2026 K/9 11.4
    'Yoshinobu Yamamoto': 8.0, # Elite NPB transition
    # V6.7 Additions — 5/5 forensic audit misses
    'Bryce Elder': 6.5,       # 5/5: pred 5 actual 9 — model sandbagged
    'Eduardo Rodriguez': 7.0, # 5/5: pred 3 actual 7 (ARI) — name collision issue
    'Taj Bradley': 7.5,       # 5/5: pred 5 actual 8 — emerging K arm
    'Brayan Bello': 6.5,      # 5/5: pred 3 actual 7 — model severely undershot
    'Sam Aldegheri': 4.0,     # 5/5: pred 5 actual 0 — ROOKIE with no floor
    'Bubba Chandler': 5.5,    # 5/5: close but add floor
    'Framber Valdez': 5.5,    # Volatile but career K arm
    'Sandy Alcantara': 5.5,   # Comeback season, lower K rate
    'Stephen Kolek': 5.0,     # Developing arm
    'Erick Fedde': 5.0,       # Contact pitcher, low floor
    'Andre Pallante': 4.5,    # Contact-first
    'Brandon Sproat': 6.0,    # Developing K arm
    'Andrew Abbott': 7.0,     # 2026 K/9 ~9.5
    'Jameson Taillon': 5.5,   # Career moderate K
    'Peter Lambert': 5.5,     # Contact-leaning
    'Drew Rasmussen': 6.0,    # Pre-injury K profile
    'Walker Buehler': 7.0,    # Career 10.5 K/9, post-injury regression
    'Logan Webb': 5.0,        # Low-K ground ball pitcher (confirmed 5/5)
    'George Kirby': 6.5,      # Career 8.0 K/9
    'Luis Severino': 6.0,     # Career 9.4 K/9
    # V20.0 Additions — 5/10 forensic audit misses
    'Davis Martin': 7.0,       # 2026 K/9 8.36, actual 9 Ks on 5/10
    'Tyler Mahle': 6.0,         # Post-injury, still has K stuff
    'Logan Henderson': 6.0,     # MIL emerging arm
    'Carlos Rodon': 7.5,        # Career 10.0 K/9
    'Payton Tolle': 5.5,        # Developing arm
    'Nick Martinez': 5.5,       # Career 7.5 K/9
    'Noah Cameron': 5.5,        # Developing arm, actual 10 Ks on 5/10
    'Drew Anderson': 5.0,       # Contact-leaning
    'Kyle Leahy': 5.0,          # Contact-leaning rookie
    'David Peterson': 5.0,      # Career ~7.5 K/9
    'Tomoyuki Sugano': 4.5,     # Contact-first NPB veteran
    'Chris Bassitt': 6.0,       # Career 8.5 K/9
    'Andrew Morris': 4.0,       # Rookie, minimal track record
    'Jose Soriano': 8.0,        # 2026 K/9 11.67, elite stuff
    'Eric Lauer': 6.0,          # Career 8.0 K/9
    'Cody Bolton': 5.5,         # Developing arm
    'Matthew Liberatore': 7.5,  # 5/13: Pred 3 actual 5. Floor prevents under-proj on velo jump.
    'J.T. Ginn': 5.5,           # 5/13: Sinker heavy, moderate K floor.
}

CATCHER_TIERS = {
    'Patrick Bailey': 1.18,  # God tier framing (+3% V20 boost)
    'Alejandro Kirk': 1.12,
    'Austin Wells': 1.12,
    'Cal Raleigh': 1.10,     # The Architect
    'Will Smith': 1.06,
    'Dillon Dingler': 1.15,
    'Danny Jansen': 1.02,
    'Gabriel Moreno': 1.08,  # V20 Addition
    'Francisco Alvarez': 1.05,# V20 Addition
    'Edgar Quero': 0.82,     # Leakage (-3% V20 nerf)
    'Drake Baldwin': 1.05,   # Tier 2
    'Hunter Goodman': 0.82,  # Tier 4
}

# ── 1. CORE DATA PARSING & PLATOON LOGIC ────────────────────────
import datetime

def get_month_weights(stat_type, current_month):
    """
    Returns weights (w26, w25, wCar) for blending based on the framework.
    stat_type: 'ERA', 'FIP', 'P_K', 'P_BB', 'H_AVG', 'H_wOBA', 'H_ISO', 'H_K_BB', 'Velocity'
    """
    if current_month <= 4:
        if stat_type == 'ERA': return (0.05, 0.45, 0.50)
        elif stat_type == 'FIP': return (0.10, 0.45, 0.45)
        elif stat_type == 'P_K_BB': return (0.25, 0.40, 0.35)
        elif stat_type == 'HR_FB': return (0.10, 0.45, 0.45)
        elif stat_type == 'H_AVG': return (0.05, 0.50, 0.45)
        elif stat_type == 'H_wOBA': return (0.10, 0.45, 0.45)
        elif stat_type == 'H_ISO': return (0.10, 0.45, 0.45)
        elif stat_type == 'H_K_BB': return (0.25, 0.40, 0.35)
        elif stat_type == 'Velocity': return (0.80, 0.15, 0.05)
    elif current_month == 5:
        if stat_type == 'ERA': return (0.15, 0.40, 0.45)
        elif stat_type == 'FIP': return (0.25, 0.40, 0.35)
        elif stat_type == 'P_K_BB': return (0.40, 0.35, 0.25)
        elif stat_type == 'HR_FB': return (0.20, 0.40, 0.40)
        elif stat_type == 'H_AVG': return (0.10, 0.45, 0.45)
        elif stat_type == 'H_wOBA': return (0.15, 0.45, 0.40)
        elif stat_type == 'H_ISO': return (0.20, 0.40, 0.40)
        elif stat_type == 'H_K_BB': return (0.40, 0.35, 0.25)
        elif stat_type == 'Velocity': return (0.75, 0.15, 0.10)
    elif current_month == 6:
        if stat_type == 'ERA': return (0.25, 0.40, 0.35)
        elif stat_type == 'FIP': return (0.40, 0.35, 0.25)
        elif stat_type == 'P_K_BB': return (0.55, 0.30, 0.15)
        elif stat_type == 'HR_FB': return (0.35, 0.35, 0.30)
        elif stat_type == 'H_AVG': return (0.25, 0.40, 0.35)
        elif stat_type == 'H_wOBA': return (0.30, 0.40, 0.30)
        elif stat_type == 'H_ISO': return (0.35, 0.35, 0.30)
        elif stat_type == 'H_K_BB': return (0.55, 0.30, 0.15)
        elif stat_type == 'Velocity': return (0.60, 0.25, 0.15)
    elif current_month == 7:
        if stat_type == 'ERA': return (0.40, 0.35, 0.25)
        elif stat_type == 'FIP': return (0.55, 0.30, 0.15)
        elif stat_type == 'P_K_BB': return (0.70, 0.20, 0.10)
        elif stat_type == 'HR_FB': return (0.55, 0.30, 0.15)
        elif stat_type == 'H_AVG': return (0.40, 0.35, 0.25)
        elif stat_type == 'H_wOBA': return (0.45, 0.35, 0.20)
        elif stat_type == 'H_ISO': return (0.50, 0.30, 0.20)
        elif stat_type == 'H_K_BB': return (0.70, 0.20, 0.10)
        elif stat_type == 'Velocity': return (0.60, 0.25, 0.15)
    elif current_month == 8:
        if stat_type == 'ERA': return (0.60, 0.28, 0.12)
        elif stat_type == 'FIP': return (0.70, 0.22, 0.08)
        elif stat_type == 'P_K_BB': return (0.80, 0.15, 0.05)
        elif stat_type == 'HR_FB': return (0.70, 0.20, 0.10)
        elif stat_type == 'H_AVG': return (0.55, 0.30, 0.15)
        elif stat_type == 'H_wOBA': return (0.60, 0.28, 0.12)
        elif stat_type == 'H_ISO': return (0.65, 0.25, 0.10)
        elif stat_type == 'H_K_BB': return (0.80, 0.15, 0.05)
        elif stat_type == 'Velocity': return (0.65, 0.25, 0.10)
    else:
        if stat_type == 'ERA': return (0.75, 0.18, 0.07)
        elif stat_type == 'FIP': return (0.80, 0.15, 0.05)
        elif stat_type == 'P_K_BB': return (0.85, 0.10, 0.05)
        elif stat_type == 'HR_FB': return (0.80, 0.15, 0.05)
        elif stat_type == 'H_AVG': return (0.70, 0.20, 0.10)
        elif stat_type == 'H_wOBA': return (0.75, 0.18, 0.07)
        elif stat_type == 'H_ISO': return (0.78, 0.15, 0.07)
        elif stat_type == 'H_K_BB': return (0.85, 0.10, 0.05)
        elif stat_type == 'Velocity': return (0.70, 0.20, 0.10)
    return (0.33, 0.33, 0.34)

def apply_blending(val26, val25, valCar, w26, w25, wCar, league_avg):
    if valCar is None and val25 is None:
        return (w26 * val26) + ((1.0 - w26) * league_avg)
    elif valCar is None:
        total_w = w26 + w25
        return (w26/total_w * val26) + (w25/total_w * val25)
    elif val25 is None:
        total_w = w26 + wCar
        return (w26/total_w * val26) + (wCar/total_w * valCar)
    else:
        return (w26 * val26) + (w25 * val25) + (wCar * valCar)

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
                    current_section = fv
                    if fv not in sections: sections[fv] = []
                    headers = []
                    continue
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

def get_lineup_wrc(lineup_names, team, sections, opposing_sp_hand=None, sections_25=None, sections_car=None):
    def fetch_stats(sec):
        if not sec: return []
        if opposing_sp_hand == 'L' and 'Batting Splits LHP' in sec:
            return sec['Batting Splits LHP']
        elif opposing_sp_hand == 'R' and 'Batting Splits RHP' in sec:
            return sec['Batting Splits RHP']
        return sec.get('Batting Advanced', [])

    batters_26 = fetch_stats(sections)
    batters_25 = fetch_stats(sections_25) if sections_25 else []
    batters_car = fetch_stats(sections_car) if sections_car else []
    
    team_batters_26 = [b for b in batters_26 if b.get('Team') == team]
    team_batters_25 = [b for b in batters_25 if b.get('Team') == team]
    team_batters_car = [b for b in batters_car if b.get('Team') == team]

    wrc_key = 'wRC+ wRC+ - Runs per PA scaled where 100 is average; both league and park adjusted; based on wOBA'
    k_key = 'K% K% - Strikeouts per plate appearance'

    wrcs = []
    k_pcts = []
    
    current_month = datetime.datetime.now().month

    for name, hand in lineup_names:
        match_26 = fuzzy_find(name, team_batters_26) or fuzzy_find(name, batters_26)
        match_25 = fuzzy_find(name, team_batters_25) or fuzzy_find(name, batters_25)
        match_car = fuzzy_find(name, team_batters_car) or fuzzy_find(name, batters_car)

        # Fallback to Advanced if not found in splits
        if not match_26 and (opposing_sp_hand == 'L' or opposing_sp_hand == 'R'):
            adv_26 = sections.get('Batting Advanced', [])
            match_26 = fuzzy_find(name, [b for b in adv_26 if b.get('Team') == team]) or fuzzy_find(name, adv_26)
        if not match_25 and (opposing_sp_hand == 'L' or opposing_sp_hand == 'R') and sections_25:
            adv_25 = sections_25.get('Batting Advanced', [])
            match_25 = fuzzy_find(name, [b for b in adv_25 if b.get('Team') == team]) or fuzzy_find(name, adv_25)
        if not match_car and (opposing_sp_hand == 'L' or opposing_sp_hand == 'R') and sections_car:
            adv_car = sections_car.get('Batting Advanced', [])
            match_car = fuzzy_find(name, [b for b in adv_car if b.get('Team') == team]) or fuzzy_find(name, adv_car)

        # Base stats
        wrc_26 = to_float(match_26.get(wrc_key) or match_26.get('wRC+'), 100.0) if match_26 else 100.0
        k_26 = to_float(match_26.get(k_key) or match_26.get('K%'), 22.0) if match_26 else 22.0

        wrc_25 = to_float(match_25.get(wrc_key) or match_25.get('wRC+'), None) if match_25 else None
        k_25 = to_float(match_25.get(k_key) or match_25.get('K%'), None) if match_25 else None

        wrc_car = to_float(match_car.get(wrc_key) or match_car.get('wRC+'), None) if match_car else None
        k_car = to_float(match_car.get(k_key) or match_car.get('K%'), None) if match_car else None

        # Framework Blending
        wrc_w26, wrc_w25, wrc_wCar = get_month_weights('H_wOBA', current_month)
        k_w26, k_w25, k_wCar = get_month_weights('H_K_BB', current_month)

        final_wrc = apply_blending(wrc_26, wrc_25, wrc_car, wrc_w26, wrc_w25, wrc_wCar, 100.0)
        final_k = apply_blending(k_26, k_25, k_car, k_w26, k_w25, k_wCar, 22.0)

        wrcs.append(final_wrc)
        k_pcts.append(final_k)
    
    avg_wrc = sum(wrcs) / len(wrcs) if wrcs else 100.0
    avg_k = sum(k_pcts) / len(k_pcts) if k_pcts else 22.0
    top4_wrc = sum(wrcs[:4]) / min(len(wrcs), 4) if wrcs else 100.0
    return avg_wrc, avg_k, top4_wrc

def to_float(val, default=0.0):
    if val is None: return default
    if isinstance(val, str):
        val = val.strip().strip('%')
        if not val: return default
    try:
        return float(val)
    except:
        return default

def get_pitcher_stats(name, team, sections, sections_25=None, sections_car=None):
    pitchers_26 = sections.get('Pitching Advanced', [])
    team_p = [p for p in pitchers_26 if p.get('Team') == team]
    p_26 = fuzzy_find(name, team_p) or fuzzy_find(name, pitchers_26)
    
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
    ip_key = 'IP IP - Innings Pitched'
    hh_key = 'HardHit% HardHit% -  Percentage of batted balls with exit velocity of 95 mph or higher'
    br_key = 'Barrel% Barrel% - Percentage of batted balls that are classified as barrels'
    xera_key = 'xERA xERA - Expected ERA'
    
    if p_26:
        stats['xFIP'] = to_float(p_26.get(xfip_key) or p_26.get('xFIP'), 4.15)
        stats['IP'] = to_float(p_26.get(ip_key) or p_26.get('IP'), 15.0)
        stats['K/9'] = to_float(p_26.get(k9_key) or p_26.get('K/9'), 8.5)
        stats['K_pct'] = to_float(p_26.get('K%'), 22.0)
        
    if stuff_p:
        val = stuff_p.get('Stuff+ Stuff+ - Model based pitching metric where 100 is average') or stuff_p.get('Stuff+')
        stats['Stuff'] = to_float(val, 100.0)
        stats['Stuff+'] = stats['Stuff']
        
    if sc_p:
        stats['HardHit%'] = to_float(sc_p.get(hh_key) or sc_p.get('HardHit%'), 38.0)
        stats['Barrel%'] = to_float(sc_p.get(br_key) or sc_p.get('Barrel%'), 7.5)
        stats['xERA'] = to_float(sc_p.get(xera_key) or sc_p.get('xERA'), 4.15)
    # Framework Blending
    current_month = datetime.datetime.now().month
    fip_w26, fip_w25, fip_wCar = get_month_weights('FIP', current_month)
    k_w26, k_w25, k_wCar = get_month_weights('P_K_BB', current_month)
    hrfb_w26, hrfb_w25, hrfb_wCar = get_month_weights('HR_FB', current_month)

    # Fetch 2025 and Career stats if available
    xfip_25 = k9_25 = kpct_25 = hh_25 = br_25 = xera_25 = hrfb_25 = None
    if sections_25:
        pitchers_25 = sections_25.get('Pitching Advanced', [])
        p_25 = fuzzy_find(name, [p for p in pitchers_25 if p.get('Team') == team]) or fuzzy_find(name, pitchers_25)
        sc_p_25 = fuzzy_find(name, sections_25.get('Pitching Statcast', []))
        if p_25:
            xfip_25 = to_float(p_25.get(xfip_key) or p_25.get('xFIP'), 4.15)
            k9_25 = to_float(p_25.get(k9_key) or p_25.get('K/9'), 8.5)
            kpct_25 = to_float(p_25.get('K%'), 22.0)
            hrfb_25 = to_float(p_25.get('HR/FB') or p_25.get('HR/FB%'), 12.0)
        if sc_p_25:
            hh_25 = to_float(sc_p_25.get(hh_key) or sc_p_25.get('HardHit%'), 38.0)
            br_25 = to_float(sc_p_25.get(br_key) or sc_p_25.get('Barrel%'), 7.5)
            xera_25 = to_float(sc_p_25.get(xera_key) or sc_p_25.get('xERA'), 4.15)

    xfip_car = k9_car = kpct_car = hrfb_car = None
    if sections_car:
        pitchers_car = sections_car.get('Pitching Advanced', [])
        p_car = fuzzy_find(name, [p for p in pitchers_car if p.get('Team') == team]) or fuzzy_find(name, pitchers_car)
        if p_car:
            xfip_car = to_float(p_car.get(xfip_key) or p_car.get('xFIP'), 4.15)
            k9_car = to_float(p_car.get(k9_key) or p_car.get('K/9'), 8.5)
            kpct_car = to_float(p_car.get('K%'), 22.0)
            hrfb_car = to_float(p_car.get('HR/FB') or p_car.get('HR/FB%'), 12.0)

    # 2026 HR/FB
    hrfb_26 = to_float(p_26.get('HR/FB') or p_26.get('HR/FB%'), 12.0) if p_26 else 12.0

    # Apply blending
    stats['xFIP'] = apply_blending(stats['xFIP'], xfip_25, xfip_car, fip_w26, fip_w25, fip_wCar, 4.15)
    stats['K/9'] = apply_blending(stats['K/9'], k9_25, k9_car, k_w26, k_w25, k_wCar, 8.5)
    stats['K_pct'] = apply_blending(stats.get('K_pct', 22.0), kpct_25, kpct_car, k_w26, k_w25, k_wCar, 22.0)
    stats['HR/FB'] = apply_blending(hrfb_26, hrfb_25, hrfb_car, hrfb_w26, hrfb_w25, hrfb_wCar, 12.0)
    
    # We use the FIP weights for advanced metrics like HardHit, Barrel, xERA
    stats['HardHit%'] = apply_blending(stats['HardHit%'], hh_25, None, fip_w26, fip_w25, fip_wCar, 38.0)
    stats['Barrel%'] = apply_blending(stats['Barrel%'], br_25, None, fip_w26, fip_w25, fip_wCar, 7.5)
    stats['xERA'] = apply_blending(stats['xERA'], xera_25, None, fip_w26, fip_w25, fip_wCar, 4.15)

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
        return {'A': 3.50, 'B': 5.00, 'C': 6.00, 'AVG': 4.15}
        
    xfips.sort()
    a_team = xfips[:2] if len(xfips) >= 2 else xfips
    b_team = xfips[-3:] if len(xfips) >= 3 else xfips
    c_team = xfips[-2:] if len(xfips) >= 2 else xfips
    
    return {
        'A': sum(a_team)/len(a_team),
        'B': sum(b_team)/len(b_team),
        'C': sum(c_team)/len(c_team),  # Removed artificial 1.30x blowout multiplier
        'AVG': sum(xfips)/len(xfips)
    }

def bayesian_era_v6_4(stats, era_26, recent_3_era=None):
    """V6.7: Added recent_3_era parameter for Fix 6."""
    xfip = stats['xFIP']
    ip = stats['IP']
    xera = stats['xERA']
    hh_pct = stats['HardHit%']
    barrel_pct = stats['Barrel%']
    
    w26 = min(0.45, ip / 50.0)
    sc_mod = 1.0
    if hh_pct > 42.0: sc_mod += (hh_pct - 42.0) * 0.0075
    if barrel_pct > 10.0: sc_mod += (barrel_pct - 10.0) * 0.01
    
    # HR/FB% Modifier
    hrfb_pct = stats.get('HR/FB', 12.0)
    if hrfb_pct > 12.0: sc_mod += (hrfb_pct - 12.0) * 0.015
    elif hrfb_pct < 10.0: sc_mod -= (10.0 - hrfb_pct) * 0.01
    
    sc_mod = min(sc_mod, 1.15) # Shrinkage Cap
    
    # V6.6.2: Ace Decay Penalty
    if xfip > 4.50 and xera < xfip - 0.50:
        print(f"  [ACE DECAY] Pitcher has xFIP > 4.50 and outperforming xERA. Applying +0.75 ERA penalty.")
        sc_mod *= 1.15
        xfip += 0.75
    
    base_blended = (1-w26)*xfip + w26*era_26
    
    # Fix 6: Weight recent 3-start ERA at 60% if available
    if recent_3_era is not None:
        base_blended = recent_3_era * 0.60 + base_blended * 0.40
        print(f"  [V6.7 RECENT FORM] Blending recent 3-start ERA ({recent_3_era:.2f}) at 60% weight")
    
    final_era = (base_blended * 0.7 + xera * 0.3) * sc_mod
    
    return max(1.50, min(final_era, 9.50))

def calc_expected_ip(blended_era, opp_wrc, manager_hook=0.0, base_ip=5.5):
    era_penalty = (blended_era - 4.0) * 0.5
    wrc_penalty = (opp_wrc - 100.0) * 0.02
    ip = base_ip - era_penalty - wrc_penalty + manager_hook
    return max(2.5, min(ip, 7.0))

# ── 3. MATH DISTRIBUTION GENERATORS ─────────────────────────────

def stochastic_event_count(lam):
    if lam <= 0: return 0
    if lam > 500: return max(0, int(random.gauss(lam, math.sqrt(lam))))
    L = math.exp(-lam); k=0; p=1.0
    while p > L: k+=1; p*=random.random()
    return k-1

def nbinom_rvs(n, mu):
    if mu <= 0: return 0
    p = n / (n + mu)
    return stochastic_event_count(random.gammavariate(n, (1.0-p)/p))

def calculate_yrfi_probability(away_sp_era, home_sp_era, away_top4_wrc, home_top4_wrc, env_factor):
    """
    Calculate the probability of a run in the first inning (YRFI).
    Uses a 100,000-iteration Monte Carlo simulation of the 1st inning
    to derive probability empirically.
    """
    # 1st Inning Multiplier: Accounts for pitcher settling in and top-of-order stress
    FIRST_INNING_MOD = 1.15
    
    # lambda_A1: Away runs in Top 1st (vs Home SP)
    # lambda_H1: Home runs in Bottom 1st (vs Away SP)
    lambda_A1 = (home_sp_era / 9.0) * (away_top4_wrc / 100.0) * env_factor * FIRST_INNING_MOD
    lambda_H1 = (away_sp_era / 9.0) * (home_top4_wrc / 100.0) * env_factor * FIRST_INNING_MOD
    
    nrfi_count = 0
    sims = 100000
    for _ in range(sims):
        top_runs = stochastic_event_count(lambda_A1)
        if top_runs > 0:
            continue
        bot_runs = stochastic_event_count(lambda_H1)
        if bot_runs == 0:
            nrfi_count += 1
            
    p_nrfi = nrfi_count / sims
    return (1.0 - p_nrfi) * 100.0

# ── 4. STATE ENGINE SIMULATOR ───────────────────────────────────

def simulate_game_v6_5(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                       away_wrc, home_wrc, env_factor, rain_intensity=0, runs_to_blowout=6,
                       away_drs=0, home_drs=0, umpire_zone='neutral',
                       away_lineup_k=22.7, home_lineup_k=22.7):
    
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
    # V20.0 Fix 1: Tighten NB shape parameter to reduce fat-tail total inflation
    # Old: sp_k = 20.0. New: 35.0 baseline, 50.0 for ace duels.
    is_ace_duel = away_sp_stats.get('Blended', 4.0) < 3.50 and home_sp_stats.get('Blended', 4.0) < 3.50
    sp_k = 50.0 if is_ace_duel else 35.0
    if rain_intensity > 0.4: sp_k = max(20.0, sp_k - 10.0)

    for i in range(N_SIMS):
        # V16.3: Amplify BABIP Variance
        babip_luck_h = random.gauss(1.0, 0.15)
        babip_luck_a = random.gauss(1.0, 0.15)
        
        # Batting Simulations
        h_sp_runs = nbinom_rvs(sp_k, home_sp_mu * babip_luck_h)
        a_sp_runs = nbinom_rvs(sp_k, away_sp_mu * babip_luck_a)
        
        # V16.3: Baseball Entropy Coefficient (Tail-Risk)
        if random.random() < 0.04:
            if random.random() < 0.5:
                h_sp_runs += stochastic_event_count(3.0)
            else:
                a_sp_runs += stochastic_event_count(3.0)
                
        actual_h_ip = home_sp_stats['Exp_IP']
        
        # Chapter 9.2: Laboring Inefficiency Check
        est_ppi = 15.0 + ((h_sp_runs * 2.2) / max(1.0, home_sp_stats['Exp_IP'])) + (home_sp_stats['K/9'] * 0.4)
        if est_ppi > 19.5:
            labor_mod = (est_ppi - 19.5) * 0.4
            actual_h_ip = max(2.0, actual_h_ip - labor_mod)

        if h_sp_runs >= 5 or est_ppi > 22:
            # V20.1 Calibration: Softened hook (0.5 vs 0.8) to allow for "inning eaters"
            actual_h_ip = max(0.5, actual_h_ip - (h_sp_runs - 2)*0.5) 
        elif h_sp_runs >= 3:
            # V20.1 Calibration: Softened hook (0.3 vs 0.5)
            actual_h_ip = max(1.0, actual_h_ip - (h_sp_runs - 2)*0.3)
        elif h_sp_runs <= 1:
            actual_h_ip = min(8.0, actual_h_ip + 1.0) # Cruising Bonus
        elif h_sp_runs == 2:
            actual_h_ip = min(7.0, actual_h_ip + 0.5)
        if random.random() < 0.02:
            actual_h_ip = random.uniform(0.1, 2.0); h_sp_runs += stochastic_event_count(2.0)
        
        bp_innings = 9.0 - actual_h_ip
        if h_sp_runs >= runs_to_blowout or actual_h_ip < 4.0:
            tm = 1.10 if actual_h_ip < 4.0 else 1.0
            h_bp_mu = (home_bp['C'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty * tm * home_drs_dampener * umpire_run_mod
        elif actual_h_ip < home_sp_stats['Exp_IP']:
            h_bp_mu = (home_bp['B'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty * home_drs_dampener * umpire_run_mod
        else:
            h_bp_mu = (home_bp['A'] / 9.0) * bp_innings * (away_wrc/100.0) * env_factor * rain_grip_penalty * home_drs_dampener * umpire_run_mod
        
        # V16.3: Leverage Stress Factor
        if abs(h_sp_runs - a_sp_runs) <= 1:
            h_bp_mu *= 1.15
            
        a_runs = h_sp_runs + stochastic_event_count(h_bp_mu)
        
        actual_a_ip = away_sp_stats['Exp_IP']
        
        # Chapter 9.2: Laboring Inefficiency Check
        # Estimate pitch count based on runs and expected K rate
        est_ppi = 15.0 + ((a_sp_runs * 2.2) / max(1.0, away_sp_stats['Exp_IP'])) + (away_sp_stats['K/9'] * 0.4)
        if est_ppi > 19.5:
            labor_mod = (est_ppi - 19.5) * 0.4
            actual_a_ip = max(2.0, actual_a_ip - labor_mod)

        if a_sp_runs >= 5 or est_ppi > 22:
            # V20.1 Calibration: Softened hook (0.5 vs 0.8)
            actual_a_ip = max(0.5, actual_a_ip - (a_sp_runs - 2)*0.5) 
        elif a_sp_runs >= 3:
            # V20.1 Calibration: Softened hook (0.3 vs 0.5)
            actual_a_ip = max(1.0, actual_a_ip - (a_sp_runs - 2)*0.3)
        elif a_sp_runs <= 1:
            actual_a_ip = min(8.0, actual_a_ip + 1.0) # Cruising Bonus
        elif a_sp_runs == 2:
            actual_a_ip = min(7.0, actual_a_ip + 0.5)
        if random.random() < 0.02:
            actual_a_ip = random.uniform(0.1, 2.0); a_sp_runs += stochastic_event_count(2.0)
            
        bp_innings = 9.0 - actual_a_ip
        if a_sp_runs >= runs_to_blowout or actual_a_ip < 4.0:
            tm = 1.10 if actual_a_ip < 4.0 else 1.0
            a_bp_mu = (away_bp['C'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty * tm * away_drs_dampener * umpire_run_mod
        elif actual_a_ip < away_sp_stats['Exp_IP']:
            a_bp_mu = (away_bp['B'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty * away_drs_dampener * umpire_run_mod
        else:
            a_bp_mu = (away_bp['A'] / 9.0) * bp_innings * (home_wrc/100.0) * env_factor * rain_grip_penalty * away_drs_dampener * umpire_run_mod
        
        # V16.3: Leverage Stress Factor
        if abs(h_sp_runs - a_sp_runs) <= 1:
            a_bp_mu *= 1.15
            
        h_runs = a_sp_runs + stochastic_event_count(a_bp_mu)

        away_total_runs.append(a_runs); home_total_runs.append(h_runs)
        
        # K-Alpha V1.0: Calibrated with Umpire Zone & Run Penalty
        # V20.1 Calibration: Added stochastic form multiplier to widen distribution
        run_penalty_a = 1.0
        if a_sp_runs >= 5: run_penalty_a = 0.95
        elif a_sp_runs >= 3: run_penalty_a = 0.98
        
        raw_a_k_prob = calculate_odds_ratio_k(away_sp_stats['K_pct'], home_lineup_k, 22.7, away_sp_stats.get('Stuff', 100))
        a_k_prob = raw_a_k_prob * umpire_k_mod * run_penalty_a * random.gauss(1.0, 0.15)
        
        # Mean K per sim iteration = Prob * Batters Faced
        # Est Batters Faced = IP * 3.8 + Runs (approx) + Variance
        est_bf_a = (actual_a_ip * 3.8) + a_sp_runs + random.uniform(-1.5, 1.5)
        raw_a_k_mu = max(0.01, a_k_prob * est_bf_a)
        away_sp_k_dist.append(stochastic_event_count(raw_a_k_mu))
        
        run_penalty_h = 1.0
        if h_sp_runs >= 5: run_penalty_h = 0.95
        elif h_sp_runs >= 3: run_penalty_h = 0.98
        
        raw_h_k_prob = calculate_odds_ratio_k(home_sp_stats['K_pct'], away_lineup_k, 22.7, home_sp_stats.get('Stuff', 100))
        h_k_prob = raw_h_k_prob * umpire_k_mod * run_penalty_h * random.gauss(1.0, 0.15)
        
        est_bf_h = (actual_h_ip * 3.8) + h_sp_runs + random.uniform(-1.5, 1.5)
        raw_h_k_mu = max(0.01, h_k_prob * est_bf_h)
        home_sp_k_dist.append(stochastic_event_count(raw_h_k_mu))
        
    return away_total_runs, home_total_runs, away_sp_k_dist, home_sp_k_dist

def calculate_odds_ratio_k(p_k_pct, l_k_pct, lg_avg_k=22.7, stuff_plus=100):
    """K-Alpha V1.0: Uses Log-Odds Ratio for K projection."""
    # Convert pct (0-100) to ratio (0-1)
    p = max(0.05, min(0.50, p_k_pct / 100.0))
    l = max(0.05, min(0.50, l_k_pct / 100.0))
    avg = lg_avg_k / 100.0
    
    # Pitcher/League odds
    p_odds = p / (1 - p)
    avg_odds = avg / (1 - avg)
    p_factor = p_odds / avg_odds
    
    # Lineup/League odds
    l_odds = l / (1 - l)
    l_factor = l_odds / avg_odds
    
    # Combined odds
    # V20.1 Calibration: Increased Lineup Factor weight from 40% to 55% for contact-heavy matchups.
    # 5/13 Lesson: Suppressors (Wetherholt/Burleson) had high contact impact on Ginn's K/BF.
    l_factor_dampened = (l_factor * 0.55) + 0.45 
    combined_odds = p_factor * l_factor_dampened * avg_odds
    
    # Adjust for Stuff+
    stuff_mod = 1.0 + ((stuff_plus - 100) * 0.008)
    combined_odds *= stuff_mod
    
    # Convert back to probability
    return combined_odds / (1 + combined_odds)

def run_v6_6_protocol(away_team, home_team, away_sp_name, home_sp_name,
                      away_sp_hand, home_sp_hand, away_era, home_era,
                      away_lineup, home_lineup, park_factor, is_dome, temp_f, wind_mph, wind_ang=90, 
                      humidity=50, altitude=0, rain_intensity=0,
                      away_drs=0, home_drs=0, away_manager_hook=0.0, home_manager_hook=0.0,
                      away_bp_pitches_d1=0, away_bp_pitches_d2=0, home_bp_pitches_d1=0, home_bp_pitches_d2=0,
                      umpire_zone='neutral', away_catcher='MISSING', home_catcher='MISSING', game_time='19:00',
                      vegas_total=None, away_recent_3_era=None, home_recent_3_era=None,
                      away_7day_wrc=None, home_7day_wrc=None,
                      away_lineup_k=22.7, home_lineup_k=22.7):
    
    # V6.6: Auto-run calibration check
    cal_total_mod = 0.0
    cal_k9_mod = 1.0
    if HAS_CALIBRATION:
        try:
            cal = run_calibration_check()
            cal_total_mod = cal.get('total_modifier', 0.0)
            cal_k9_mod = cal.get('k9_modifier', 1.0)
            print(f"  [V6.6 CALIBRATION] Total Modifier: {cal_total_mod:+.2f} | K/9 Modifier: {cal_k9_mod:.3f}x")
        except Exception as e:
            print(f"  [V6.6 CALIBRATION] Failed: {e}. Using defaults.")
    
    sections = parse_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats'))
    sections_25 = parse_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats 2025')) if os.path.exists(os.path.join(ROOT_DIR, 'data', 'MLB Stats 2025')) else None
    sections_car = parse_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats Career.csv')) if os.path.exists(os.path.join(ROOT_DIR, 'data', 'MLB Stats Career.csv')) else None
    
    if sections_25:
        print("  [V6.7 FRAMEWORK] MLB Stats 2025 file found.")
    if sections_car:
        print("  [V6.7 FRAMEWORK] MLB Stats Career file found. Applying Month-by-Month blending.")

    away_sp_stats = get_pitcher_stats(away_sp_name, away_team, sections, sections_25, sections_car)
    home_sp_stats = get_pitcher_stats(home_sp_name, home_team, sections, sections_25, sections_car)
    
    # V6.6: Enforce career K/9 floors BEFORE any modifiers
    away_floor = CAREER_K9_FLOORS.get(away_sp_name)
    home_floor = CAREER_K9_FLOORS.get(home_sp_name)
    if away_floor and away_sp_stats['K/9'] < away_floor:
        print(f"  [V6.6 K-FLOOR] {away_sp_name}: K/9 {away_sp_stats['K/9']:.1f} → floored to {away_floor}")
        away_sp_stats['K/9'] = away_floor
    if home_floor and home_sp_stats['K/9'] < home_floor:
        print(f"  [V6.6 K-FLOOR] {home_sp_name}: K/9 {home_sp_stats['K/9']:.1f} → floored to {home_floor}")
        home_sp_stats['K/9'] = home_floor
    
    away_sp_stats['Blended'] = bayesian_era_v6_4(away_sp_stats, away_era, recent_3_era=away_recent_3_era)
    home_sp_stats['Blended'] = bayesian_era_v6_4(home_sp_stats, home_era, recent_3_era=home_recent_3_era)
    
    # Fix 6: Apply 7-day offensive momentum if available
    away_wrc, away_k_pct, away_top4_wrc = get_lineup_wrc(away_lineup, away_team, sections, home_sp_hand, sections_25, sections_car)
    home_wrc, home_k_pct, home_top4_wrc = get_lineup_wrc(home_lineup, home_team, sections, away_sp_hand, sections_25, sections_car)
    
    if away_7day_wrc is not None:
        away_wrc = away_wrc * 0.50 + away_7day_wrc * 0.50
        print(f"  [V6.7 MOMENTUM] {away_team} 7-day wRC+ {away_7day_wrc:.0f} blended → {away_wrc:.1f}")
    if home_7day_wrc is not None:
        home_wrc = home_wrc * 0.50 + home_7day_wrc * 0.50
        print(f"  [V6.7 MOMENTUM] {home_team} 7-day wRC+ {home_7day_wrc:.0f} blended → {home_wrc:.1f}")
    
    away_sp_stats['Exp_IP'] = calc_expected_ip(away_sp_stats['Blended'], home_wrc, manager_hook=away_manager_hook)
    home_sp_stats['Exp_IP'] = calc_expected_ip(home_sp_stats['Blended'], away_wrc, manager_hook=home_manager_hook)
    
    away_bp = get_bullpen_tiers(away_team, away_sp_name, sections)
    home_bp = get_bullpen_tiers(home_team, home_sp_name, sections)
    
    print(f"  [DEBUG] {away_team} Bullpen: {away_bp}")
    print(f"  [DEBUG] {home_team} Bullpen: {home_bp}")
    
    # Bullpen Fatigue Downgrade (V16.3 Compounded Usage)
    away_bp_usage = (away_bp_pitches_d1 * 1.5) + (away_bp_pitches_d2 * 0.75)
    if away_bp_usage > 30:
        away_bp['A'] = away_bp['B']
        away_bp['B'] = away_bp['C']
    
    home_bp_usage = (home_bp_pitches_d1 * 1.5) + (home_bp_pitches_d2 * 0.75)
    if home_bp_usage > 30:
        home_bp['A'] = home_bp['B']
        home_bp['B'] = home_bp['C']
    
    pf = park_factor / 100.0
    t_adj = 1.0 if is_dome else 1.0 + ((temp_f - 72) * 0.0015) # Increased from 0.0008
    eff_wind = 0 if is_dome else wind_mph * math.cos(math.radians(wind_ang))
    w_adj = 1.0 + (eff_wind * 0.005)
    # V20 Upgrade: Exponential ADI (Air Density Index)
    # Humidity effect is non-linear (Magnus effect reduction at high humidity)
    # Pressure/Altitude effect is also exponential
    h_adj = 1.0 + (math.exp((humidity - 50) * 0.015) - 1.0) * 0.02
    alt_adj = math.exp(altitude / 10000.0) # ~10% boost at 1000ft
    
    # V20.1 Crosswind Drag Correction:
    # A strong crosswind (90 deg) disrupts both ball flight and pitch movement.
    crosswind_drag = 1.0
    if not is_dome and wind_mph > 12:
        crosswind_component = abs(math.sin(math.radians(wind_ang)))
        crosswind_drag = 1.0 - (wind_mph * crosswind_component * 0.002)
            
    env_factor = pf * t_adj * w_adj * h_adj * alt_adj * crosswind_drag * (1.0 - rain_intensity*0.035)
    
    # V16.3: Environmental Dampener (Totals Conflict)
    is_shootout = (env_factor > 1.05) or (away_sp_stats['Blended'] > 4.5) or (home_sp_stats['Blended'] > 4.5) or (away_bp_usage > 60) or (home_bp_usage > 60)
    if not is_shootout:
        print(f"  [V16.3 TOTALS DAMPENER] Standard environment detected. Applying 0.90x dampener to suppress over-optimistic totals.")
        env_factor *= 0.90
    
    # V6.6.2: Playoff Atmosphere Dampener
    if away_wrc > 110 and home_wrc > 110 and away_sp_stats['Blended'] < 3.50 and home_sp_stats['Blended'] < 3.50:
        print(f"  [PLAYOFF ATMOSPHERE] Elite Offenses vs Elite Pitching detected. Applying 0.80x dampener to env_factor to suppress blowout shootouts.")
        env_factor *= 0.80
        
    print(f"  [DEBUG] Env Factor: {env_factor:.3f} (PF:{pf} T:{t_adj:.3f} W:{w_adj:.3f} H:{h_adj:.3f} Alt:{alt_adj:.3f})")
    print(f"  [DEBUG] {away_team}: Blended ERA {away_sp_stats['Blended']:.2f}, wRC+ {away_wrc:.1f}, K% {away_k_pct:.1f}%, Exp IP {away_sp_stats['Exp_IP']:.2f}")
    print(f"  [DEBUG] {home_team}: Blended ERA {home_sp_stats['Blended']:.2f}, wRC+ {home_wrc:.1f}, K% {home_k_pct:.1f}%, Exp IP {home_sp_stats['Exp_IP']:.2f}")
    
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

    # Update K/9 with Bible modifiers + V6.6 calibration
    away_sp_stats['K/9'] *= away_arch_mod * away_cadj * shadow_boost * cal_k9_mod
    home_sp_stats['K/9'] *= home_arch_mod * home_cadj * shadow_boost * cal_k9_mod
    
    # V6.6.2: Opponent K% Modifier (fixing systematic under-projection bias)
    if home_k_pct > 24.0:
        print(f"  [K% OVERRIDE] {home_team} strikes out {home_k_pct:.1f}% of the time. Boosting {away_sp_name} baseline by +1.5 K/9.")
        away_sp_stats['K/9'] += 1.5
    if away_k_pct > 24.0:
        print(f"  [K% OVERRIDE] {away_team} strikes out {away_k_pct:.1f}% of the time. Boosting {home_sp_name} baseline by +1.5 K/9.")
        home_sp_stats['K/9'] += 1.5
    
    # V6.6.1: Apply calibration total modifier to env_factor
    # Increased from 0.06 to 0.10 — model was overshooting 80% of games
    # with only a 3% env reduction. Need 5%+ to meaningfully correct.
    if cal_total_mod != 0.0:
        env_factor *= (1.0 + (cal_total_mod * 0.05))
        print(f"  [V6.6.1 CALIBRATION] Env factor adjusted by cal_total_mod: {cal_total_mod:+.2f}")
    
    # Calculate YRFI Probability using the new forensic model
    # Ballpark lookup (mapping from PF or team name if needed, but here we assume we can pass the name)
    # Since we don't always have the ballpark name in the protocol, we'll try to infer it or pass it.
    # For now, we'll use a mapping or just pass the home team's default park.
    TEAM_PARK_MAPPING = {
        'PHI': 'Citizens Bank Park', 'COL': 'Coors Field', 'LAD': 'Dodger Stadium', 'HOU': 'Minute Maid Park',
        'NYY': 'Yankee Stadium', 'BOS': 'Fenway Park', 'SEA': 'T-Mobile Park', 'ATL': 'Truist Park',
        'MIL': 'American Family Field', 'ARI': 'Chase Field', 'BAL': 'Camden Yards', 'KC': 'Kauffman Stadium',
        'PIT': 'PNC Park', 'STL': 'Busch Stadium', 'CWS': 'Guaranteed Rate Field', 'MIN': 'Target Field',
        'TB': 'Tropicana Field', 'MIA': 'loanDepot Park', 'WSH': 'Nationals Park', 'CLE': 'Progressive Field',
        'DET': 'Comerica Park', 'LAA': 'Angel Stadium', 'OAK': 'Oakland Coliseum', 'TOR': 'Rogers Centre',
        'NYM': 'Citi Field', 'CIN': 'Great American Ball Park', 'SF': 'Oracle Park', 'SD': 'Petco Park',
        'TEX': 'Globe Life Field', 'CHC': 'Wrigley Field'
    }
    ballpark_name = TEAM_PARK_MAPPING.get(home_team, 'Sahlen Field')
    
    # Calculate YRFI Probability using the new V2.0 Data-Driven model
    game_input = yrfi.GameInput(
        home_team=home_team,
        away_team=away_team,
        home_pitcher=home_sp_name,
        away_pitcher=away_sp_name,
        ballpark=ballpark_name,
        home_lineup=[x[0] for x in home_lineup],
        away_lineup=[x[0] for x in away_lineup]
    )
    try:
        yrfi_pred = yrfi.predict_game(game_input, env_factor=env_factor, umpire_zone=umpire_zone)
        yrfi_prob = yrfi_pred.yrfi_prob * 100.0
    except Exception as e:
        print(f"  [YRFI V2.0 ERROR] Could not calculate YRFI prob: {e}")
        yrfi_prob = 50.0
    
    ar, hr, a_k, h_k = simulate_game_v6_5(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                                          away_wrc, home_wrc, env_factor, rain_intensity, 6,
                                          away_drs, home_drs, umpire_zone,
                                          away_lineup_k=away_lineup_k, home_lineup_k=home_lineup_k)
                                         
    n = len(ar)
    tr = [ar[i]+hr[i] for i in range(n)]
    aw = sum(1 for i in range(n) if ar[i]>hr[i]); hw = sum(1 for i in range(n) if hr[i]>ar[i]); ties = n-aw-hw
    apct = (aw + ties*0.48)/n*100; hpct = (hw + ties*0.52)/n*100
    raw_away_mu = sum(ar)/n; raw_home_mu = sum(hr)/n; raw_total_mu = sum(tr)/n
    ak_mean = sum(a_k)/n; hk_mean = sum(h_k)/n
    ak_med = statistics.median(a_k); hk_med = statistics.median(h_k)
    blowout_prob = sum(1 for r in tr if r > 13) / n * 100
    
    # V6.6: Vegas Total Blending
    if vegas_total is not None:
        # V20.0 Fix 2: Rebalance from 65/35 to 50/50 — model overshoots 80% of games
        blended_total = raw_total_mu * 0.50 + vegas_total * 0.50
        scale = blended_total / raw_total_mu if raw_total_mu > 0 else 1.0
        away_mu = raw_away_mu * scale
        home_mu = raw_home_mu * scale
        total_mu = blended_total
        print(f"  [V20.0 VEGAS ANCHOR] Raw total: {raw_total_mu:.2f} -> Blended: {total_mu:.2f} (Vegas: {vegas_total})")
    else:
        away_mu = raw_away_mu
        home_mu = raw_home_mu
        total_mu = raw_total_mu
    
    run_diff = abs(away_mu - home_mu)

    print(f"+------------------------------------------------------------------+")
    print(f"|        MLB QUANT-ELITE V6.7 | POST-AUDIT ENGINE              |")
    print(f"|        {away_team} @ {home_team} | DETERMINISTIC STATE ENGINE         |")
    print(f"+------------------------------------------------------------------+\n")
    print(f"-- 1. STATE ENGINE EXPECTANCY ({N_SIMS:,} SIMS) -------------------")
    print(f"  {away_team}: {away_mu:.3f} runs  |  {home_team}: {home_mu:.3f} runs")
    print(f"  TOTAL: {total_mu:.3f} runs")
    if vegas_total:
        print(f"  RAW (pre-anchor): {raw_total_mu:.3f} runs")
    print(f"  WIN PROBABILITY: {away_team} {apct:.1f}% | {home_team} {hpct:.1f}%")
    print(f"  YRFI PROBABILITY: {yrfi_prob:.1f}%")
    print(f"  BLOWOUT PROBABILITY (>13 RUNS): {blowout_prob:.1f}%")
    
    print(f"\n-- 2. PITCHER PROP PROJECTIONS ------------------------------------")
    print(f"  {away_sp_name} - {ak_mean:.2f} K's - Final Prediction: {int(ak_med)} K's")
    print(f"  {home_sp_name} - {hk_mean:.2f} K's - Final Prediction: {int(hk_med)} K's")
    
    print(f"\n-- 3. BETTING INTELLIGENCE FLAGS ----------------------------------")
    if int(ak_med) > ak_mean + 0.5 or (ak_med >= 6 and (ak_med - ak_mean) > -0.2):
        print(f"  [VOLATILITY WARNING] {away_sp_name} projected for high K's but carries early-hook tail risk.")
    if int(hk_med) > hk_mean + 0.5 or (hk_med >= 6 and (hk_med - hk_mean) > -0.2):
        print(f"  [VOLATILITY WARNING] {home_sp_name} projected for high K's but carries early-hook tail risk.")

    # V6.6: VEGAS EDGE DETECTOR
    if vegas_total is not None:
        edge = total_mu - vegas_total
        edge_abs = abs(edge)
        direction = "OVER" if edge > 0 else "UNDER"
        if edge_abs >= 2.0:
            print(f"  [!!! BIG EDGE] Model {total_mu:.1f} vs Vegas {vegas_total} -> {direction} by {edge_abs:.1f} runs. HIGH-CONVICTION {direction}.")
        elif edge_abs >= 1.0:
            print(f"  [EDGE] Model {total_mu:.1f} vs Vegas {vegas_total} -> {direction} by {edge_abs:.1f} runs.")
        else:
            print(f"  [-] Model {total_mu:.1f} vs Vegas {vegas_total} -> No significant edge ({direction} {edge_abs:.1f}).")
        # Calibration caveat: warn if model has active over-prediction bias
        if cal_total_mod < -0.3 and edge > 1.0:
            print(f"  [⚠ CALIBRATION NOTE] Model has active over-prediction bias ({cal_total_mod:+.2f}). Over edge may be inflated — size accordingly.")

    if run_diff < 0.5:
        print(f"  [WARNING] Run Diff {run_diff:.2f} < 0.5. TOSS-UP: FADE MONEYLINE.")
        print(f"  [ACTION] Focus on Game Totals or Pitcher Unders.")
    elif run_diff >= 1.4:
        fav = away_team if away_mu > home_mu else home_team
        print(f"  [EDGE DETECTED] Run Diff {run_diff:.2f} >= 1.4. MASSIVE EDGE: CONSIDER RUNLINE (-1.5) FOR {fav}.")
    else:
        fav = away_team if away_mu > home_mu else home_team
        print(f"  [EDGE DETECTED] Run Diff {run_diff:.2f}. CONSIDER MONEYLINE FOR {fav}.")

    print(f"==================================================================")
    print(f"  V6.6 FINAL: {away_team} {away_mu:.2f} - {home_team} {home_mu:.2f} | YRFI: {yrfi_prob:.1f}%")
    print(f"==================================================================")
    
    return ar, hr, a_k, h_k, yrfi_prob

# Backwards compatibility alias
run_v6_5_protocol = run_v6_6_protocol

if __name__ == '__main__':
    # Test LAA @ KC
    laa_lineup = [('Neto', 'R'), ('Trout', 'R'), ('Adell', 'R'), ('Soler', 'R'), ('Peraza', 'R'), ('Schanuel', 'L'), ('Grissom', 'R'), ('O\'Hoppe', 'R'), ('Teodosio', 'R')]
    kcr_lineup = [('Garcia', 'R'), ('Witt', 'R'), ('Pasquantino', 'L'), ('Perez', 'R'), ('Jensen', 'L'), ('Massey', 'L'), ('Caglianone', 'L'), ('Collins', 'S'), ('Isbel', 'L')]
    run_v6_6_protocol('LAA', 'KCR', 'Walbert Urena', 'Cole Ragans', 'R', 'L',
                      2.35, 6.00, laa_lineup, kcr_lineup, 101, False, 62, 9, 60, 50, 912, 0.0,
                      vegas_total=7.5)