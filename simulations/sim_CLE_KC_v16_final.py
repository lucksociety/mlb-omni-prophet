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
    
    # 2026 Statcast data based on user report and harvested metrics
    game_data = {
        'away_team': 'CLE',
        'home_team': 'KC',
        'away_sp_name': 'Slade Cecconi',
        'away_sp_hand': 'R',
        'away_sp_era': 6.56,
        'away_sp_ip': 24.2,
        'away_sp_statcast': {
            'Stuff': 88, # Lowered due to velo drop report
            'VAA': -4.5,
            'K_pct': 18.0,
            'BB_pct': 9.4,
            'xERA': 4.82,
            'L3_CSW': 24.5,
            'L3_SwStr': 9.5,
            'Velo_Trend': 'Down',
            'HR_9': 1.8
        },
        'home_sp_name': 'Seth Lugo',
        'home_sp_hand': 'R',
        'home_sp_era': 2.68,
        'home_sp_ip': 31.1,
        'home_sp_statcast': {
            'Stuff': 98,
            'VAA': -5.1,
            'K_pct': 20.8,
            'BB_pct': 7.4,
            'xERA': 3.93,
            'L3_CSW': 28.0,
            'L3_SwStr': 11.5,
            'Velo_Trend': 'Stable',
            'GB_pct': 52.0
        },
        'away_lineup_names': ['Steven Kwan', 'Angel Martinez', 'Jose Ramirez', 'Kyle Manzardo', 'Daniel Schneemann', 'Travis Bazzana', 'Brayan Rocchio', 'Bo Naylor', 'Petey Halpin'],
        'away_lineup_hands': ['L', 'S', 'S', 'L', 'L', 'L', 'S', 'L', 'L'],
        'away_lineup_statcast': [
            {'K_pct': 9.5, 'O_Swing': 22.0, 'Z_Contact': 93.0},
            {'K_pct': 19.4, 'O_Swing': 31.0, 'Z_Contact': 85.0},
            {'K_pct': 11.5, 'O_Swing': 28.0, 'Z_Contact': 89.0},
            {'K_pct': 27.8, 'O_Swing': 32.0, 'Z_Contact': 78.0},
            {'K_pct': 18.8, 'O_Swing': 30.0, 'Z_Contact': 84.0},
            {'K_pct': 18.2, 'O_Swing': 29.0, 'Z_Contact': 86.0},
            {'K_pct': 17.9, 'O_Swing': 33.0, 'Z_Contact': 82.0},
            {'K_pct': 28.6, 'O_Swing': 34.0, 'Z_Contact': 76.0},
            {'K_pct': 26.5, 'O_Swing': 35.0, 'Z_Contact': 75.0}
        ],
        'home_lineup_names': ['Maikel Garcia', 'Bobby Witt Jr.', 'Vinnie Pasquantino', 'Salvador Perez', 'Carter Jensen', 'Jac Caglianone', 'Isaac Collins', 'Michael Massey', 'Kyle Isbel'],
        'home_lineup_hands': ['R', 'R', 'L', 'R', 'L', 'L', 'S', 'L', 'L'],
        'home_lineup_statcast': [
            {'K_pct': 12.6, 'O_Swing': 30.0, 'Z_Contact': 88.0},
            {'K_pct': 18.1, 'O_Swing': 27.0, 'Z_Contact': 89.0},
            {'K_pct': 16.6, 'O_Swing': 23.0, 'Z_Contact': 91.0},
            {'K_pct': 18.8, 'O_Swing': 38.0, 'Z_Contact': 84.0},
            {'K_pct': 26.6, 'O_Swing': 33.0, 'Z_Contact': 81.0},
            {'K_pct': 30.0, 'O_Swing': 35.0, 'Z_Contact': 78.0},
            {'K_pct': 22.2, 'O_Swing': 34.0, 'Z_Contact': 80.0},
            {'K_pct': 21.0, 'O_Swing': 32.0, 'Z_Contact': 82.0},
            {'K_pct': 22.2, 'O_Swing': 30.0, 'Z_Contact': 83.0}
        ],
        'is_dome': False,
        'park_factor': 104,
        'game_time': '14:10',
        'env': {
            'Weather': {
                'temp': 65,
                'wind_speed': 15,
                'wind_dir': 0, # Straight out to CF
                'humidity': 50
            },
            'altitude': 880,
            'rain_intensity': 0.0,
            'is_dome': False,
            'park_factor': 104,
            'Umpire': {
                'name': 'DATA NULL',
                'CS_pct': 16.5,
                'zone_type': 'neutral'
            }
        },
        'away_catcher': 'Bo Naylor',
        'home_catcher': 'Carter Jensen',
        'away_drs': 5,
        'home_drs': 15,
        'away_manager_hook': 0.0,
        'home_manager_hook': 0.0,
        'away_bp_pitches_d1': 20,
        'away_bp_pitches_d2': 40,
        'home_bp_pitches_d1': 15,
        'home_bp_pitches_d2': 35,
        'market_odds': {
            'Moneyline KC': -145,
            'Moneyline CLE': +122,
            'Game Total Over 9.5': -105,
            'Game Total Under 9.5': -115,
            'Seth Lugo Under 4.5 K': -150,
            'Seth Lugo Over 4.5 K': +115,
            'Slade Cecconi Under 3.5 K': +105,
            'Slade Cecconi Over 3.5 K': -135,
            'NRFI (No Run 1st)': +100,
            'YRFI (Run 1st)': -130,
            'KC Runline -1.5': +140,
            'CLE Runline +1.5': -165,
            'F5 ML KC': -160,
            'F5 ML CLE': +120
        }
    }
    
    omni.clear_canonical()
    omni.run_omni_simulation(game_data, market_odds=game_data['market_odds'])

if __name__ == "__main__":
    run_sim()