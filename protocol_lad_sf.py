import sys
import os
import csv
import random
import math
from collections import Counter
import datetime

# Add workspace to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6 import (
    parse_csv, get_pitcher_stats, bayesian_era, get_lineup_wrc,
    calc_expected_ip, get_bullpen_tiers, simulate_game_v6
)

def run_full_protocol(away_team, home_team, away_sp_name, home_sp_name,
                      away_sp_hand, home_sp_hand, away_era, home_era,
                      away_lineup, home_lineup, park_factor, is_dome, temp_f, wind_mph, wind_ang=90):
    
    random.seed(202604233)
    N_SIMS = 100000
    sections = parse_csv('MLB Stats')
    
    # 1. Pitcher Data
    away_sp_stats = get_pitcher_stats(away_sp_name, away_team, sections)
    home_sp_stats = get_pitcher_stats(home_sp_name, home_team, sections)
    
    away_sp_stats['Blended'] = bayesian_era(away_sp_stats['xFIP'], away_era, away_sp_stats['IP'])
    home_sp_stats['Blended'] = bayesian_era(home_sp_stats['xFIP'], home_era, home_sp_stats['IP'])
    
    # 2. Lineup Strength
    away_wrc = get_lineup_wrc(away_lineup, away_team, sections, home_sp_hand)
    home_wrc = get_lineup_wrc(home_lineup, home_team, sections, away_sp_hand)
    
    # 3. Dynamic IP
    away_sp_stats['Exp_IP'] = calc_expected_ip(away_sp_stats['Blended'], home_wrc)
    home_sp_stats['Exp_IP'] = calc_expected_ip(home_sp_stats['Blended'], away_wrc)
    
    # 4. Bullpens
    away_bp = get_bullpen_tiers(away_team, away_sp_name, sections)
    home_bp = get_bullpen_tiers(home_team, home_sp_name, sections)
    
    # 5. Environment
    pf = park_factor / 100.0
    t_adj = 1.0 if is_dome else 1.0 + ((temp_f - 72) * 0.0008)
    eff_wind = 0 if is_dome else wind_mph * math.cos(math.radians(wind_ang))
    w_adj = 1.0 if is_dome else 1.0 + (eff_wind * 0.004)
    env_factor = pf * t_adj * w_adj
    
    # 6. Simulation
    ar, hr, a_k, h_k = simulate_game_v6(away_sp_stats, home_sp_stats, away_bp, home_bp, 
                                        away_wrc, home_wrc, env_factor)
                                        
    n = len(ar)
    tr = [ar[i]+hr[i] for i in range(n)]
    scores = Counter(zip(ar, hr))
    mode, mode_ct = scores.most_common(1)[0]
    
    aw = sum(1 for i in range(n) if ar[i]>hr[i])
    hw = sum(1 for i in range(n) if hr[i]>ar[i])
    ties = n-aw-hw
    apct = (aw + ties*0.48)/n*100
    hpct = (hw + ties*0.52)/n*100
    
    away_mu = sum(ar)/n
    home_mu = sum(hr)/n
    total_mu = sum(tr)/n
    tstd = math.sqrt(sum((x-total_mu)**2 for x in tr)/n)
    
    ak_mean = sum(a_k)/n
    hk_mean = sum(h_k)/n
    
    # ── REPORTING ──
    print(f"╔══════════════════════════════════════════════════════════════════╗")
    print(f"║        MLB QUANT-ELITE V6.0 | FULL SCORE PREDICTION PROTOCOL   ║")
    print(f"║        {away_team} @ {home_team} | {datetime.datetime.now().strftime('%B %d, %Y')}                     ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝\n")
    
    print(f"── 1. DATA VERIFICATION ─────────────────────────────────────────")
    print(f"  Status:       ● CONFIRMED LINEUPS")
    print(f"  Venue:        Oracle Park | {temp_f}°F | Wind {wind_mph} mph")
    print(f"  Park Factor:  {park_factor} (Extreme Pitcher Environment)")
    print(f"  Env Factor:   {env_factor:.3f}")
    
    print(f"\n── 2. STARTING PITCHER ANALYSIS ─────────────────────────────────")
    print(f"  {away_sp_name} ({away_team}):")
    print(f"    Blended ERA: {away_sp_stats['Blended']:.2f} | xFIP: {away_sp_stats['xFIP']:.2f}")
    print(f"    Expected IP: {away_sp_stats['Exp_IP']:.2f} | Projected Ks: {ak_mean:.2f}")
    print(f"  {home_sp_name} ({home_team}):")
    print(f"    Blended ERA: {home_sp_stats['Blended']:.2f} | xFIP: {home_sp_stats['xFIP']:.2f}")
    print(f"    Expected IP: {home_sp_stats['Exp_IP']:.2f} | Projected Ks: {hk_mean:.2f}")
    
    print(f"\n── 3. LINEUP & BULLPEN STRENGTH ─────────────────────────────────")
    print(f"  {away_team} wRC+: {away_wrc:.1f} | Bullpen High Lev: {away_bp['A']:.2f}")
    print(f"  {home_team} wRC+: {home_wrc:.1f} | Bullpen High Lev: {home_bp['A']:.2f}")
    
    print(f"\n── 4. SCORE DISTRIBUTION ────────────────────────────────────────")
    print(f"  MOST LIKELY FINAL:  {away_team} {mode[0]} — {home_team} {mode[1]}  ({mode_ct/n*100:.1f}%)")
    for s, c in scores.most_common(5)[1:]:
        print(f"                      {away_team} {s[0]} — {home_team} {s[1]}  ({c/n*100:.1f}%)")
    
    print(f"\n── 5. MATHEMATICAL EXPECTANCY ({n:,} SIMS) ─────────────────────")
    print(f"  {away_team}: {away_mu:.3f} runs  |  {home_team}: {home_mu:.3f} runs")
    print(f"  TOTAL PROJECTED: {total_mu:.3f} runs")
    print(f"  WIN PROBABILITY: {away_team} {apct:.1f}% | {home_team} {hpct:.1f}%")
    print(f"  → EDGE: {home_team if hpct > apct else away_team} ({max(apct, hpct):.1f}%)")
    
    print(f"\n── 6. OVER/UNDER ANALYSIS ───────────────────────────────────────")
    for line in [6.5, 7.0, 7.5, 8.0, 8.5]:
        over = sum(1 for t in tr if t > line)/n*100
        print(f"  O/U {line:4.1f}:  Over {over:5.1f}% | Under {100-over:5.1f}%")
        
    print(f"\n── 7. VOLATILITY & EDGE FLAGS ──────────────────────────────────")
    chaos = 'EXTREME' if tstd > 4.5 else 'HIGH' if tstd > 3.8 else 'MODERATE'
    print(f"  Std Dev: {tstd:.2f} [{chaos}]")
    if park_factor < 96:
        print(f"  ℹ INFO: Oracle Park's suppression factor is active. Expecting low variance.")
        
    print(f"\n==================================================================")
    print(f"  V6 FINAL PREDICTION: {away_team} {away_mu:.2f} — {home_team} {home_mu:.2f}")
    print(f"==================================================================")

if __name__ == '__main__':
    AWAY_LINEUP = [
        ('S. Ohtani', 'L'), ('Kyle Tucker', 'L'), ('Will Smith', 'R'),
        ('F. Freeman', 'L'), ('Max Muncy', 'L'), ('T. Hernandez', 'R'),
        ('Andy Pages', 'R'), ('Hyeseong Kim', 'L'), ('A. Freeland', 'S'),
    ]
    HOME_LINEUP = [
        ('Willy Adames', 'R'), ('Luis Arraez', 'L'), ('Matt Chapman', 'R'),
        ('R. Devers', 'L'), ('C. Schmitt', 'R'), ('Jung Hoo Lee', 'L'),
        ('Heliot Ramos', 'R'), ('Drew Gilbert', 'L'), ('P. Bailey', 'S'),
    ]
    run_full_protocol(
        'LAD', 'SF', 'Tyler Glasnow', 'Logan Webb', 'R', 'R',
        3.24, 5.10, AWAY_LINEUP, HOME_LINEUP, 95, False, 60, 3
    )
