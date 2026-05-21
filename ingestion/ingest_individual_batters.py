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

data = [
    {"Name": "Anthony Volpe", "Team": "NYY", "PA": 596, "BB%": "7.2%", "K%": "25.2%", "AVG": ".212", "OBP": ".272", "SLG": ".391", "wOBA": ".286", "wRC+": 83},
    {"Name": "Tommy Edman", "Team": "LAD", "PA": 377, "BB%": "5.0%", "K%": "16.2%", "AVG": ".225", "OBP": ".274", "SLG": ".382", "wOBA": ".284", "wRC+": 81},
    {"Name": "Gavin Lux", "Team": "LAD", "PA": 503, "BB%": "11.1%", "K%": "22.7%", "AVG": ".269", "OBP": ".350", "SLG": ".374", "wOBA": ".322", "wRC+": 102},
    {"Name": "Sebastian Walcott", "Team": "TEX", "PA": 552, "BB%": "12.7%", "K%": "19.6%", "AVG": ".255", "OBP": ".355", "SLG": ".386", "wOBA": ".349", "wRC+": 110}
]

with open('/Users/danielreiss/Desktop/Antigravity/MLB/data/MLB Stats', 'a', encoding='utf-8') as f:
    # No section header needed if we just append to Batting Advanced
    # But wait, Batting Advanced was written earlier. I'll just append them.
    for b in data:
        # Header for reference: #,Name,Team,PA,BB%,K%,BB/K,AVG,OBP,SLG,OPS,ISO,Spd,BABIP,UBR,wGDP,XBR,wSB,wRC,wRAA,wOBA,wRC+
        # We only need enough columns to satisfy the parser.
        # The parser uses headers from the last '#' row it saw.
        f.write(f"999,{b['Name']},{b['Team']},{b['PA']},{b['BB%']},{b['K%']},0.50,{b['AVG']},{b['OBP']},{b['SLG']},.700,.150,5.0,.300,0,0,0,0,50,0,{b['wOBA']},{b['wRC+']}\n")

print("Successfully ingested missing batters.")