import argparse
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

import os
import csv
import json, datetime, statistics
import unicodedata
from collections import defaultdict
from omni_prophet_v16 import OmniProphetV18
import quant_elite_v6_6 as qe

def normalize_name(name):
    if not name: return ""
    # Remove accents and convert to lowercase
    nfkd_form = unicodedata.normalize('NFKD', name)
    name = "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
    # Remove periods, commas, and common suffixes
    name = name.replace(".", "").replace(",", "")
    parts = name.split()
    suffixes = {'jr', 'sr', 'ii', 'iii', 'iv'}
    parts = [p for p in parts if p not in suffixes]
    return " ".join(parts).strip()

def parse_multi_csv(filepath):
    sections = {}
    current_section = None
    last_updated = None
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        headers = []
        for row in reader:
            if not row or not any(row): continue
            first_val = row[0].strip()
            
            if first_val.startswith('# LAST_UPDATED:'):
                try:
                    date_str = first_val.split(':')[1].strip()
                    last_updated = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                except:
                    pass
                continue
                
            cleaned_val = first_val.split(',')[0].strip()
            if cleaned_val in ["Batting Advanced", "Batting Stat Cast", "Pitching Advanced", "Pitching +", "Pitching Statcast"]:
                current_section = cleaned_val
                sections.setdefault(current_section, [])
                headers = []
                continue
            
            if current_section:
                if first_val == '#' and not headers:
                    headers = [h.split()[0] for h in row]
                    continue
                if headers and first_val != '#':
                    if len(row) >= len(headers):
                        row_dict = dict(zip(headers, row[:len(headers)]))
                        sections[current_section].append(row_dict)
    return sections, last_updated

def safe_float(val, default):
    try:
        return float(str(val).replace('%', '').strip() or default)
    except:
        return default

def get_pitcher_stats(sections, sections_25, sections_car, name):
    norm_search = normalize_name(name)
    current_month = datetime.datetime.now().month
    
    k_w26, k_w25, k_wCar = qe.get_month_weights('P_K_BB', current_month)
    fip_w26, fip_w25, fip_wCar = qe.get_month_weights('FIP', current_month)
    hr_w26, hr_w25, hr_wCar = qe.get_month_weights('HR_FB', current_month)

    def extract_stats(sec):
        if not sec: return None
        for p in sec.get('Pitching Advanced', []):
            p_name = p.get('Name', '').strip()
            if not p_name or p_name.lower() == 'name': continue
            norm_p = normalize_name(p_name)
            if norm_search in norm_p or norm_p in norm_search or norm_search.split()[-1] == norm_p.split()[-1]:
                k_pct = safe_float(p.get('K%', '20'), 20.0)
                bb_pct = safe_float(p.get('BB%', '8'), 8.0)
                era = safe_float(p.get('ERA', 4.0), 4.0)
                xfip = safe_float(p.get('xFIP', 4.0), 4.0)
                hrfb = safe_float(p.get('HR/FB', p.get('HR/FB%', '12')), 12.0)
                return {'Name': p_name, 'K%': k_pct, 'BB%': bb_pct, 'ERA': era, 'xFIP': xfip, 'HR/FB': hrfb}
        return None

    s26 = extract_stats(sections)
    if not s26: return None
    s25 = extract_stats(sections_25)
    sCar = extract_stats(sections_car)

    k_final = qe.apply_blending(s26['K%'], s25['K%'] if s25 else None, sCar['K%'] if sCar else None, k_w26, k_w25, k_wCar, 20.0)
    bb_final = qe.apply_blending(s26['BB%'], s25['BB%'] if s25 else None, sCar['BB%'] if sCar else None, k_w26, k_w25, k_wCar, 8.0)
    era_final = qe.apply_blending(s26['ERA'], s25['ERA'] if s25 else None, sCar['ERA'] if sCar else None, fip_w26, fip_w25, fip_wCar, 4.0)
    xfip_final = qe.apply_blending(s26['xFIP'], s25['xFIP'] if s25 else None, sCar['xFIP'] if sCar else None, fip_w26, fip_w25, fip_wCar, 4.0)
    hrfb_final = qe.apply_blending(s26['HR/FB'], s25['HR/FB'] if s25 else None, sCar['HR/FB'] if sCar else None, hr_w26, hr_w25, hr_wCar, 12.0)

    return {
        'Name': s26['Name'],
        'ERA': era_final,
        'xERA': xfip_final,
        'K_pct': k_final,
        'BB_pct': bb_final,
        'HR/FB%': hrfb_final,
        'IP': safe_float(s26.get('IP', 100), 100.0),
        'Starts': safe_float(s26.get('Starts', 10), 10.0),
        'Stuff': 100, 'VAA': -4.5
    }

def get_batter_stats(sections, sections_25, sections_car, name):
    norm_search = normalize_name(name)
    current_month = datetime.datetime.now().month
    k_w26, k_w25, k_wCar = qe.get_month_weights('H_K_BB', current_month)

    def extract_stats(sec):
        if not sec: return None
        for b in sec.get('Batting Advanced', []):
            b_name = b.get('Name', '').strip()
            if not b_name or b_name.lower() == 'name': continue
            norm_b = normalize_name(b_name)
            if norm_search in norm_b or norm_b in norm_search or norm_search.split()[-1] == norm_b.split()[-1]:
                return {
                    'Name': b_name, 
                    'K%': safe_float(b.get('K%', '22.7'), 22.7),
                    'wOBA': safe_float(b.get('wOBA', '0.320'), 0.320)
                }
        return None

    s26 = extract_stats(sections)
    if not s26: return None
    s25 = extract_stats(sections_25)
    sCar = extract_stats(sections_car)

    k_final = qe.apply_blending(s26['K%'], s25['K%'] if s25 else None, sCar['K%'] if sCar else None, k_w26, k_w25, k_wCar, 22.7)
    woba_final = qe.apply_blending(s26['wOBA'], s25['wOBA'] if s25 else None, sCar['wOBA'] if sCar else None, k_w26, k_w25, k_wCar, 0.320)

    return {
        'Name': s26['Name'],
        'K_pct': k_final,
        'wOBA': woba_final,
        'O_Swing': 30.0, 'Z_Contact': 85.0, 'Hand': 'R'
    }


def apply_overrides(name, override_list, is_pitcher):
    norm_search = normalize_name(name)
    for ov in override_list or []:
        parts = ov.split(':')
        norm_ov = normalize_name(parts[0])
        if norm_search in norm_ov or norm_ov in norm_search:
            if is_pitcher and len(parts) >= 5:
                return {
                    'Name': name,
                    'K_pct': float(parts[1].strip('%')),
                    'BB_pct': float(parts[2].strip('%')),
                    'ERA': float(parts[3]),
                    'xERA': float(parts[4]),
                    'HR/FB%': float(parts[5].strip('%')) if len(parts) >= 6 else 12.0,
                    'Starts': float(parts[6]) if len(parts) >= 7 else 10.0,
                    'IP': float(parts[7]) if len(parts) >= 8 else 100.0,
                    'Stuff': float(parts[8]) if len(parts) >= 9 else 100.0,
                    'VAA': -4.5
                }
            elif not is_pitcher and len(parts) >= 2:
                return {
                    'Name': name,
                    'K_pct': float(parts[1].strip('%')),
                    'wOBA': float(parts[2]) if len(parts) >= 3 else 0.320,
                    'Hand': parts[3] if len(parts) >= 4 else 'R',
                    'O_Swing': 30.0, 'Z_Contact': 85.0
                }
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--away', required=True)
    parser.add_argument('--home', required=True)
    parser.add_argument('--away_sp', required=True)
    parser.add_argument('--home_sp', required=True)
    parser.add_argument('--away_sp_hand', default='R', help="Pitcher handedness (R or L)")
    parser.add_argument('--home_sp_hand', default='R', help="Pitcher handedness (R or L)")
    parser.add_argument('--away_lineup', required=True, help="Comma separated list of 9 names")
    parser.add_argument('--home_lineup', required=True, help="Comma separated list of 9 names")
    parser.add_argument('--check_data', action='store_true', help="Only check for missing/stale data and return JSON")
    parser.add_argument('--override_sp', action='append', help="Format: Name:K%%:BB%%:ERA:xFIP")
    parser.add_argument('--override_batter', action='append', help="Format: Name:K%%")
    parser.add_argument('--save_overrides', action='store_true', help="Append overridden data to MLB Stats database")
    parser.add_argument('--odds', help="Comma separated market odds (e.g. 'LAD ML:-207,Total Over 8.5:-110')")
    # V17.1 Layer 6 Args
    parser.add_argument('--away_ivb', type=float, help="Away SP Induced Vertical Break")
    parser.add_argument('--home_ivb', type=float, help="Home SP Induced Vertical Break")
    parser.add_argument('--away_hb', type=float, help="Away SP Horizontal Break")
    parser.add_argument('--home_hb', type=float, help="Home SP Horizontal Break")
    parser.add_argument('--away_velo_delta', type=float, default=0.0)
    parser.add_argument('--home_velo_delta', type=float, default=0.0)
    parser.add_argument('--bullpen_burn', type=float, default=0.0, help="Team bullpen fatigue (0.0 to 1.0)")
    parser.add_argument('--game_time_decimal', type=float, help="Game time in decimal hours (e.g. 19.5 for 7:30 PM)")
    # V18 Args
    parser.add_argument('--away_woba_rank_14d', type=int, default=15)
    parser.add_argument('--home_woba_rank_14d', type=int, default=15)
    parser.add_argument('--away_sp_blowup_21d', action='store_true')
    parser.add_argument('--home_sp_blowup_21d', action='store_true')
    parser.add_argument('--away_sp_era_split_diff', type=float, default=0.0)
    parser.add_argument('--home_sp_era_split_diff', type=float, default=0.0)
    parser.add_argument('--away_contact_rank', type=int, default=15)
    parser.add_argument('--home_contact_rank', type=int, default=15)
    parser.add_argument('--away_sp_rest', type=int, default=5)
    parser.add_argument('--home_sp_rest', type=int, default=5)
    parser.add_argument('--away_sp_whip_4', type=float, default=1.25)
    parser.add_argument('--home_sp_whip_4', type=float, default=1.25)
    parser.add_argument('--away_sp_strong_home', action='store_true')
    parser.add_argument('--home_sp_strong_home', action='store_true')
    parser.add_argument('--away_sp_1st_era', type=float, default=4.0)
    parser.add_argument('--home_sp_1st_era', type=float, default=4.0)
    parser.add_argument('--away_1st_rank_30d', type=int, default=15)
    parser.add_argument('--home_1st_rank_30d', type=int, default=15)
    parser.add_argument('--away_1st_pct', type=float, default=0.30)
    parser.add_argument('--home_lineup_1st_pct_recent', type=float, default=0.30)
    parser.add_argument('--dome', action='store_true', help="Set if game is in a dome")
    parser.add_argument('--temp', type=float, default=72.0)
    parser.add_argument('--wind_speed', type=float, default=0.0)
    parser.add_argument('--wind_dir', type=int, default=0, help="0: None, 1: In, 2: Out, 3: L-R, 4: R-L")
    parser.add_argument('--umpire', default='Unknown')
    args = parser.parse_args()

    # --------------------------------------------------------------------------
    # DISTRIBUTION GUARDRAIL CHECK (V20.1 - WRITTEN IN STONE)
    # --------------------------------------------------------------------------
    if not args.check_data:
        print("\n[V20.1 CALIBRATION] Stochastic Volatility: ACTIVE (Chaos Injector Enabled)")
        print("[V20.1 CALIBRATION] Distribution Blur: ACTIVE (30% Smear Enabled)")
        print("[V20.1 CALIBRATION] Tail Preservation: ACTIVE (Overdispersion Enabled)")
    # --------------------------------------------------------------------------

    sections, last_updated = parse_multi_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats'))
    sections_25, _ = parse_multi_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats 2025')) if os.path.exists(os.path.join(ROOT_DIR, 'data', 'MLB Stats 2025')) else ({}, None)
    sections_car, _ = parse_multi_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats Career.csv')) if os.path.exists(os.path.join(ROOT_DIR, 'data', 'MLB Stats Career.csv')) else ({}, None)

    missing_pitchers = []
    missing_batters = []

    away_sp_data = apply_overrides(args.away_sp, args.override_sp, True) or get_pitcher_stats(sections, sections_25, sections_car, args.away_sp)
    if not away_sp_data: missing_pitchers.append(args.away_sp)

    home_sp_data = apply_overrides(args.home_sp, args.override_sp, True) or get_pitcher_stats(sections, sections_25, sections_car, args.home_sp)
    if not home_sp_data: missing_pitchers.append(args.home_sp)

    away_lineup_names = [n.strip() for n in args.away_lineup.split(',')]
    home_lineup_names = [n.strip() for n in args.home_lineup.split(',')]
    while len(away_lineup_names) < 9: away_lineup_names.append("Unknown")
    while len(home_lineup_names) < 9: home_lineup_names.append("Unknown")
    away_lineup_names = away_lineup_names[:9]
    home_lineup_names = home_lineup_names[:9]

    away_lineup_statcast = []
    for n in away_lineup_names:
        # Extract hand if present: "Name (L)"
        hand = 'R'
        clean_name = n
        if '(' in n and ')' in n:
            hand = n.split('(')[1].split(')')[0].upper()
            clean_name = n.split('(')[0].strip()
        
        stat = apply_overrides(clean_name, args.override_batter, False) or get_batter_stats(sections, sections_25, sections_car, clean_name)
        if not stat and clean_name != "Unknown": missing_batters.append(clean_name)
        
        entry = stat or {'Name': clean_name, 'K_pct': 22.7, 'wOBA': 0.320, 'O_Swing': 30.0, 'Z_Contact': 85.0}
        if 'Hand' not in entry or entry['Hand'] == 'R': entry['Hand'] = hand
        away_lineup_statcast.append(entry)

    home_lineup_statcast = []
    for n in home_lineup_names:
        hand = 'R'
        clean_name = n
        if '(' in n and ')' in n:
            hand = n.split('(')[1].split(')')[0].upper()
            clean_name = n.split('(')[0].strip()
            
        stat = apply_overrides(clean_name, args.override_batter, False) or get_batter_stats(sections, sections_25, sections_car, clean_name)
        if not stat and clean_name != "Unknown": missing_batters.append(clean_name)
        
        entry = stat or {'Name': clean_name, 'K_pct': 22.7, 'wOBA': 0.320, 'O_Swing': 30.0, 'Z_Contact': 85.0}
        if 'Hand' not in entry or entry['Hand'] == 'R': entry['Hand'] = hand
        home_lineup_statcast.append(entry)

    if args.check_data:
        days_stale = 0
        if last_updated:
            days_stale = (datetime.date.today() - last_updated).days
        else:
            days_stale = 999
        
        status = "OK"
        if missing_pitchers or missing_batters or days_stale > 2:
            status = "STALE_OR_MISSING"
        
        print(json.dumps({
            "status": status,
            "days_stale": days_stale,
            "missing_pitchers": missing_pitchers,
            "missing_batters": missing_batters
        }, indent=2))
        return

    # If not check_data, but there are missing players that weren't overridden, we proceed with defaults
    if not away_sp_data: away_sp_data = {'Name': args.away_sp, 'ERA': 4.0, 'xERA': 4.0, 'K_pct': 22.7, 'BB_pct': 8.5, 'HR/FB%': 12.0, 'IP': 100, 'Stuff': 100, 'VAA': -4.5}
    if not home_sp_data: home_sp_data = {'Name': args.home_sp, 'ERA': 4.0, 'xERA': 4.0, 'K_pct': 22.7, 'BB_pct': 8.5, 'HR/FB%': 12.0, 'IP': 100, 'Stuff': 100, 'VAA': -4.5}

    # V17.1: Inject Layer 6 Statcast data if provided
    if args.away_ivb: away_sp_data['IVB'] = args.away_ivb
    if args.home_ivb: home_sp_data['IVB'] = args.home_ivb
    if args.away_hb: away_sp_data['HB'] = args.away_hb
    if args.home_hb: home_sp_data['HB'] = args.home_hb
    away_sp_data['Velo_Delta'] = args.away_velo_delta
    home_sp_data['Velo_Delta'] = args.home_velo_delta

    game_data = {
        'away_team': args.away, 'home_team': args.home,
        'away_sp_name': away_sp_data['Name'], 'home_sp_name': home_sp_data['Name'],
        'away_sp_hand': args.away_sp_hand, 'home_sp_hand': args.home_sp_hand,
        'away_sp_era': away_sp_data['ERA'], 'home_sp_era': home_sp_data['ERA'],
        'away_sp_statcast': away_sp_data, 'home_sp_statcast': home_sp_data,
        'away_lineup_names': away_lineup_names, 'home_lineup_names': home_lineup_names,
        'away_lineup_hands': [b['Hand'] for b in away_lineup_statcast],
        'home_lineup_hands': [b['Hand'] for b in home_lineup_statcast],
        'away_lineup_statcast': away_lineup_statcast, 'home_lineup_statcast': home_lineup_statcast,
        'park_factor': 100, 'is_dome': args.dome,
        'location': args.home, 
        'game_time_decimal': args.game_time_decimal or 19.0,
        'game_time': f"{int(args.game_time_decimal or 19)}:00", # String for QE
        'bullpen_burn': args.bullpen_burn,
        'env': {'Weather': {'temp': args.temp, 'wind_speed': args.wind_speed, 'wind_dir': args.wind_dir, 'humidity': 50}, 'altitude': 0, 'rain_intensity': 0.0, 'Umpire': {'name': args.umpire, 'CS_pct': 16.5, 'zone_type': 'neutral'}},
        'away_drs': 0, 'home_drs': 0, 'away_manager_hook': 0.0, 'home_manager_hook': 0.0,
        'away_bp_pitches_d1': 0, 'away_bp_pitches_d2': 0, 'home_bp_pitches_d1': 0, 'home_bp_pitches_d2': 0,
        'away_catcher': 'Unknown', 'home_catcher': 'Unknown',
        # V18 Calibration
        'away_lineup_woba_rank_14d': args.away_woba_rank_14d,
        'home_lineup_woba_rank_14d': args.home_woba_rank_14d,
        'away_sp_blowup_21d': args.away_sp_blowup_21d,
        'home_sp_blowup_21d': args.home_sp_blowup_21d,
        'away_sp_era_split_diff': args.away_sp_era_split_diff,
        'home_sp_era_split_diff': args.home_sp_era_split_diff,
        'away_lineup_contact_rank': args.away_contact_rank,
        'home_lineup_contact_rank': args.home_contact_rank,
        'away_sp_rest_days': args.away_sp_rest,
        'home_sp_rest_days': args.home_sp_rest,
        'away_sp_recent_whip_4start': args.away_sp_whip_4,
        'home_sp_recent_whip_4start': args.home_sp_whip_4,
        'away_sp_strong_home_start': args.away_sp_strong_home,
        'home_sp_strong_home_start': args.home_sp_strong_home,
        'away_sp_1st_era': args.away_sp_1st_era,
        'home_sp_1st_era': args.home_sp_1st_era,
        'away_team_1st_rank_30d': args.away_1st_rank_30d,
        'home_team_1st_rank_30d': args.home_1st_rank_30d,
        'away_lineup_1st_pct_recent': args.away_1st_pct,
        'home_lineup_1st_pct_recent': args.home_lineup_1st_pct_recent
    }

    if args.save_overrides and not args.check_data:
        with open(os.path.join(ROOT_DIR, 'data', 'MLB Stats'), 'a', encoding='utf-8') as f:
            if args.override_sp:
                f.write('\nPitching Advanced,,,,,,,,,,,,,,,,,,,,,\n')
                f.write('#,Name,K%,BB%,ERA,xFIP,HR/FB%,Starts,IP,Stuff+\n')
                for i, ov in enumerate(args.override_sp):
                    parts = ov.split(':')
                    if len(parts) >= 5:
                        hrfb = parts[5] if len(parts) >= 6 else '12.0%'
                        starts = parts[6] if len(parts) >= 7 else '10'
                        ip = parts[7] if len(parts) >= 8 else '100'
                        stuff = parts[8] if len(parts) >= 9 else '100'
                        f.write(f'{i+999},{parts[0]},{parts[1]},{parts[2]},{parts[3]},{parts[4]},{hrfb},{starts},{ip},{stuff}\n')
            
            if args.override_batter:
                f.write('\nBatting Advanced,,,,,,,,,,,,,,,,,,,,,\n')
                f.write('#,Name,K%,wOBA,Hand\n')
                for i, ov in enumerate(args.override_batter):
                    parts = ov.split(':')
                    if len(parts) >= 2:
                        woba = parts[2] if len(parts) >= 3 else '0.320'
                        hand = parts[3] if len(parts) >= 4 else 'R'
                        f.write(f'{i+999},{parts[0]},{parts[1]},{woba},{hand}\n')
        print("[AUTO-CACHE] Saved overridden stats to MLB Stats database permanently.")

    market_odds = {}
    if args.odds:
        try:
            for pair in args.odds.split(','):
                label, val = pair.rsplit(':', 1)
                market_odds[label.strip()] = float(val.strip())
        except Exception as e:
            print(f"[!] ERROR: Could not parse odds '{args.odds}': {e}")

    # K-Alpha V1.0: Calculate Lineup K% for better projection
    away_lineup_k = statistics.mean([b['K_pct'] for b in away_lineup_statcast])
    home_lineup_k = statistics.mean([b['K_pct'] for b in home_lineup_statcast])

    # V20.0 Fix 3: Estimate Stuff+ from K/9 when Pitching+ data is unavailable
    def estimate_stuff_plus(k9):
        """Estimate Stuff+ from K/9 rate when raw Pitching+ data is missing."""
        if k9 >= 12.0: return 130
        elif k9 >= 10.5: return 120
        elif k9 >= 9.5: return 115
        elif k9 >= 8.5: return 105
        elif k9 >= 7.5: return 100
        elif k9 >= 6.5: return 95
        else: return 90

    # Fetch Stuff+ from sections, with K/9 fallback
    def get_stuff_plus(name):
        norm_search = normalize_name(name)
        # Primary: Look for explicit Pitching+ section
        for p in sections.get('Pitching +', []):
            if normalize_name(p.get('Name', '')) == norm_search:
                return safe_float(p.get('Stuff+'), 100.0)
        # Fallback: Estimate from K/9 in Pitching Advanced
        for p in sections.get('Pitching Advanced', []):
            p_name = p.get('Name', '').strip()
            if not p_name or p_name.lower() == 'name': continue
            if normalize_name(p_name) == norm_search:
                k9 = safe_float(p.get('K/9'), 8.5)
                estimated = estimate_stuff_plus(k9)
                print(f"  [V20.0 STUFF+ EST] {name}: K/9={k9:.1f} -> Stuff+={estimated}")
                return estimated
        return 100.0

    if 'Stuff' not in away_sp_data or away_sp_data['Stuff'] == 100:
        away_sp_data['Stuff'] = get_stuff_plus(away_sp_data['Name'])
    if 'Stuff' not in home_sp_data or home_sp_data['Stuff'] == 100:
        home_sp_data['Stuff'] = get_stuff_plus(home_sp_data['Name'])

    omni = OmniProphetV18()
    # Update game_data with lineup K%
    game_data['away_lineup_k_pct'] = away_lineup_k
    game_data['home_lineup_k_pct'] = home_lineup_k

    omni.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == "__main__":
    main()