#!/usr/bin/env python3
"""
QUANT-ELITE V5.0 — SINGLE GAME PROTOCOL
HOU @ CLE | April 22, 2026 | 1:10 PM ET
CONFIRMED LINEUPS
"""
import csv, random, math
from collections import Counter
import datetime

random.seed(2026_04_22_2)
N_SIMS = 100000

# ── CONFIRMED DATA FROM SCREENSHOT ──────────────────────────────

AWAY = 'HOU'
HOME = 'CLE'
AWAY_SP = 'Peter Lambert'
HOME_SP = 'Tanner Bibee'
AWAY_SP_ERA = 7.20
HOME_SP_ERA = 4.81

# CONFIRMED LINEUPS (name, hand)
HOU_LINEUP = [
    ('Carlos Correa', 'R'), ('Yordan Alvarez', 'L'), ('Jose Altuve', 'R'),
    ('Christian Walker', 'R'), ('Isaac Paredes', 'R'), ('Cam Smith', 'R'),
    ('Dominic Johnson', 'L'), ('Christian Vazquez', 'R'), ('Brice Matthews', 'R'), # Guessed some first names from common knowledge or initials
]
# Let's actually use the initials for fuzzy matching if the full name fails.
# The fuzzy matcher looks for the last name.
HOU_LINEUP_INITIALS = [
    ('Correa', 'R'), ('Alvarez', 'L'), ('Altuve', 'R'),
    ('Walker', 'R'), ('Paredes', 'R'), ('Smith', 'R'),
    ('Johnson', 'L'), ('Vazquez', 'R'), ('Matthews', 'R'),
]

CLE_LINEUP_INITIALS = [
    ('Kwan', 'L'), ('DeLauter', 'L'), ('Ramirez', 'S'),
    ('Manzardo', 'L'), ('Valera', 'L'), ('Schneemann', 'L'),
    ('Brito', 'S'), ('Naylor', 'L'), ('Rocchio', 'S'),
]

# Umpire: Not provided in screenshot, assume neutral
UMPIRE_RUN_MULT = 1.0

# Weather/Park for CLE
PARK_FACTOR = 97  # Progressive Field
IS_DOME = False
TEMP_F = 58
WIND_MPH = 8
WIND_ANG = 90 # Neutral crosswind

# Vegas: Not provided

# ── ENGINE ──────────────────────────────────────────────────────

def parse_csv(filepath):
    sections = {}
    current_section = None
    headers = []
    with open(filepath, 'r') as f:
        for row in csv.reader(f):
            if not row or not any(row): continue
            fv = row[0].strip()
            if fv in ["Batting Advanced","Batting Stat Cast","Pitching Advanced","Pitching +","Pitching Statcast"]:
                current_section = fv; sections[fv] = []; headers = []; continue
            if current_section:
                if fv == '#' and not headers:
                    headers = [h.split()[0] if h.strip() else f'c{i}' for i,h in enumerate(row)]
                    continue
                if headers and fv != '#' and len(row) >= len(headers):
                    sections[current_section].append(dict(zip(headers, row[:len(headers)])))
    return sections

def fuzzy_find(name, players):
    name_l = name.lower()
    last = name_l.split()[-1]
    for p in players:
        pn = p.get('Name','').lower()
        if last in pn: return p
    return None

def get_lineup_wrc(lineup_names, team, sections):
    """Get actual wRC+ for confirmed lineup batters."""
    batters = sections.get('Batting Advanced', [])
    team_batters = [b for b in batters if b.get('Team') == team]
    all_batters = batters
    
    wrcs = []
    for name, hand in lineup_names:
        match = fuzzy_find(name, team_batters) or fuzzy_find(name, all_batters)
        if match:
            try:
                wrcs.append(float(match.get('wRC+', '100')))
            except: wrcs.append(95.0)  # Below avg for unmatched
        else:
            wrcs.append(85.0)  # Penalty for unknown hitters (likely weak bats)
    return sum(wrcs) / len(wrcs)

def get_sp(name, team, sections):
    pitchers = sections.get('Pitching Advanced', [])
    team_p = [p for p in pitchers if p.get('Team') == team]
    return fuzzy_find(name, team_p) or fuzzy_find(name, pitchers)

def get_stuff(name, sections):
    p = fuzzy_find(name, sections.get('Pitching +', []))
    if p:
        try: return float(p.get('Stuff+', '100'))
        except: pass
    return None

def get_bp_xfip(team, sp_name, sections):
    pitchers = [p for p in sections.get('Pitching Advanced', [])
                if p.get('Team') == team and p.get('Name','') != sp_name]
    xfips = []
    for p in pitchers:
        try: xfips.append(float(p.get('xFIP', '4.15')))
        except: pass
    return sum(xfips)/len(xfips) if xfips else 4.15

def bayesian_era(xfip, era_26, ip):
    if ip <= 0 or era_26 <= 0: return xfip * 0.7 + 4.15 * 0.3
    w26 = min(0.35, ip / 60.0)
    return max(1.50, min((1-w26)*xfip + w26*era_26, 8.00))

def stuff_mod(stuff):
    if stuff is None: return 1.0
    return 1.0 - ((stuff - 100) * 0.005)

def wind_adjustment(wind_speed, wind_angle, is_dome):
    if is_dome: return 1.0
    effective = wind_speed * math.cos(math.radians(wind_angle))
    return 1.0 + (effective * 0.004)

def temp_adjustment(temp_f, is_dome):
    if is_dome: return 1.0
    return 1.0 + ((temp_f - 72) * 0.0008)

def poisson_rvs(lam):
    if lam > 500: return max(0, int(random.gauss(lam, math.sqrt(lam))))
    L = math.exp(-lam); k=0; p=1.0
    while p > L: k+=1; p*=random.random()
    return k-1

def nbinom_rvs(n, p):
    return poisson_rvs(random.gammavariate(n, (1.0-p)/p))

def simulate(away_mu, home_mu, k=5.5, n=N_SIMS):
    ap = k/(k+away_mu); hp = k/(k+home_mu)
    return ([nbinom_rvs(k,ap) for _ in range(n)],
            [nbinom_rvs(k,hp) for _ in range(n)])

# ── MAIN ────────────────────────────────────────────────────────

def main():
    sections = parse_csv('MLB Stats')
    
    # Starter data
    away_sp = get_sp(AWAY_SP, AWAY, sections)
    home_sp = get_sp(HOME_SP, HOME, sections)
    
    away_xfip = float(away_sp.get('xFIP','4.15')) if away_sp else 4.15
    home_xfip = float(home_sp.get('xFIP','4.15')) if home_sp else 4.15
    away_ip = float(away_sp.get('IP','15')) if away_sp else 15.0
    home_ip = float(home_sp.get('IP','15')) if home_sp else 15.0
    away_siera = away_sp.get('SIERA','N/A') if away_sp else 'N/A'
    home_siera = home_sp.get('SIERA','N/A') if home_sp else 'N/A'
    away_kpct = away_sp.get('K%','N/A') if away_sp else 'N/A'
    home_kpct = home_sp.get('K%','N/A') if home_sp else 'N/A'
    
    away_blended = bayesian_era(away_xfip, AWAY_SP_ERA, away_ip)
    home_blended = bayesian_era(home_xfip, HOME_SP_ERA, home_ip)
    
    away_stuff = get_stuff(AWAY_SP, sections)
    home_stuff = get_stuff(HOME_SP, sections)
    
    # Confirmed lineup wRC+
    away_wrc = get_lineup_wrc(HOU_LINEUP_INITIALS, AWAY, sections)
    home_wrc = get_lineup_wrc(CLE_LINEUP_INITIALS, HOME, sections)
    
    # Bullpen
    away_bp = get_bp_xfip(AWAY, AWAY_SP, sections)
    home_bp = get_bp_xfip(HOME, HOME_SP, sections)
    
    # Projected IP
    away_proj_ip = 5.5 if away_blended < 4.0 else 5.0
    home_proj_ip = 5.5 if home_blended < 4.0 else 5.0
    
    # Full-game ERA
    away_fg = ((home_blended * home_proj_ip) + (home_bp * (9-home_proj_ip))) / 9.0
    home_fg = ((away_blended * away_proj_ip) + (away_bp * (9-away_proj_ip))) / 9.0
    
    # Environmental
    pf = PARK_FACTOR / 100.0
    w_adj = wind_adjustment(WIND_MPH, WIND_ANG, IS_DOME)
    t_adj = temp_adjustment(TEMP_F, IS_DOME)
    env = pf * w_adj * t_adj
    
    # Expected runs
    away_mu = away_fg * (away_wrc/100.0) * stuff_mod(home_stuff) * env * UMPIRE_RUN_MULT
    home_mu = home_fg * (home_wrc/100.0) * stuff_mod(away_stuff) * env * UMPIRE_RUN_MULT * 1.03
    
    away_mu = max(2.0, min(away_mu, 10.0))
    home_mu = max(2.0, min(home_mu, 10.0))
    
    # Simulate
    ar, hr = simulate(away_mu, home_mu)
    n = len(ar)
    tr = [ar[i]+hr[i] for i in range(n)]
    
    scores = Counter(zip(ar, hr))
    mode, mode_ct = scores.most_common(1)[0]
    
    aw = sum(1 for i in range(n) if ar[i]>hr[i])
    hw = sum(1 for i in range(n) if hr[i]>ar[i])
    ties = n-aw-hw
    apct = (aw + ties*0.48)/n*100
    hpct = (hw + ties*0.52)/n*100
    
    tmean = sum(tr)/n
    tstd = math.sqrt(sum((x-tmean)**2 for x in tr)/n)
    
    # ── REPORT ──────────────────────────────────────────────────
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║        MLB QUANT-ELITE V5.0 | GAME-DAY PRECISION PROTOCOL      ║")
    print(f"║        {AWAY} @ {HOME} | {datetime.datetime.now().strftime('%B %d, %Y')} | 1:10 PM ET          ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    print(f"\n── 1. DATA VERIFICATION ─────────────────────────────────────────")
    print(f"  Lineups:      ● CONFIRMED (Both Teams)")
    print(f"  Starters:     ● CONFIRMED")
    print(f"  Umpire:       Assumed Neutral | 8.5 R/G")
    print(f"  Venue:        Progressive Field")
    print(f"  Weather:      {TEMP_F}°F | {WIND_MPH}mph wind")
    print(f"  Park Factor:  {PARK_FACTOR} (slightly pitcher-friendly)")
    print(f"  Simulations:  {N_SIMS:,} iterations")
    
    print(f"\n── 2. STARTING PITCHER ANALYSIS ─────────────────────────────────")
    print(f"  ┌─ AWAY: {AWAY_SP} (R)")
    print(f"  │  2026 ERA:      {AWAY_SP_ERA:.2f}")
    print(f"  │  xFIP:          {away_xfip:.2f}")
    print(f"  │  SIERA:         {away_siera}")
    print(f"  │  Stuff+:        {away_stuff if away_stuff else 'N/A'}")
    print(f"  │  K%:            {away_kpct}")
    print(f"  │  Blended ERA:   {away_blended:.2f} (Bayesian @ {away_ip:.0f} IP)")
    print(f"  │  Proj IP:       {away_proj_ip:.1f}")
    print(f"  │")
    print(f"  └─ HOME: {HOME_SP} (R)")
    print(f"     2026 ERA:      {HOME_SP_ERA:.2f}")
    print(f"     xFIP:          {home_xfip:.2f}")
    print(f"     SIERA:         {home_siera}")
    print(f"     Stuff+:        {home_stuff if home_stuff else 'N/A'}")
    print(f"     K%:            {home_kpct}")
    print(f"     Blended ERA:   {home_blended:.2f} (Bayesian @ {home_ip:.0f} IP)")
    print(f"     Proj IP:       {home_proj_ip:.1f}")
    
    print(f"\n── 3. LINEUP STRENGTH ───────────────────────────────────────────")
    print(f"  {AWAY} Confirmed wRC+: {away_wrc:.1f}")
    for name, hand in HOU_LINEUP_INITIALS:
        print(f"    {hand} {name}")
    print(f"\n  {HOME} Confirmed wRC+: {home_wrc:.1f}")
    for name, hand in CLE_LINEUP_INITIALS:
        print(f"    {hand} {name}")
    
    print(f"\n  Bullpen xFIP: {AWAY} {away_bp:.2f} | {HOME} {home_bp:.2f}")
    
    print(f"\n── 4. MATHEMATICAL EXPECTANCY ({N_SIMS:,} SIMS) ─────────────────────")
    print(f"  ┌──────────────────────────────────────────────┐")
    print(f"  │  {AWAY}: {away_mu:.3f} runs  |  {HOME}: {home_mu:.3f} runs   │")
    print(f"  │  PROJECTED TOTAL: {away_mu+home_mu:.3f} runs              │")
    print(f"  └──────────────────────────────────────────────┘")
    
    print(f"\n── 5. SCORE DISTRIBUTION ────────────────────────────────────────")
    print(f"  MOST LIKELY FINAL:  {AWAY} {mode[0]} — {HOME} {mode[1]}  ({mode_ct/n*100:.1f}%)")
    for s, c in scores.most_common(6)[1:]:
        print(f"                      {AWAY} {s[0]} — {HOME} {s[1]}  ({c/n*100:.1f}%)")
    
    print(f"\n── 6. WIN PROBABILITY ───────────────────────────────────────────")
    fav = AWAY if apct > hpct else HOME
    dog = HOME if fav == AWAY else AWAY
    fav_pct = max(apct, hpct)
    dog_pct = min(apct, hpct)
    print(f"  {AWAY}: {apct:.1f}%  |  {HOME}: {hpct:.1f}%")
    print(f"  → EDGE: {fav} ({fav_pct:.1f}%)")
    
    rl_away = sum(1 for i in range(n) if ar[i]-hr[i]>1.5)/n*100
    rl_home = sum(1 for i in range(n) if hr[i]-ar[i]>1.5)/n*100
    print(f"\n  Run Line: {AWAY} −1.5 → {rl_away:.1f}%  |  {HOME} −1.5 → {rl_home:.1f}%")
    
    print(f"\n── 7. OVER/UNDER ANALYSIS ───────────────────────────────────────")
    print(f"  Model Total: {away_mu+home_mu:.2f}")
    for line in [6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]:
        over = sum(1 for t in tr if t > line)/n*100
        print(f"  O/U {line:5.1f}:  Over {over:5.1f}%  |  Under {100-over:5.1f}%")
    
    print(f"\n── 8. VOLATILITY & GAME SCRIPT ──────────────────────────────────")
    chaos = 'HIGH' if tstd > 3.8 else 'MODERATE' if tstd > 3.0 else 'LOW'
    p25 = sorted(tr)[int(n*0.25)]
    p75 = sorted(tr)[int(n*0.75)]
    print(f"  Std Dev:    {tstd:.2f} [{chaos}]")
    print(f"  IQR:        {p25}–{p75} total runs")
    print(f"  Pitchers Duel (≤4):  {sum(1 for t in tr if t<=4)/n*100:.1f}%")
    print(f"  Low (5-7):           {sum(1 for t in tr if 5<=t<=7)/n*100:.1f}%")
    print(f"  Average (8-10):      {sum(1 for t in tr if 8<=t<=10)/n*100:.1f}%")
    print(f"  Slugfest (≥11):      {sum(1 for t in tr if t>=11)/n*100:.1f}%")
    
    print(f"\n── 9. EDGE FLAGS ───────────────────────────────────────────────")
    if away_blended - away_xfip > 0.5:
        print(f"  ⚠ {AWAY_SP}: ERA ({AWAY_SP_ERA}) significantly above xFIP ({away_xfip:.2f}) → due for regression DOWN")
    if home_blended - home_xfip > 0.5:
        print(f"  ⚠ {HOME_SP}: ERA ({HOME_SP_ERA}) significantly above xFIP ({home_xfip:.2f}) → due for regression DOWN")
    if PARK_FACTOR < 98:
        print(f"  ⚠ Progressive Field is slightly pitcher-friendly (PF {PARK_FACTOR}) → supports Under")
    
    hou_lefties = sum(1 for _,h in HOU_LINEUP_INITIALS if h in ('L','S'))
    cle_lefties = sum(1 for _,h in CLE_LINEUP_INITIALS if h in ('L','S'))
    print(f"  ℹ HOU has {hou_lefties}/9 LHB/SHB vs RHP Bibee")
    print(f"  ℹ CLE has {cle_lefties}/9 LHB/SHB vs RHP Lambert")
    
    print(f"\n{'='*66}")
    print(f"  FINAL PREDICTION:  {AWAY} {away_mu:.2f} — {HOME} {home_mu:.2f}")
    print(f"  TOTAL: {away_mu+home_mu:.2f}  |  WINNER: {fav} ({fav_pct:.0f}%)")
    print(f"{'='*66}")

if __name__ == '__main__':
    main()
