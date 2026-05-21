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

sys.path.append("/Users/danielreiss/Desktop/Antigravity/MLB")
import nrfi_yrfi_model as yrfi

def test_matchup(name, home_p, away_p, ballpark, home_lineup, away_lineup):
    game = yrfi.GameInput(
        home_team="HOME", away_team="AWAY",
        home_pitcher=home_p, away_pitcher=away_p,
        ballpark=ballpark,
        home_lineup=home_lineup, away_lineup=away_lineup
    )
    pred = yrfi.predict_game(game)
    print(f"\n--- TEST: {name} ---")
    print(f"Matchup: {away_p} @ {home_p} ({ballpark})")
    print(f"YRFI Prob: {pred.yrfi_prob*100:.1f}%")
    print(f"Top NR: {pred.top_nr_prob*100:.1f}% | Bottom NR: {pred.bottom_nr_prob*100:.1f}%")

# 1. Standard Average Matchup (using default stats 4.0 ERA, 100 wRC+)
test_matchup("Average vs Average", "Unknown P1", "Unknown P2", "Neutral", [], [])

# 2. Ace Duel (High K, low ERA)
# We need real names or overrides. Let's use Zack Wheeler and Tarik Skubal if they are in the data.
test_matchup("Ace Duel", "Zack Wheeler", "Tarik Skubal", "Neutral", [], [])

# 3. Slugfest in Coors
test_matchup("Coors Slugfest", "Unknown P3", "Unknown P4", "Coors Field", 
             ["Aaron Judge", "Shohei Ohtani", "Juan Soto", "Matt Olson", "George Springer"],
             ["Aaron Judge", "Shohei Ohtani", "Juan Soto", "Matt Olson", "George Springer"])

# 4. Bad Pitchers
test_matchup("Bad Pitchers", "Simeon Woods Richardson", "Justin Wrobleski", "Neutral", [], [])