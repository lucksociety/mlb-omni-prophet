import re
import os
import unicodedata

def normalize_name(name):
    if not name: return ""
    name = "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = name.replace('.', '').replace('-', ' ').strip().lower()
    for suffix in [' jr', ' sr', ' iii', ' ii', ' iv']:
        if name.endswith(suffix):
            name = name[:-len(suffix)].strip()
    return name

def parse_multi_csv(filepath):
    sections = {}
    current_section = None
    headers = []
    if not os.path.exists(filepath): return sections
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if "Batting Advanced" in line:
                current_section = "Batting Advanced"
                sections[current_section] = []
                headers = []
                continue
            if "Pitching Advanced" in line:
                current_section = "Pitching Advanced"
                sections[current_section] = []
                headers = []
                continue
            if current_section:
                row = line.split(',')
                if row[0] == '#' and not headers:
                    headers = [h.strip() for h in row]
                    continue
                if headers and row[0] != '#':
                    if len(row) >= len(headers):
                        row_dict = dict(zip(headers, row[:len(headers)]))
                        sections[current_section].append(row_dict)
    return sections

# Load database
sections = parse_multi_csv('/Users/danielreiss/Desktop/Antigravity/MLB/MLB Stats')
pitchers_db = {normalize_name(p.get('Name', '')): p for p in sections.get('Pitching Advanced', [])}
batters_db = {normalize_name(b.get('Name', '')): b for b in sections.get('Batting Advanced', [])}

# Read Rotowire content
with open('/Users/danielreiss/.gemini/antigravity/brain/cb02feba-8b2c-4982-8ed5-e44a08c2f27b/.system_generated/steps/190/content.md', 'r') as f:
    content = f.read()

# Extract games and lineups
# Looking for patterns like [Team] (Record) ... [Pitcher] ... [Lineup]
games = []
# This is a rough parser for the Rotowire markdown format
sections_split = content.split('Alerts](https://www.rotowire.com/baseball/daily-lineups.php)')
for s in sections_split[1:]:
    # Extract Teams
    teams = re.findall(r'\[(.*?)\s+\(\d+-\d+\)', s)
    if len(teams) < 2: continue
    away_team, home_team = teams[0], teams[1]
    
    # Extract Pitchers
    pitchers = re.findall(r'\[(.*?)\]\(https://www\.rotowire\.com/baseball/player/.*?\)\s+[RL]\s+\d+-\d+', s)
    if len(pitchers) < 2: continue
    away_sp, home_sp = pitchers[0], pitchers[1]
    
    # Extract Lineups
    # Lineups appear after "Confirmed Lineup" or "Expected Lineup"
    lineup_parts = re.split(r'Confirmed Lineup|Expected Lineup', s)
    away_lineup = []
    home_lineup = []
    if len(lineup_parts) >= 2:
        away_lineup = re.findall(r'\[(.*?)\]\(https://www\.rotowire\.com/baseball/player/.*?\)', lineup_parts[1])[:9]
    if len(lineup_parts) >= 3:
        home_lineup = re.findall(r'\[(.*?)\]\(https://www\.rotowire\.com/baseball/player/.*?\)', lineup_parts[2])[:9]
    
    games.append({
        'away': away_team, 'home': home_team,
        'away_sp': away_sp, 'home_sp': home_sp,
        'away_lineup': away_lineup, 'home_lineup': home_lineup
    })

missing_pitchers = set()
missing_batters = set()

for g in games:
    if normalize_name(g['away_sp']) not in pitchers_db: missing_pitchers.add(g['away_sp'])
    if normalize_name(g['home_sp']) not in pitchers_db: missing_pitchers.add(g['home_sp'])
    for b in g['away_lineup']:
        if normalize_name(b) not in batters_db: missing_batters.add(b)
    for b in g['home_lineup']:
        if normalize_name(b) not in batters_db: missing_batters.add(b)

print("MISSING PITCHERS:")
for p in sorted(missing_pitchers): print(f"- {p}")
print("\nMISSING BATTERS:")
for b in sorted(missing_batters): print(f"- {b}")
