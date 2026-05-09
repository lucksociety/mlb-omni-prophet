import subprocess
import json

# Tonight's Slate: May 8, 2026
games = [
    {
        "away": "HOU", "home": "CIN", "away_sp": "Mike Burrows", "home_sp": "Nick Lodolo",
        "away_lineup": "Altuve,Alvarez,Tucker,Bregman,Pena,Diaz,Meyers,Dubon,McCormick",
        "home_lineup": "Friedl,Bleday,De La Cruz,Steer,Stephenson,Lowe,India,Hayes,McClain",
        "game_time": 18.1, "location": "CIN"
    },
    {
        "away": "COL", "home": "PHI", "away_sp": "Chase Dollander", "home_sp": "Jesús Luzardo",
        "away_lineup": "Blackmon,Tovar,Bryant,McMahon,Jones,Doyle,Rodgers,Stallings,Beck",
        "home_lineup": "Schwarber,Turner,Harper,Garcia,Marsh,Realmuto,Stott,Bohm,Crawford",
        "game_time": 18.6, "location": "PHI", "home_ivb": 17.5 
    },
    {
        "away": "LAA", "home": "TOR", "away_sp": "Reid Detmers", "home_sp": "Dylan Cease",
        "away_lineup": "Schanuel,Trout,Ohtani,Rendon,Ward,Drury,O'Hoppe,Neto,Moniak",
        "home_lineup": "Springer,Bichette,Guerrero,Okamoto,Varsho,Kirk,Clement,Kiermaier,Biggio",
        "game_time": 19.1, "location": "TOR", "home_hb": 15.5 
    },
    {
        "away": "NYM", "home": "ARI", "away_sp": "David Peterson", "home_sp": "Ryne Nelson",
        "away_lineup": "Lindor,Nimmo,Alonso,Martinez,McNeil,Alvarez,Baty,Taylor,Bader",
        "home_lineup": "Carroll,Marte,Gurriel,Walker,Suarez,Moreno,McCarthy,Ahmed,Perdomo",
        "game_time": 21.6, "location": "ARI", "home_ivb": 18.9 
    },
    {
        "away": "PIT", "home": "SF", "away_sp": "Carmen Mlodzinski", "home_sp": "Jordan Hicks",
        "away_lineup": "Hayes,Reynolds,Cruz,Suwinski,Joe,Triolo,Davis,Taylor,Williams",
        "home_lineup": "Lee,Estrada,Wade,Conforto,Bailey,Soler,Chapman,Ahmed,Fitzgerald",
        "game_time": 22.2, "location": "SF", "temp": 58 # Marine Layer trigger
    }
]

print("# MLB Omni-Prophet V17.1 - Tonight's Physics-Optimized Slate\n")
for g in games:
    cmd = [
        "python3", "auto_sim_v16.py",
        "--away", g["away"],
        "--home", g["home"],
        "--away_sp", g["away_sp"],
        "--home_sp", g["home_sp"],
        "--away_lineup", g["away_lineup"],
        "--home_lineup", g["home_lineup"],
        "--game_time_decimal", str(g.get("game_time", 19.0))
    ]
    
    # Layer 6 Statcast Overrides
    if "away_ivb" in g: cmd.extend(["--away_ivb", str(g["away_ivb"])])
    if "home_ivb" in g: cmd.extend(["--home_ivb", str(g["home_ivb"])])
    if "away_hb" in g: cmd.extend(["--away_hb", str(g["away_hb"])])
    if "home_hb" in g: cmd.extend(["--home_hb", str(g["home_hb"])])
    if "bullpen_burn" in g: cmd.extend(["--bullpen_burn", str(g["bullpen_burn"])])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"## {g['away']} @ {g['home']}")
    print(f"**SP:** {g['away_sp']} vs {g['home_sp']}")
    if result.stderr:
        print(f"⚠️ **Error:** {result.stderr}")
    print(result.stdout)
    print("-" * 40)
