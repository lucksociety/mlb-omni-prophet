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



from omni_prophet_v16 import OmniProphetV16
from k_pipeline import KProphetMaster

game_data = {
    'away_team': 'MIN', 'home_team': 'WSH',
    'away_sp_name': 'Simeon Woods Richardson', 'home_sp_name': 'Jake Irvin',
    'away_sp_hand': 'R', 'home_sp_hand': 'R',
    'away_sp_era': 6.49, 'home_sp_era': 4.93,
    'away_lineup_names': ['Buxton', 'Larnach', 'Martin', 'Jeffers', 'Wallner', 'Keaschall', 'Clemens', 'Lee', 'Gray'],
    'away_lineup_hands': ['R', 'L', 'R', 'R', 'L', 'R', 'L', 'S', 'L'],
    'home_lineup_names': ['Wood', 'Lile', 'Mead', 'Abrams', 'House', 'Tena', 'Young', 'Ruiz', 'Nuñez'],
    'home_lineup_hands': ['L', 'L', 'R', 'L', 'R', 'L', 'R', 'S', 'S'],
    'away_sp_statcast': {'Stuff': 88, 'VAA': -1.5, 'K_pct': 11.0, 'BB_pct': 9.6, 'IP': 34.2, 'xERA': 5.78, 'Hand': 'R'},
    'home_sp_statcast': {'Stuff': 102, 'VAA': -1.3, 'K_pct': 26.4, 'BB_pct': 8.5, 'IP': 34.2, 'xERA': 4.10, 'Hand': 'R'},
    'away_lineup_statcast': [{'K_pct': 27.6, 'O_Swing': 32, 'Z_Contact': 80, 'Hand': 'R'}, {'K_pct': 25, 'Hand': 'L'}, {'K_pct': 13.7, 'Hand': 'R'}, {'K_pct': 25, 'Hand': 'R'}, {'K_pct': 36.8, 'Hand': 'L'}, {'K_pct': 14, 'Hand': 'R'}, {'K_pct': 26, 'Hand': 'L'}, {'K_pct': 16.2, 'Hand': 'S'}, {'K_pct': 28, 'Hand': 'L'}],
    'home_lineup_statcast': [{'K_pct': 36.7, 'Hand': 'L'}, {'K_pct': 15.8, 'Hand': 'L'}, {'K_pct': 18.2, 'Hand': 'R'}, {'K_pct': 20, 'Hand': 'L'}, {'K_pct': 31.8, 'Hand': 'R'}, {'K_pct': 22, 'Hand': 'L'}, {'K_pct': 15.6, 'Hand': 'R'}, {'K_pct': 15, 'Hand': 'S'}, {'K_pct': 20.2, 'Hand': 'S'}],
    'env': {'Weather': {'temp': 59, 'wind_speed': 3, 'wind_dir': 0}, 'Umpire': {'CS_pct': 16.0}}
}

k_master = KProphetMaster()
# Map basic env to the format expected by pipeline
env_context = game_data['env'].copy()
env_context['Location'] = game_data['home_team']
env_context['GameTime'] = 19.0
env_context['Moneyline'] = 0

away_k_proj = k_master.execute_pipeline(game_data['away_sp_statcast'], game_data['home_lineup_statcast'], env_context, {'PitchLimit': 92})
home_k_proj = k_master.execute_pipeline(game_data['home_sp_statcast'], game_data['away_lineup_statcast'], env_context, {'PitchLimit': 92})

print(f"Jake Irvin Over 4.5 K Prob: {home_k_proj['probabilities'][4.5]['Over']:.1%}")
print(f"S. Richardson Under 3.5 K Prob: {away_k_proj['probabilities'][3.5]['Under']:.1%}")