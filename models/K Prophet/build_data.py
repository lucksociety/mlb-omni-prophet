import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)
#!/usr/bin/env python3
"""
V7.0 Data Builder — Advanced Column Mapping.
Parses stats from multiple sources and maps them to K Prophet V7.0 format.
"""
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

SRC = '/Users/danielreiss/Desktop/Antigravity/MLB/data/MLB Stats'
SRC2 = '/Users/danielreiss/Desktop/Antigravity/K Prophet/K Profit Data - Sheet1.csv'

def pct(val):
    if not val or str(val).strip() == '':
        return ''
    return str(val).strip().replace('%', '')

def num(val):
    if not val or str(val).strip() == '':
        return ''
    v = str(val).strip()
    if v.startswith('.'):
        v = '0' + v
    return v

def get_section_data(section_names, required_cols=None):
    """Searches SRC and SRC2 for a list of section name variations and returns (headers, rows)."""
    if isinstance(section_names, str):
        section_names = [section_names]
    
    section_names_lower = [s.lower() for s in section_names]
    
    for src_path in [SRC2, SRC]:
        if not os.path.exists(src_path): continue
        with open(src_path, 'r') as f:
            reader = csv.reader(f)
            found = False
            headers = []
            section_rows = []
            for row in reader:
                if not row: continue
                # Match section name or variations
                cell0 = row[0].strip().lower()
                if not found:
                    if any(s == cell0 or (s in cell0 and len(cell0) < len(s) + 5) for s in section_names_lower):
                        found = True
                    continue
                
                if found:
                    if row[0].strip() == '#':
                        headers = [h.strip() for h in row]
                        continue
                    if headers:
                        # Stop if we hit a blank row or another major section
                        if not row[0].strip() or row[0].strip().startswith('---'):
                            break
                        # Guard against running into another section if # was missing
                        if cell0 in ['advanced', 'plate discipline', 'pitching +', 'batting advanced', 'pitching advanced']:
                            break
                        section_rows.append(dict(zip(headers, row)))
            
            if found and section_rows:
                # If required_cols is provided, verify they exist in headers
                if required_cols:
                    if any(any(c in h for h in headers) for c in required_cols):
                        return headers, section_rows
                    else:
                        # Required columns not found in this "Advanced" section, keep searching
                        found = False
                        headers = []
                        section_rows = []
                        continue
                return headers, section_rows
    return None, None


def build():
    print("🚀 Starting K Prophet V5.1 Data Build...")
    
    # 1. Batting Advanced
    _, rows = get_section_data(['Batting Advanced', 'Batting Advanced +', 'Advanced'], required_cols=['K%'])
    if rows:
        with open(os.path.join(DATA_DIR, 'batting_advanced.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['Name', 'Team', 'PA', 'BB_pct', 'K_pct', 'wRC_plus'])
            for r in rows:
                name = r.get('Name')
                team = r.get('Team')
                pa = r.get('PA PA - Plate Appearances') or r.get('PA', '')
                bb = r.get('BB% BB% - Walk Percentage (BB/PA)') or r.get('BB%', '')
                k = r.get('K% K% - Strikeout Percentage (SO/PA)') or r.get('K%', '')
                wrc = r.get('wRC+ wRC+ - Runs per PA scaled where 100 is average; both league and park adjusted; based on wOBA') or r.get('wRC+', '')
                w.writerow([name, team, num(pa), pct(bb), pct(k), num(wrc)])
        print("✅ Batting Advanced built.")
    else:
        print("⚠ Warning: Batting Advanced section not found.")

    # 2. Pitching Advanced
    _, rows = get_section_data(['Pitching Advanced', 'Pitching Advanced +', 'Advanced'], required_cols=['K%'])
    if rows:
        with open(os.path.join(DATA_DIR, 'pitching_advanced.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['Name', 'Team', 'K_pct', 'BB_pct', 'SIERA', 'xFIP', 'Zone_pct', 'F-Strike_pct'])
            for r in rows:
                name = r.get('Name')
                team = r.get('Team')
                k = r.get('K%') or r.get('K% K% - Strikeout Percentage (SO/TBF)', '')
                bb = r.get('BB%') or r.get('BB% BB% - Walk Percentage (BB/TBF)', '')
                siera = r.get('SIERA') or r.get('SIERA SIERA - Skill Interactive ERA', '')
                xfip = r.get('xFIP') or r.get('xFIP xFIP - Expected Fielder Independent Pitching', '')
                zone = r.get('Zone%') or ''
                fstrike = r.get('F-Strike%') or ''
                w.writerow([name, team, pct(k), pct(bb), num(siera), num(xfip), pct(zone), pct(fstrike)])
        print("✅ Pitching Advanced built (with Zone/F-Strike).")

    # 3. Batting Discipline
    _, rows = get_section_data(['Batting Plate Discipline', 'Batting Discipline', 'Plate Discipline'])
    if rows:
        with open(os.path.join(DATA_DIR, 'batting_discipline.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['Name', 'Team', 'O-Swing', 'Z-Swing', 'Contact', 'SwStr', 'CSW'])
            for r in rows:
                w.writerow([r.get('Name'), r.get('Team'), pct(r.get('O-Swing%')), pct(r.get('Z-Swing%')), pct(r.get('Contact%')), pct(r.get('SwStr%')), pct(r.get('CSW%'))])
        print("✅ Batting Discipline built.")

    # 4. Pitching Discipline
    _, rows = get_section_data(['Plate Discipline', 'Advanced'], required_cols=['SwStr%'])
    if rows:
        with open(os.path.join(DATA_DIR, 'pitching_discipline.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['Name', 'Team', 'O-Swing', 'Z-Swing', 'Contact', 'SwStr', 'CSW'])
            for r in rows:
                w.writerow([r.get('Name'), r.get('Team'), pct(r.get('O-Swing%')), pct(r.get('Z-Swing%')), pct(r.get('Contact%')), pct(r.get('SwStr%')), pct(r.get('CSW%'))])
        print("✅ Pitching Discipline built.")

    # 5. Pitching+ (Stuff+)
    _, rows = get_section_data(['Pitching +', 'Pitching Plus'])
    if rows:
        with open(os.path.join(DATA_DIR, 'pitching_plus.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            header = ['Name', 'Team', 'IP', 'Stuff', 'Location', 'Pitching', 'FA', 'SI', 'FC', 'FS', 'SL', 'CU', 'CH', 'KC', 'FO']
            w.writerow(header)
            for r in rows:
                name = r.get('Name')
                team = r.get('Team')
                ip = r.get('IP IP - Innings Pitched') or r.get('IP', '')
                stuff = r.get('Stuff+') or r.get('Stuff+ Stuff+ - Model based pitching metric where 100 is average', '')
                loc = r.get('Location+') or r.get('Location+ Location+ - Model based pitching metric where 100 is average', '')
                pit = r.get('Pitching+') or r.get('Pitching+ Pitching+ - Model based pitching metric where 100 is average', '')
                fa = r.get('Pit+ FA') or ''
                si = r.get('Pit+ SI') or ''
                fc = r.get('Pit+ FC') or ''
                fs = r.get('Pit+ FS') or ''
                sl = r.get('Pit+ SL') or ''
                cu = r.get('Pit+ CU') or ''
                ch = r.get('Pit+ CH') or ''
                kc = r.get('Pit+ KC') or ''
                fo = r.get('Pit+ FO') or ''
                w.writerow([name, team, num(ip), num(stuff), num(loc), num(pit), num(fa), num(si), num(fc), num(fs), num(sl), num(cu), num(ch), num(kc), num(fo)])
        print("✅ Pitching+ built (with Pitch Mix).")

    # 6. Pitching Statcast
    _, rows = get_section_data(['Pitching Statcast'])
    if rows:
        with open(os.path.join(DATA_DIR, 'pitching_statcast.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['Name', 'Team', 'HardHit_pct', 'Barrel_pct', 'xERA', 'xwOBA'])
            for r in rows:
                name = r.get('Name')
                team = r.get('Team')
                hh = r.get('HardHit%') or r.get('HardHit% HardHit% - Percentage of batted balls with exit velocity of 95 mph or higher', '')
                br = r.get('Barrel%') or r.get('Barrel% Barrel% - Percentage of batted balls that are classified as barrels', '')
                xera = r.get('xERA') or r.get('xERA xERA - Expected ERA', '')
                xwoba = r.get('xwOBA') or r.get('xwOBA xwOBA - Expected Weighted On-Base Average', '')
                w.writerow([name, team, pct(hh), pct(br), num(xera), num(xwoba)])
        print("✅ Pitching Statcast built.")

    # 7. Batting Statcast
    _, rows = get_section_data(['Batting Statcast', 'Batting Stat Cast'])
    if rows:
        with open(os.path.join(DATA_DIR, 'batting_statcast.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['Name', 'Team', 'EV', 'HardHit_pct', 'xwOBA'])
            for r in rows:
                w.writerow([r.get('Name'), r.get('Team'), num(r.get('EV')), pct(r.get('HardHit%')), num(r.get('xwOBA'))])
        print("✅ Batting Statcast built.")

    print("🎯 Data build complete.")

if __name__ == '__main__':
    build()