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

import os
sys.path.append("/Users/danielreiss/Desktop/Antigravity/HR")
from hr_model import HRModel
from games_data import GAMES

model = HRModel("/Users/danielreiss/Desktop/Antigravity/HR/MLB Stats")

hr_hitters = [
    "Drew Romo", "Aaron Judge", "Pete Crow-Armstrong", "Juan Soto", 
    "Bo Bichette", "Elly De La Cruz", "Spencer Steer", "Nolan Gorman", 
    "Victor Scott II", "Oneil Cruz", "Ryan O'Hearn", "Konnor Griffin", 
    "Pete Alonso", "Brice Matthews", "Bobby Witt Jr.", "Salvador Perez", 
    "Ozzie Albies", "Wenceel Pérez", "Josh Naylor", "Byron Buxton", 
    "Sal Frelick", "Colson Montgomery", "Josh Lowe", "Xander Bogaerts", 
    "Edouard Julien"
]

all_results = []
stadiums = {
    "Reds":          {"pf": 112, "temp": 70, "wind": 5, "dir": 45},
    "Orioles":       {"pf": 98,  "temp": 54, "wind": 10, "dir": 20},
    "Blue Jays":     {"pf": 102, "temp": 72, "wind": 0,  "dir": 0},
    "Mets":          {"pf": 97,  "temp": 53, "wind": 12, "dir": 45},
    "Rays":          {"pf": 100, "temp": 72, "wind": 0,  "dir": 0},
    "Braves":        {"pf": 105, "temp": 78, "wind": 4,  "dir": 0},
    "White Sox":     {"pf": 104, "temp": 53, "wind": 10, "dir": 60},
    "Royals":        {"pf": 95,  "temp": 75, "wind": 11, "dir": 135},
    "Brewers":       {"pf": 102, "temp": 72, "wind": 0,  "dir": 0},
    "Rangers":       {"pf": 100, "temp": 72, "wind": 0,  "dir": 0},
    "Astros":        {"pf": 105, "temp": 72, "wind": 0,  "dir": 0},
    "Cardinals":     {"pf": 100, "temp": 78, "wind": 9,  "dir": 135},
    "Dodgers":       {"pf": 102, "temp": 64, "wind": 13, "dir": 225},
    "Giants":        {"pf": 94,  "temp": 58, "wind": 10, "dir": 250},
    "Diamondbacks":  {"pf": 165, "temp": 75, "wind": 5,  "dir": 0}, # Mexico City
}
pitcher_hands = {
    "Keider Montero": "RHP", "Rhett Lowder": "RHP",
    "Connelly Early": "LHP", "Kyle Bradish": "RHP",
    "Slade Cecconi": "RHP", "Patrick Corbin": "LHP",
    "Jose Quintana": "LHP", "Nolan McLean": "RHP",
    "Simeon Woods Richardson": "RHP", "Griffin Jax": "RHP",
    "Aaron Nola": "RHP", "Chris Sale": "LHP",
    "Foster Griffin": "LHP", "Bryan Hudson": "LHP",
    "Reid Detmers": "LHP", "Seth Lugo": "RHP",
    "Zebby Matthews": "RHP", "Freddy Peralta": "RHP",
    "J.T. Ginn": "RHP", "Kumar Rocker": "RHP",
    "Luis Gil": "RHP", "Spencer Arrighetti": "RHP",
    "Emerson Hancock": "RHP", "Michael McGreevy": "RHP",
    "Shota Imanaga": "LHP", "Justin Wrobleski": "LHP",
    "Max Meyer": "RHP", "Landen Roupp": "RHP",
    "Michael King": "RHP", "Ryne Nelson": "RHP",
    "Chase Dollander": "RHP", "Kodai Senga": "RHP",
}

for game in GAMES:
    away = game['away']
    home = game['home']
    home_team = home['team']
    umpire = game.get('umpire', 'MISSING')
    s_data = stadiums.get(home_team, {"pf": 100, "temp": 70, "wind": 0, "dir": 0})
    
    for role, team_data in [('away', away), ('home', home)]:
        opp_pitcher = home['pitcher'] if role == 'away' else away['pitcher']
        opp_team = home['team'] if role == 'away' else away['team']
        p_hand = pitcher_hands.get(opp_pitcher, "RHP")[0]
        
        for i, batter in enumerate(team_data['lineup']):
            prob = model.calculate_hr_probability(
                batter, opp_pitcher, batter_index=i, opp_team_name=opp_team,
                park_factor=s_data['pf'], temp=s_data['temp'],
                wind_speed=s_data['wind'], wind_dir=s_data['dir'],
                pitcher_hand=p_hand, umpire_name=umpire
            )
            all_results.append({
                'player': batter,
                'prob': prob,
                'vs': opp_pitcher
            })

all_results.sort(key=lambda x: x['prob'], reverse=True)

print(f"{'Player':<20} | {'Rank':<4} | {'Prob':<6} | {'Vs Pitcher':<20}")
print("-" * 60)
hits = 0
for i, r in enumerate(all_results, 1):
    found = False
    for h in hr_hitters:
        if h.lower() in r['player'].lower():
            found = True
            break
    if found:
        tag = "HIT!" if i <= 25 else "MISS"
        if i <= 25: hits += 1
        print(f"{r['player']:<20} | {i:<4} | {r['prob']*100:>5.1f}% | {r['vs']:<20} ({tag})")

print("-" * 60)
print(f"TOTAL HITS IN TOP 25: {hits} / {len(hr_hitters)}")

print("-" * 60)
print(f"TOTAL HITS IN TOP 25: {hits}")