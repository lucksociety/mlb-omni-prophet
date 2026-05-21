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
QUANT-ELITE V5.0 — SINGLE GAME PROTOCOL
STL @ MIA | April 22, 2026 | 12:10 PM ET
CONFIRMED LINEUPS + UMPIRE + DOME
"""
import csv, random, math
from collections import Counter
import datetime

random.seed(2026_04_22)
N_SIMS = 100000

# ── CONFIRMED DATA FROM SCREENSHOT ──────────────────────────────

AWAY = 'STL'
HOME = 'MIA'
AWAY_SP = 'Kyle Leahy'
HOME_SP = 'Janson Junk'
AWAY_SP_ERA = 5.21
HOME_SP_ERA = 4.50

# CONFIRMED LINEUPS (name, hand)
STL_LINEUP = [
    ('J.J. Wetherholt', 'L'), ('Ivan Herrera', 'R'), ('Nolan Gorman', 'L'),
    ('Ramon Urias', 'R'), ('Jose Fermin', 'R'), ('Nathan Church', 'L'),
    ('Thomas Saggese', 'R'), ('Pedro Pages', 'R'), ('Victor Scott', 'L'),
]
MIA_LINEUP = [
    ('Jakob Marsee', 'L'), ('Xavier Edwards', 'S'), ('Otto Lopez', 'R'),
    ('Liam Hicks', 'L'), ('Agustin Ramirez', 'R'), ('Harold Hernandez', 'R'),
    ('Owen Caissie', 'L'), ('Leo Jimenez', 'R'), ('Jose Sanoja', 'R'),
]

# Umpire: Jacob Metz — 8.0 R/G (league avg ~8.5), 18.0 K/G (high)
# 8.0/8.5 = 0.941 → slightly suppresses runs
UMPIRE_RUN_MULT = 8.0 / 8.5

# Dome — no weather effect
PARK_FACTOR = 95  # loanDepot Park (pitcher-friendly)
IS_DOME = True
TEMP_F = 75
WIND_MPH = 0

# Vegas: MIA -143, O/U 8.0

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
    away_wrc = get_lineup_wrc(STL_LINEUP, AWAY, sections)
    home_wrc = get_lineup_wrc(MIA_LINEUP, HOME, sections)
    
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
    env = pf  # Dome: no wind/temp adjustment
    
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
    print(f"║        {AWAY} @ {HOME} | {datetime.datetime.now().strftime('%B %d, %Y')} | 12:10 PM ET          ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    print(f"\n── 1. DATA VERIFICATION ─────────────────────────────────────────")
    print(f"  Lineups:      ● CONFIRMED (Both Teams)")
    print(f"  Starters:     ● CONFIRMED")
    print(f"  Umpire:       Jacob Metz | 8.0 R/G (−5.9% vs avg) | 18.0 K/G (HIGH)")
    print(f"  Venue:        loanDepot Park | DOME (roof closed)")
    print(f"  Park Factor:  {PARK_FACTOR} (pitcher-friendly)")
    print(f"  Vegas Line:   MIA −143 | O/U 8.0")
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
    for name, hand in STL_LINEUP:
        print(f"    {hand} {name}")
    print(f"\n  {HOME} Confirmed wRC+: {home_wrc:.1f}")
    for name, hand in MIA_LINEUP:
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
    
    # Implied odds comparison
    vegas_home_pct = 143.0 / (143.0 + 100.0) * 100  # -143 implied
    model_diff = hpct - vegas_home_pct
    print(f"\n  Vegas Implied:  MIA {vegas_home_pct:.1f}%")
    print(f"  Model:          MIA {hpct:.1f}%")
    if abs(model_diff) > 3:
        direction = "OVER" if model_diff > 0 else "UNDER"
        print(f"  ⚡ MODEL {direction}VALUES MIA by {abs(model_diff):.1f}pp vs Vegas")
    else:
        print(f"  ≈ Model aligns with Vegas (within 3pp)")
    
    rl_away = sum(1 for i in range(n) if ar[i]-hr[i]>1.5)/n*100
    rl_home = sum(1 for i in range(n) if hr[i]-ar[i]>1.5)/n*100
    print(f"\n  Run Line: {AWAY} −1.5 → {rl_away:.1f}%  |  {HOME} −1.5 → {rl_home:.1f}%")
    
    print(f"\n── 7. OVER/UNDER ANALYSIS ───────────────────────────────────────")
    print(f"  Vegas O/U: 8.0 | Model Total: {away_mu+home_mu:.2f}")
    for line in [6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]:
        over = sum(1 for t in tr if t > line)/n*100
        marker = " ◄ VEGAS LINE" if line == 8.0 else ""
        print(f"  O/U {line:5.1f}:  Over {over:5.1f}%  |  Under {100-over:5.1f}%{marker}")
    
    ou_edge = sum(1 for t in tr if t > 8.0)/n*100
    if ou_edge > 55:
        print(f"\n  ⚡ LEAN: OVER 8.0 ({ou_edge:.1f}% of sims)")
    elif ou_edge < 45:
        print(f"\n  ⚡ LEAN: UNDER 8.0 ({100-ou_edge:.1f}% of sims)")
    else:
        print(f"\n  ≈ O/U 8.0 is a coin flip ({ou_edge:.1f}% over)")
    
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
    if UMPIRE_RUN_MULT < 0.95:
        print(f"  ⚠ Umpire Metz suppresses runs (8.0 R/G vs 8.5 avg) → slight Under lean")
    if PARK_FACTOR < 98:
        print(f"  ⚠ loanDepot Park is pitcher-friendly (PF {PARK_FACTOR}) → supports Under")
    
    # Both SP are R, check lineup handedness
    stl_lefties = sum(1 for _,h in STL_LINEUP if h == 'L')
    mia_lefties = sum(1 for _,h in MIA_LINEUP if h in ('L','S'))
    print(f"  ℹ STL has {stl_lefties}/9 LHB vs RHP Junk")
    print(f"  ℹ MIA has {mia_lefties}/9 LHB/SHB vs RHP Leahy")
    
    print(f"\n{'='*66}")
    print(f"  FINAL PREDICTION:  {AWAY} {away_mu:.2f} — {HOME} {home_mu:.2f}")
    print(f"  TOTAL: {away_mu+home_mu:.2f}  |  WINNER: {fav} ({fav_pct:.0f}%)")
    print(f"{'='*66}")

if __name__ == '__main__':
    main()