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

# ── RESEARCH DATA AUDIT ─────────────────────────────────────────

# Aaron Nola (PHI) - Forensic Audit
# ERA: 6.03 | xERA: 4.42 | Stuff+: 102 | VAA: -4.8
# K%: 25.0% | BB%: 9.3% | IP: 31.1
# L3 CSW%: 30.4% | L3 SwStr%: 12.1% | Velo: Stable
# Archetype: Standard

# Janson Junk (MIA) - Forensic Audit
# ERA: 3.00 | xERA: 3.51 | Stuff+: 106 | VAA: -5.1
# K%: 15.8% | BB%: 6.0% | IP: 33.0
# L3 CSW%: 29.1% | L3 SwStr%: 19.7% | Velo: Stable
# Archetype: East-West

game_data = {
    'away_team': 'PHI',
    'home_team': 'MIA',
    'away_sp_name': 'Aaron Nola',
    'home_sp_name': 'Janson Junk',
    'away_sp_hand': 'R',
    'home_sp_hand': 'R',
    'away_sp_era': 6.03,
    'home_sp_era': 3.00,
    'away_sp_statcast': {
        'Full Name': 'Aaron Nola',
        'Hand': 'R',
        'ERA': 6.03,
        'Stuff': 102,
        'VAA': -4.8,
        'K_pct': 25.0,
        'BB_pct': 9.3,
        'IP': 31.1,
        'xERA': 4.42,
    },
    'home_sp_statcast': {
        'Full Name': 'Janson Junk',
        'Hand': 'R',
        'ERA': 3.00,
        'Stuff': 106,
        'VAA': -5.1,
        'K_pct': 15.8,
        'BB_pct': 6.0,
        'IP': 33.0,
        'xERA': 3.51,
    },
    'away_lineup_names': [
        'Trea Turner', 'Kyle Schwarber', 'Bryce Harper', 'Adolis Garcia', 
        'Brandon Marsh', 'Bryson Stott', 'Alec Bohm', 'Garrett Stubbs', 'Justin Crawford'
    ],
    'away_lineup_hands': ['R', 'L', 'L', 'R', 'L', 'L', 'R', 'L', 'L'],
    'away_lineup_statcast': [
        {'K_pct': 20.0, 'O_Swing': 28.0, 'Z_Contact': 85.0}, # Turner
        {'K_pct': 22.0, 'O_Swing': 41.2, 'Z_Contact': 81.4}, # Schwarber
        {'K_pct': 24.0, 'O_Swing': 30.0, 'Z_Contact': 82.0}, # Harper
        {'K_pct': 26.0, 'O_Swing': 35.0, 'Z_Contact': 78.0}, # Garcia
        {'K_pct': 21.1, 'O_Swing': 25.0, 'Z_Contact': 89.0}, # Marsh
        {'K_pct': 18.6, 'O_Swing': 24.0, 'Z_Contact': 93.3}, # Stott
        {'K_pct': 16.7, 'O_Swing': 23.8, 'Z_Contact': 88.0}, # Bohm
        {'K_pct': 25.0, 'O_Swing': 32.0, 'Z_Contact': 80.0}, # Stubbs
        {'K_pct': 16.7, 'O_Swing': 20.0, 'Z_Contact': 90.0}, # Crawford
    ],
    'home_lineup_names': [
        'Jakob Marsee', 'Kyle Stowers', 'Otto Lopez', 'Xavier Edwards', 
        'Liam Hicks', 'Christopher Morel', 'Joe Mack', 'Owen Caissie', 'Graham Pauley'
    ],
    'home_lineup_hands': ['L', 'L', 'R', 'S', 'L', 'R', 'L', 'L', 'L'],
    'home_lineup_statcast': [
        {'K_pct': 24.5, 'O_Swing': 26.0, 'Z_Contact': 84.0}, # Marsee
        {'K_pct': 24.5, 'O_Swing': 28.0, 'Z_Contact': 82.0}, # Stowers
        {'K_pct': 19.9, 'O_Swing': 22.0, 'Z_Contact': 88.0}, # Lopez
        {'K_pct': 10.3, 'O_Swing': 18.0, 'Z_Contact': 94.0}, # Edwards
        {'K_pct': 8.0,  'O_Swing': 15.0, 'Z_Contact': 95.0}, # Hicks
        {'K_pct': 30.8, 'O_Swing': 36.0, 'Z_Contact': 75.0}, # Morel
        {'K_pct': 28.0, 'O_Swing': 28.0, 'Z_Contact': 82.0}, # Mack
        {'K_pct': 42.6, 'O_Swing': 34.0, 'Z_Contact': 70.0}, # Caissie
        {'K_pct': 25.3, 'O_Swing': 27.0, 'Z_Contact': 83.0}, # Pauley
    ],
    'park_factor': 95,
    'is_dome': True,
    'env': {
        'Weather': {'temp': 72, 'wind_speed': 0, 'wind_dir': 0, 'humidity': 50},
        'altitude': 15,
        'rain_intensity': 0.0,
        'Umpire': {'name': 'Neutral', 'CS_pct': 16.5, 'zone_type': 'neutral'},
    },
    'away_drs': -27,
    'home_drs': -15,
    'away_manager_hook': 0.0,
    'home_manager_hook': 0.0,
    'away_bp_pitches_d1': 50,
    'away_bp_pitches_d2': 0,
    'home_bp_pitches_d1': 20,
    'home_bp_pitches_d2': 0,
    'away_catcher': 'Garrett Stubbs',
    'home_catcher': 'Joe Mack',
    'game_time': '18:40',
}

market_odds = {
    'MIA ML': -115,
    'PHI ML': -105,
    'Total Over 8.5': -110,
    'Total Under 8.5': -110,
    'Nola Over 5.5 K': -110,
    'Junk Over 3.5 K': -110,
}

if __name__ == "__main__":
    omni = OmniProphetV16()
    omni.run_omni_simulation(game_data, market_odds=market_odds)