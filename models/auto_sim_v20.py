import argparse
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import os
import csv
import json, datetime, statistics
import unicodedata
from omni_prophet_v20 import OmniProphetV20
import quant_elite_v6_6 as qe

def normalize_name(name):
    if not name: return ""
    nfkd_form = unicodedata.normalize('NFKD', name)
    name = "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
    name = name.replace(".", "").replace(",", "")
    parts = name.split()
    suffixes = {'jr', 'sr', 'ii', 'iii', 'iv'}
    parts = [p for p in parts if p not in suffixes]
    return " ".join(parts).strip()

def parse_multi_csv(filepath):
    sections = {}
    current_section = None
    last_updated = None
    if not os.path.exists(filepath): return {}, None
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
                except: pass
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
    try: return float(str(val).replace('%', '').strip() or default)
    except: return default

def get_pitcher_stats(sections, sections_25, sections_car, name):
    norm_search = normalize_name(name)
    current_month = datetime.datetime.now().month
    k_w26, k_w25, k_wCar = qe.get_month_weights('P_K_BB', current_month)
    fip_w26, fip_w25, fip_wCar = qe.get_month_weights('FIP', current_month)

    def extract_stats(sec):
        if not sec: return None
        for p in sec.get('Pitching Advanced', []):
            if normalize_name(p.get('Name', '')) == norm_search:
                return {
                    'Name': p.get('Name'),
                    'K%': safe_float(p.get('K%', '20'), 20.0),
                    'BB%': safe_float(p.get('BB%', '8'), 8.0),
                    'ERA': safe_float(p.get('ERA', 4.0), 4.0),
                    'xFIP': safe_float(p.get('xFIP', 4.0), 4.0),
                    'HR/FB': safe_float(p.get('HR/FB', '12'), 12.0),
                    'IP': safe_float(p.get('IP', 100), 100.0),
                    'Starts': safe_float(p.get('Starts', 10), 10.0)
                }
        return None

    s26 = extract_stats(sections)
    if not s26: return None
    s25 = extract_stats(sections_25)
    sCar = extract_stats(sections_car)

    k_final = qe.apply_blending(s26['K%'], s25['K%'] if s25 else None, sCar['K%'] if sCar else None, k_w26, k_w25, k_wCar, 20.0)
    era_final = qe.apply_blending(s26['ERA'], s25['ERA'] if s25 else None, sCar['ERA'] if sCar else None, fip_w26, fip_w25, fip_wCar, 4.0)

    return {
        'Name': s26['Name'], 'ERA': era_final, 'K_pct': k_final,
        'BB_pct': s26['BB%'], 'xERA': s26['xFIP'], 'HR/FB%': s26['HR/FB'],
        'IP': s26['IP'], 'Starts': s26['Starts'], 'Stuff': 100, 'VAA': -4.5
    }

def get_batter_stats(sections, sections_25, sections_car, name):
    norm_search = normalize_name(name)
    def extract_stats(sec):
        if not sec: return None
        for b in sec.get('Batting Advanced', []):
            if normalize_name(b.get('Name', '')) == norm_search:
                return {'Name': b.get('Name'), 'K_pct': safe_float(b.get('K%', '22.7'), 22.7), 'wOBA': safe_float(b.get('wOBA', '0.320'), 0.320)}
        return None
    s26 = extract_stats(sections)
    if not s26: return None
    return {'Name': s26['Name'], 'K_pct': s26['K_pct'], 'wOBA': s26['wOBA'], 'Hand': 'R', 'O_Swing': 30.0, 'Z_Contact': 85.0}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--away', required=True)
    parser.add_argument('--home', required=True)
    parser.add_argument('--away_sp', required=True)
    parser.add_argument('--home_sp', required=True)
    parser.add_argument('--away_lineup', required=True)
    parser.add_argument('--home_lineup', required=True)
    parser.add_argument('--absolute', action='store_true', help="Trigger Absolute Best Prediction Report")
    parser.add_argument('--check_data', action='store_true')
    args = parser.parse_args()

    sections, last_updated = parse_multi_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats'))
    sections_25, _ = parse_multi_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats 2025'))
    sections_car, _ = parse_multi_csv(os.path.join(ROOT_DIR, 'data', 'MLB Stats Career.csv'))

    away_sp_data = get_pitcher_stats(sections, sections_25, sections_car, args.away_sp)
    home_sp_data = get_pitcher_stats(sections, sections_25, sections_car, args.home_sp)

    if args.check_data:
        print(json.dumps({"status": "OK" if away_sp_data and home_sp_data else "STALE_OR_MISSING"}, indent=2))
        return

    away_lineup = [get_batter_stats(sections, sections_25, sections_car, n.strip()) or {'Name': n.strip(), 'K_pct': 22.7, 'wOBA': 0.320} for n in args.away_lineup.split(',')]
    home_lineup = [get_batter_stats(sections, sections_25, sections_car, n.strip()) or {'Name': n.strip(), 'K_pct': 22.7, 'wOBA': 0.320} for n in args.home_lineup.split(',')]

    game_data = {
        'away_team': args.away, 'home_team': args.home,
        'away_sp_name': args.away_sp, 'home_sp_name': args.home_sp,
        'away_sp_hand': 'R', 'home_sp_hand': 'R',
        'away_sp_era': away_sp_data['ERA'] if away_sp_data else 4.40,
        'home_sp_era': home_sp_data['ERA'] if home_sp_data else 4.40,
        'away_sp_statcast': away_sp_data or {'Name': args.away_sp, 'ERA': 4.40, 'Stuff': 100},
        'home_sp_statcast': home_sp_data or {'Name': args.home_sp, 'ERA': 4.40, 'Stuff': 100},
        'away_lineup_names': [b['Name'] for b in away_lineup],
        'home_lineup_names': [b['Name'] for b in home_lineup],
        'away_lineup_statcast': away_lineup, 'home_lineup_statcast': home_lineup,
        'away_lineup_hands': ['R']*9, 'home_lineup_hands': ['R']*9,
        'park_factor': 100, 'is_dome': False,
        'env': {
            'Weather': {'temp': 72, 'wind_speed': 0, 'wind_dir': 0, 'humidity': 50},
            'altitude': 0,
            'rain_intensity': 0.0,
            'Umpire': {'name': 'Unknown', 'zone_type': 'neutral', 'CS_pct': 16.5}
        },
        'game_time': '19:00', 'bullpen_burn': 0.0,
        'away_drs': 0, 'home_drs': 0, 'away_manager_hook': 0.0, 'home_manager_hook': 0.0,
        'away_bp_pitches_d1': 0, 'away_bp_pitches_d2': 0, 'home_bp_pitches_d1': 0, 'home_bp_pitches_d2': 0,
        'away_bp_avg_era': 4.20, 'home_bp_avg_era': 4.20,
        'away_catcher': 'Unknown', 'home_catcher': 'Unknown',
        'absolute_mode': args.absolute
    }

    omni = OmniProphetV20()
    omni.run_omni_simulation(game_data)

if __name__ == "__main__":
    main()
