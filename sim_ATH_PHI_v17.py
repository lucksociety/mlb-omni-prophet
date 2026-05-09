
import os
import sys
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from omni_prophet_v16 import OmniProphetV17

def run_game_simulation():
    engine = OmniProphetV17()
    
    # ── GAME DATA: ATH @ PHI (2026-05-07) ──────────────────────────
    game_data = {
        'away_team': 'ATH',
        'home_team': 'PHI',
        'away_sp_name': 'J.T. Ginn',
        'home_sp_name': 'Andrew Painter',
        'away_sp_hand': 'R',
        'home_sp_hand': 'R',
        'away_sp_era': 4.30,
        'home_sp_era': 5.28,
        
        # J.T. Ginn Statcast (Estimated from Sinker Profile & Career Stats)
        'away_sp_statcast': {
            'Name': 'J.T. Ginn',
            'Hand': 'R',
            'Stuff': 96,
            'K_pct': 20.0,
            'BB_pct': 8.0,
            'VAA': -4.1,
            'IP': 38,
            'xERA': 4.20,
            'SwStr%': 10.8,
            'CSW%': 28.0
        },
        
        # Andrew Painter Statcast (From Miami Sim)
        'home_sp_statcast': {
            'Name': 'Andrew Painter',
            'Hand': 'R',
            'Stuff': 118,
            'K_pct': 25.0,
            'BB_pct': 9.3,
            'VAA': -4.2,
            'IP': 85,
            'xERA': 4.84,
            'SwStr%': 10.1,
            'CSW%': 26.0
        },
        
        # Athletics Lineup
        'away_lineup_names': [
            'Nick Kurtz', 'Shea Langeliers', 'Tyler Soderstrom', 'Brent Rooker', 
            'Carlos Cortes', 'Jacob Wilson', 'Jeff McNeil', 'Lawrence Butler', 'Darell Hernaiz'
        ],
        'away_lineup_hands': ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'L', 'R'],
        'away_lineup_statcast': [
            {'Name': 'Nick Kurtz', 'Hand': 'L', 'K_pct': 30.8, 'O_Swing': 41.9, 'Z_Contact': 76.0},
            {'Name': 'Shea Langeliers', 'Hand': 'R', 'K_pct': 22.5, 'O_Swing': 35.0, 'Z_Contact': 76.0},
            {'Name': 'Tyler Soderstrom', 'Hand': 'L', 'K_pct': 21.6, 'O_Swing': 33.8, 'Z_Contact': 79.5},
            {'Name': 'Brent Rooker', 'Hand': 'R', 'K_pct': 25.5, 'O_Swing': 32.5, 'Z_Contact': 78.5},
            {'Name': 'Carlos Cortes', 'Hand': 'L', 'K_pct': 56.5, 'O_Swing': 31.5, 'Z_Contact': 75.0},
            {'Name': 'Jacob Wilson', 'Hand': 'R', 'K_pct': 11.1, 'O_Swing': 44.2, 'Z_Contact': 89.6},
            {'Name': 'Jeff McNeil', 'Hand': 'L', 'K_pct': 13.2, 'O_Swing': 26.5, 'Z_Contact': 88.0},
            {'Name': 'Lawrence Butler', 'Hand': 'L', 'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 81.0},
            {'Name': 'Darell Hernaiz', 'Hand': 'R', 'K_pct': 20.0, 'O_Swing': 33.0, 'Z_Contact': 82.0}
        ],
        
        # Phillies Lineup
        'home_lineup_names': [
            'Trea Turner', 'Kyle Schwarber', 'Bryce Harper', 'Adolis Garcia', 
            'Brandon Marsh', 'Bryson Stott', 'Alec Bohm', 'Justin Crawford', 'Rafael Marchan'
        ],
        'home_lineup_hands': ['R', 'L', 'L', 'R', 'L', 'L', 'R', 'L', 'S'],
        'home_lineup_statcast': [
            {'Name': 'Trea Turner', 'Hand': 'R', 'K_pct': 20.0, 'O_Swing': 30.0, 'Z_Contact': 86.0},
            {'Name': 'Kyle Schwarber', 'Hand': 'L', 'K_pct': 33.3, 'O_Swing': 25.0, 'Z_Contact': 75.0},
            {'Name': 'Bryce Harper', 'Hand': 'L', 'K_pct': 14.1, 'O_Swing': 22.0, 'Z_Contact': 88.0},
            {'Name': 'Adolis Garcia', 'Hand': 'R', 'K_pct': 29.9, 'O_Swing': 38.0, 'Z_Contact': 78.0},
            {'Name': 'Brandon Marsh', 'Hand': 'L', 'K_pct': 16.0, 'O_Swing': 28.0, 'Z_Contact': 85.0},
            {'Name': 'Bryson Stott', 'Hand': 'L', 'K_pct': 18.6, 'O_Swing': 24.0, 'Z_Contact': 89.0},
            {'Name': 'Alec Bohm', 'Hand': 'R', 'K_pct': 17.8, 'O_Swing': 32.0, 'Z_Contact': 84.0},
            {'Name': 'Justin Crawford', 'Hand': 'L', 'K_pct': 18.6, 'O_Swing': 26.0, 'Z_Contact': 86.0},
            {'Name': 'Rafael Marchan', 'Hand': 'S', 'K_pct': 15.4, 'O_Swing': 25.0, 'Z_Contact': 88.0}
        ],
        
        'park_factor': 103,
        'is_dome': False,
        'env': {
            'Weather': {
                'temp': 64,
                'wind_speed': 8,
                'wind_dir': 90,
                'humidity': 55
            },
            'Umpire': {
                'name': 'Neutral Umpire',
                'zone_type': 'neutral'
            },
            'altitude': 50,
            'rain_intensity': 0.0,
            'adi': 68
        },
        
        'away_drs': 5,
        'home_drs': -2,
        'away_manager_hook': 5.0,
        'home_manager_hook': 5.0,
        'away_bp_pitches_d1': 45,
        'away_bp_pitches_d2': 30,
        'home_bp_pitches_d1': 20,
        'home_bp_pitches_d2': 60,
        'away_catcher': 'Shea Langeliers',
        'home_catcher': 'Rafael Marchan',
        'game_time': '19:05'
    }
    
    # ── MARKET ODDS (Updated from Screenshots) ───────────────────
    market_odds = {
        'ATH Moneyline': 110,
        'PHI Moneyline': -132,
        'Total Over 9.0': -120,
        'Total Under 9.0': 100, # EVEN
        'F5 Athletics Moneyline': 105,
        'F5 Phillies Moneyline': -135,
        'F5 Total Over 5.0': -120,
        'F5 Total Under 5.0': -110,
        'Andrew Painter Strikeouts Over 4.5': 100, # EVEN
        'Andrew Painter Strikeouts Under 4.5': -130,
        'J.T. Ginn Strikeouts Over 4.5': 135,
        'J.T. Ginn Strikeouts Under 4.5': -180,
        'YRFI (Yes)': -130,
        'NRFI (No)': 100 # EVEN
    }
    
    # Execute Simulation
    engine.run_omni_simulation(game_data, market_odds=market_odds)

if __name__ == '__main__':
    run_game_simulation()
