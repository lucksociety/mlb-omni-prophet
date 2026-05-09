from omni_prophet_v16 import OmniProphetV16

# OMNI-PROPHET V17.0 SIMULATION: CIN @ CHC
# DATE: 2026-05-07
# LOCATION: Wrigley Field (Chicago, IL)

game_data = {
    'away_team': 'CIN',
    'home_team': 'CHC',
    'game_time': '14:20',
    'is_dome': False,
    'park_factor': 105,  # Wrigley is generally hitters' park with wind out
    
    # Starting Pitchers
    'away_sp_name': 'Rhett Lowder',
    'home_sp_name': 'Shota Imanaga',
    'away_sp_hand': 'R',
    'home_sp_hand': 'L',
    'away_sp_era': 5.09,
    'home_sp_era': 2.40,
    
    'away_sp_statcast': {
        'Full Name': 'Rhett Lowder',
        'Hand': 'R',
        'ERA': 5.09,
        'Stuff': 95,      # Estimated
        'VAA': -4.5,      # Estimated
        'K_pct': 17.9,
        'BB_pct': 7.1,
        'IP': 29.0,
        'xERA': 3.98,
        'HardHit_pct': 37.1,
        'Barrel_pct': 7.6,
        'xFIP': 4.32
    },
    
    'home_sp_statcast': {
        'Full Name': 'Shota Imanaga',
        'Hand': 'L',
        'ERA': 2.40,
        'Stuff': 115,     # Estimated from high-spin FB reputation
        'VAA': -4.1,      # Estimated
        'K_pct': 28.6,
        'BB_pct': 6.8,
        'IP': 22.0,
        'xERA': 2.92,
        'HardHit_pct': 41.9,
        'Barrel_pct': 9.3,
        'xFIP': 3.47
    },
    
    'away_lineup_names': ['Dane Myers', 'Matt McLain', 'Elly De La Cruz', 'Sal Stewart', 'Spencer Steer', 'Tyler Stephenson', 'JJ Bleday', 'Blake Dunn', 'Ke\'Bryan Hayes'],
    'away_lineup_hands': ['R', 'R', 'S', 'R', 'R', 'R', 'L', 'R', 'R'],
    'away_lineup_statcast': [
        {'K_pct': 24.0, 'O_Swing': 32.0, 'Z_Contact': 81.0}, # Dane Myers
        {'K_pct': 14.3, 'O_Swing': 22.0, 'Z_Contact': 90.0}, # Matt McLain
        {'K_pct': 32.4, 'O_Swing': 38.0, 'Z_Contact': 72.0}, # Elly De La Cruz
        {'K_pct': 14.8, 'O_Swing': 25.0, 'Z_Contact': 88.0}, # Sal Stewart
        {'K_pct': 19.2, 'O_Swing': 28.0, 'Z_Contact': 85.0}, # Spencer Steer
        {'K_pct': 18.5, 'O_Swing': 31.0, 'Z_Contact': 82.0}, # Tyler Stephenson
        {'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 80.0}, # JJ Bleday
        {'K_pct': 25.0, 'O_Swing': 30.0, 'Z_Contact': 80.0}, # Blake Dunn
        {'K_pct': 17.2, 'O_Swing': 29.0, 'Z_Contact': 86.0}  # Ke'Bryan Hayes
    ],
    
    'home_lineup_names': ['Nico Hoerner', 'Moisés Ballesteros', 'Alex Bregman', 'Ian Happ', 'Michael Busch', 'Michael Conforto', 'Dansby Swanson', 'Pete Crow-Armstrong', 'Miguel Amaya'],
    'home_lineup_hands': ['R', 'L', 'R', 'S', 'L', 'L', 'R', 'L', 'R'],
    'home_lineup_statcast': [
        {'K_pct': 8.1,  'O_Swing': 18.0, 'Z_Contact': 94.0}, # Nico Hoerner
        {'K_pct': 21.0, 'O_Swing': 31.0, 'Z_Contact': 83.0}, # Moisés Ballesteros
        {'K_pct': 13.0, 'O_Swing': 23.0, 'Z_Contact': 91.0}, # Alex Bregman
        {'K_pct': 30.4, 'O_Swing': 35.0, 'Z_Contact': 78.0}, # Ian Happ
        {'K_pct': 26.6, 'O_Swing': 33.0, 'Z_Contact': 80.0}, # Michael Busch
        {'K_pct': 24.0, 'O_Swing': 31.0, 'Z_Contact': 81.0}, # Michael Conforto
        {'K_pct': 19.5, 'O_Swing': 28.0, 'Z_Contact': 85.0}, # Dansby Swanson
        {'K_pct': 26.9, 'O_Swing': 33.0, 'Z_Contact': 79.0}, # Pete Crow-Armstrong
        {'K_pct': 24.0, 'O_Swing': 31.0, 'Z_Contact': 81.0}  # Miguel Amaya
    ],
    
    'env': {
        'Weather': {'temp': 56, 'wind_speed': 11, 'wind_dir': 0, 'humidity': 50},
        'altitude': 600,
        'rain_intensity': 0.2, # 36% precipitation risk
        'Umpire': {'name': 'Unknown', 'CS_pct': 16.5, 'zone_type': 'neutral'}
    },
    
    'away_drs': -2,  # Reds defense struggling
    'home_drs': 5,   # Cubs defense solid
    'away_manager_hook': 0.2,
    'home_manager_hook': -0.1, # Cubs trust Imanaga
    'away_bp_pitches_d1': 40,
    'away_bp_pitches_d2': 25,
    'home_bp_pitches_d1': 30,
    'home_bp_pitches_d2': 20,
    'away_catcher': 'Tyler Stephenson',
    'home_catcher': 'Miguel Amaya',
}

market_odds = {
    'CHC ML': -193,
    'CIN ML': 158,
    'Total Over 9.0': -105,
    'Total Under 9.0': -115,
    'Lowder Over 3.5 K': -120,
    'Lowder Under 3.5 K': -110,
    'Imanaga Over 6.5 K': 115,
    'Imanaga Under 6.5 K': -150,
    'YRFI (Yes)': -115,
    'NRFI (No)': -115,
    'CHC -1.5 RL': 105,
    'CIN +1.5 RL': -125,
}

if __name__ == "__main__":
    omni = OmniProphetV16()
    omni.run_omni_simulation(game_data, market_odds=market_odds)
