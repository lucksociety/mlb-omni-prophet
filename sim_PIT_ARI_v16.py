
import sys
import os

# Add the directory to path so we can import OmniProphet
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from omni_prophet_v16 import OmniProphetV16

def run_simulation():
    omni = OmniProphetV16()
    
    market_odds = {
        'PIT ML': -126,
        'ARI ML': 106,
        'PIT -1.5': 135,
        'ARI +1.5': -160,
        'Total Over 8.0': 100,
        'Total Under 8.0': -120,
        'Soroka Over 5.5 K': 105,
        'Soroka Under 5.5 K': -135,
        'Skenes Over 5.5 K': -160,
        'Skenes Under 5.5 K': 120,
        'YRFI': 105,
        'NRFI': -135
    }

    game_data = {
        'away_team': 'PIT',
        'home_team': 'ARI',
        'game_time': '19:40',
        'is_dome': True,
        'park_factor': 110,
        'env': {
            'Weather': {
                'temp': 75,
                'wind_speed': 0,
                'wind_dir': 0,
                'humidity': 40
            },
            'altitude': 1082,
            'rain_intensity': 0.0,
            'Umpire': {
                'name': 'Neutral',
                'CS_pct': 17.5,
                'zone_type': 'neutral'
            }
        },
        'away_sp_name': 'Paul Skenes',
        'away_sp_hand': 'R',
        'away_sp_era': 2.91,
        'away_sp_statcast': {
            'Name': 'Paul Skenes',
            'Hand': 'R',
            'Stuff': 115, # Bumped from 101 based on 2026 Cy Young form
            'K_pct': 27.3,
            'BB_pct': 6.4,
            'VAA': -4.0,
            'IP': 40.0,
            'xERA': 1.94,
            'L3_CSW': 30.5,
            'L3_SwStr': 14.5
        },
        'home_sp_name': 'Michael Soroka',
        'home_sp_hand': 'R',
        'home_sp_era': 4.70,
        'home_sp_statcast': {
            'Name': 'Michael Soroka',
            'Hand': 'R',
            'Stuff': 96,
            'K_pct': 29.6,
            'BB_pct': 6.1,
            'VAA': -4.5,
            'IP': 35.0,
            'xERA': 4.61,
            'L3_CSW': 27.0,
            'L3_SwStr': 11.5
        },
        'away_lineup_names': ['Oneil Cruz', 'Brandon Lowe', 'Bryan Reynolds', 'Ryan O\'Hearn', 'Nick Gonzales', 'Marcell Ozuna', 'Spencer Horwitz', 'Konnor Griffin', 'Henry Davis'],
        'away_lineup_hands': ['L', 'L', 'S', 'L', 'R', 'R', 'L', 'R', 'R'],
        'away_lineup_statcast': [
            {'Name': 'Oneil Cruz', 'Hand': 'L', 'K_pct': 33.3, 'O_Swing': 35, 'Z_Contact': 78},
            {'Name': 'Brandon Lowe', 'Hand': 'L', 'K_pct': 17.9, 'O_Swing': 28, 'Z_Contact': 88},
            {'Name': 'Bryan Reynolds', 'Hand': 'S', 'K_pct': 25.3, 'O_Swing': 27, 'Z_Contact': 86},
            {'Name': 'Ryan O\'Hearn', 'Hand': 'L', 'K_pct': 19.8, 'O_Swing': 30, 'Z_Contact': 88},
            {'Name': 'Nick Gonzales', 'Hand': 'R', 'K_pct': 13.4, 'O_Swing': 32, 'Z_Contact': 90},
            {'Name': 'Marcell Ozuna', 'Hand': 'R', 'K_pct': 31.9, 'O_Swing': 33, 'Z_Contact': 80},
            {'Name': 'Spencer Horwitz', 'Hand': 'L', 'K_pct': 15.6, 'O_Swing': 25, 'Z_Contact': 92},
            {'Name': 'Konnor Griffin', 'Hand': 'R', 'K_pct': 25.8, 'O_Swing': 34, 'Z_Contact': 82},
            {'Name': 'Henry Davis', 'Hand': 'R', 'K_pct': 28.0, 'O_Swing': 32, 'Z_Contact': 82}
        ],
        'home_lineup_names': ['Geraldo Perdomo', 'Ketel Marte', 'Corbin Carroll', 'Adrian Del Castillo', 'Ildemaro Vargas', 'Lourdes Gurriel Jr.', 'Nolan Arenado', 'Gabriel Moreno', 'Alek Thomas'],
        'home_lineup_hands': ['S', 'S', 'L', 'L', 'S', 'R', 'R', 'R', 'L'],
        'home_lineup_statcast': [
            {'Name': 'Geraldo Perdomo', 'Hand': 'S', 'K_pct': 11.8, 'O_Swing': 24, 'Z_Contact': 92},
            {'Name': 'Ketel Marte', 'Hand': 'S', 'K_pct': 16.9, 'O_Swing': 28, 'Z_Contact': 90},
            {'Name': 'Corbin Carroll', 'Hand': 'L', 'K_pct': 30.4, 'O_Swing': 28, 'Z_Contact': 84},
            {'Name': 'Adrian Del Castillo', 'Hand': 'L', 'K_pct': 22.0, 'O_Swing': 30, 'Z_Contact': 85},
            {'Name': 'Ildemaro Vargas', 'Hand': 'S', 'K_pct': 14.8, 'O_Swing': 28, 'Z_Contact': 90},
            {'Name': 'Lourdes Gurriel Jr.', 'Hand': 'R', 'K_pct': 18.0, 'O_Swing': 35, 'Z_Contact': 88},
            {'Name': 'Nolan Arenado', 'Hand': 'R', 'K_pct': 21.1, 'O_Swing': 32, 'Z_Contact': 88},
            {'Name': 'Gabriel Moreno', 'Hand': 'R', 'K_pct': 15.0, 'O_Swing': 28, 'Z_Contact': 92},
            {'Name': 'Alek Thomas', 'Hand': 'L', 'K_pct': 21.2, 'O_Swing': 33, 'Z_Contact': 85}
        ],
        'away_catcher': 'Henry Davis',
        'home_catcher': 'Gabriel Moreno',
        'away_drs': 5,
        'home_drs': 3,
        'away_manager_hook': 0.0,
        'home_manager_hook': 0.0,
        'away_bp_pitches_d1': 45,
        'away_bp_pitches_d2': 20,
        'home_bp_pitches_d1': 60,
        'home_bp_pitches_d2': 30
    }
    
    results = omni.run_omni_simulation(game_data, market_odds=market_odds)
    return results

if __name__ == "__main__":
    run_simulation()
