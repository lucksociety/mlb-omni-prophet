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

GAMES = [
    {
        'away': {
            'team': 'SF', 'pitcher': 'Adrian Houser', 'p_hand': 'R',
            'lineup': [
                ['Jung Hoo Lee', 'L'], ['Luis Arraez', 'L'], ['Casey Schmitt', 'R'],
                ['Rafael Devers', 'L'], ['Heliot Ramos', 'R'], ['Willy Adames', 'R'],
                ['Bryce Eldridge', 'L'], ['Harrison Bader', 'R'], ['Eric Haase', 'R']
            ]
        },
        'home': {
            'team': 'LAD', 'pitcher': 'Y. Yamamoto', 'p_hand': 'R',
            'lineup': [
                ['Shohei Ohtani', 'L'], ['Mookie Betts', 'R'], ['Freddie Freeman', 'L'],
                ['Kyle Tucker', 'L'], ['Will Smith', 'R'], ['Max Muncy', 'L'],
                ['Andy Pages', 'R'], ['Teoscar Hernandez', 'R'], ['Hyeseong Kim', 'L']
            ]
        },
        'umpire': 'Jacob Metz', # Placeholder
        'catcher': 'Will Smith',
        'weather': {'temp': 72, 'dome': False}, 
        'park_factor': 1.0,
        'moneyline': -330
    }
]