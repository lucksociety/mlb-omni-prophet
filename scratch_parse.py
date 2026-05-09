import urllib.request
import re
import subprocess
import json
import os

url = "https://www.rotowire.com/baseball/daily-lineups.php"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
except Exception as e:
    print("Error fetching:", e)
    import sys; sys.exit(1)

# Now parse the HTML directly
# Find all blocks: <div class="lineup__box"> ... </div>
# The games are inside these boxes
boxes = re.findall(r'<div class="lineup__box">(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)

missing_pitchers = set()
missing_batters = set()

def get_ordered_unique(plist):
    res = []
    for p in plist:
        if p not in res:
            res.append(p)
    return res

for box in boxes:
    # Get team names
    # <div class="lineup__team is-visit"> ... <div class="lineup__abbr">TEX</div>
    away = re.search(r'lineup__team is-visit.*?lineup__abbr">([^<]+)', box, re.DOTALL)
    home = re.search(r'lineup__team is-home.*?lineup__abbr">([^<]+)', box, re.DOTALL)
    if not away or not home: continue
    away_team = away.group(1).strip()
    home_team = home.group(1).strip()
    
    # Get all players: <a title="Player Name" href="/baseball/player/...
    players = re.findall(r'<a title="([^"]+)"\s+href="/baseball/player/', box)
    
    # In Rotowire HTML:
    # 1. Away SP
    # 2. Away 9 Batters
    # 3. Home SP
    # 4. Home 9 Batters
    # Then it might have umpires etc.
    
    all_players = get_ordered_unique(players)
    if len(all_players) >= 20:
        away_sp = all_players[0]
        away_lineup = all_players[1:10]
        home_sp = all_players[10]
        home_lineup = all_players[11:20]
        
        cmd = [
            "python3", "/Users/danielreiss/Desktop/Antigravity/MLB/auto_sim_v16.py",
            "--away", away_team, "--home", home_team,
            "--away_sp", away_sp, "--home_sp", home_sp,
            "--away_lineup", ",".join(away_lineup),
            "--home_lineup", ",".join(home_lineup),
            "--check_data"
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        try:
            data = json.loads(res.stdout)
            for p in data.get("missing_pitchers", []): missing_pitchers.add(p)
            for b in data.get("missing_batters", []): missing_batters.add(b)
        except:
            pass

print("PITCHERS:")
for p in missing_pitchers: print(p)
print("BATTERS:")
for b in missing_batters: print(b)
