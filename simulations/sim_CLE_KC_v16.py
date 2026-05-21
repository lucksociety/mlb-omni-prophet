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

def run_sim():
    omni = OmniProphetV16()
    
    game_data = {
        'away_team': 'CLE',
        'home_team': 'KC',
        'away_sp': 'Tanner Bibee',
        'away_sp_hand': 'R',
        'away_sp_era': 4.08,
        'away_sp_ip': 35.1,
        'away_sp_statcast': {
            'Stuff': 105,
            'VAA': -4.5,
            'K_pct': 20.9,
            'BB_pct': 9.2,
            'xERA': 3.95,
            'L3_CSW': 27.5,
            'L3_SwStr': 11.2,
            'Velo_Trend': 'Stable'
        },
        'home_sp': 'Michael Wacha',
        'home_sp_hand': 'R',
        'home_sp_era': 3.13,
        'home_sp_ip': 37.1,
        'home_sp_statcast': {
            'Stuff': 95,
            'VAA': -5.2,
            'K_pct': 22.3,
            'BB_pct': 9.5,
            'xERA': 4.10,
            'L3_CSW': 24.0,
            'L3_SwStr': 9.8,
            'Velo_Trend': 'Stable'
        },
        'away_lineup_names': ['Steven Kwan', 'D. Schneemann', 'Jose Ramirez', 'Rhys Hoskins', 'T. Bazzana', 'David Fry', 'A. Martinez', 'Bo Naylor', 'B. Rocchio'],
        'away_lineup_hands': ['L', 'L', 'S', 'R', 'L', 'R', 'S', 'L', 'S'],
        'away_lineup_statcast': [
            {'K_pct': 12.0, 'O_Swing': 24.0, 'Z_Contact': 92.0},
            {'K_pct': 26.4, 'O_Swing': 32.0, 'Z_Contact': 82.0},
            {'K_pct': 14.5, 'O_Swing': 28.0, 'Z_Contact': 88.0},
            {'K_pct': 29.0, 'O_Swing': 28.0, 'Z_Contact': 74.0},
            {'K_pct': 24.0, 'O_Swing': 30.0, 'Z_Contact': 84.0},
            {'K_pct': 25.0, 'O_Swing': 31.0, 'Z_Contact': 78.0},
            {'K_pct': 26.0, 'O_Swing': 32.0, 'Z_Contact': 80.0},
            {'K_pct': 28.6, 'O_Swing': 34.0, 'Z_Contact': 76.0},
            {'K_pct': 27.2, 'O_Swing': 33.0, 'Z_Contact': 79.0}
        ],
        'home_lineup_names': ['M. Garcia', 'Bobby Witt Jr.', 'V. Pasquantino', 'S. Perez', 'C. Jensen', 'Lane Thomas', 'J. Caglianone', 'I. Collins', 'Nick Loftin'],
        'home_lineup_hands': ['R', 'R', 'L', 'R', 'L', 'R', 'L', 'S', 'R'],
        'home_lineup_statcast': [
            {'K_pct': 23.0, 'O_Swing': 31.0, 'Z_Contact': 84.0},
            {'K_pct': 18.0, 'O_Swing': 27.0, 'Z_Contact': 89.0},
            {'K_pct': 14.0, 'O_Swing': 22.0, 'Z_Contact': 91.0},
            {'K_pct': 24.0, 'O_Swing': 38.0, 'Z_Contact': 82.0},
            {'K_pct': 26.0, 'O_Swing': 33.0, 'Z_Contact': 81.0},
            {'K_pct': 25.0, 'O_Swing': 32.0, 'Z_Contact': 83.0},
            {'K_pct': 22.0, 'O_Swing': 35.0, 'Z_Contact': 78.0},
            {'K_pct': 27.0, 'O_Swing': 34.0, 'Z_Contact': 80.0},
            {'K_pct': 20.0, 'O_Swing': 26.0, 'Z_Contact': 86.0}
        ],
        'away_sp_name': 'Tanner Bibee',
        'home_sp_name': 'Michael Wacha',
        'is_dome': False,
        'park_factor': 104,
        'game_time': '19:40',
        'env': {
            'Weather': {
                'temp': 80,
                'wind_speed': 11,
                'wind_dir': 0,
                'humidity': 45
            },
            'altitude': 880,
            'rain_intensity': 0.15,
            'is_dome': False,
            'park_factor': 104,
            'Umpire': {
                'name': 'DATA NULL',
                'CS_pct': 16.5,
                'zone_type': 'neutral'
            }
        },
        'away_catcher': 'Bo Naylor',
        'home_catcher': 'C. Jensen',
        'away_drs': 12,
        'home_drs': 28,
        'away_manager_hook': 0.0,
        'home_manager_hook': 0.0,
        'away_bp_pitches_d1': 15,
        'away_bp_pitches_d2': 42,
        'home_bp_pitches_d1': 12,
        'home_bp_pitches_d2': 38,
        'market_odds': {
            'ML': {'CLE': +100, 'KC': -120},
            'Total': 9.0
        },
        'calibration': {
            'total_adj': -0.43,
            'k9_factor': 1.032
        }
    }
    
    omni.run_omni_simulation(game_data)

if __name__ == "__main__":
    run_sim()