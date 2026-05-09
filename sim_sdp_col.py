from parse_and_sim_std import *

def simulate_sdp_col():
    sections = parse_multi_csv('MLB Stats')
    
    sdp_batters = ["Ramón Laureano", "Fernando Tatis Jr.", "Jackson Merrill", "Manny Machado", "Xander Bogaerts", "Gavin Sheets", "Ty France", "Freddy Fermin", "Jake Cronenworth"]
    col_batters = ["Edouard Julien", "Mickey Moniak", "Hunter Goodman", "Tyler Freeman", "TJ Rumfield", "T. Johnston", "Ezequiel Tovar", "Kyle Karros", "Brenton Doyle"]
    
    def get_lineup_wrc(names, team):
        wrcs = []
        for name in names:
            # simple match
            for b in sections.get('Batting Advanced', []):
                if name.split()[-1] in b.get('Name', '') and b.get('wRC+'):
                    wrcs.append(float(b['wRC+']))
                    break
        return sum(wrcs)/len(wrcs) if wrcs else 100.0

    away_wrc = get_lineup_wrc(sdp_batters, 'SDP')
    home_wrc = get_lineup_wrc(col_batters, 'COL')
    
    away_bp_era = get_bp_era(sections, 'SDP', 'Walker Buehler')
    home_bp_era = get_bp_era(sections, 'COL', 'Tomoyuki Sugano')
    
    # Pitcher Stats from Screenshot
    # Buehler 4.58 ERA, Sugano 3.92 ERA. We'll use this as their true-talent baseline since they aren't in the CSV.
    away_sp_era = 4.58
    home_sp_era = 3.92
    
    game_params = {
        'away_sp_era':       away_sp_era,
        'away_bp_era':       away_bp_era,
        'away_sp_ip':        5.5,
        'away_lineup_wrc':   away_wrc,
        'home_sp_era':       home_sp_era,
        'home_bp_era':       home_bp_era,
        'home_sp_ip':        5.5,
        'home_lineup_wrc':   home_wrc,
        'park_factor':       114, # Coors Field is extremely hitter friendly
        'wind_speed':        21,
        'wind_angle':        90, # L-R crosswind
        'temperature':       80,
    }
    
    meta_data = dict(game_params)
    meta_data['Away_Team'] = 'SDP'
    meta_data['Home_Team'] = 'COL'
    meta_data['Away_SP_Name'] = 'Walker Buehler'
    meta_data['Home_SP_Name'] = 'Tomoyuki Sugano'
    meta_data['Away_SP_xFIP'] = 4.58
    meta_data['Home_SP_xFIP'] = 3.92
    meta_data['Away_SP_SIERA'] = 4.58
    meta_data['Home_SP_SIERA'] = 3.92
    meta_data['Away_SP_SwStr'] = 'N/A'
    meta_data['Home_SP_SwStr'] = 'N/A'
    meta_data['Away_SP_Stuff'] = 'N/A'
    meta_data['Home_SP_Stuff'] = 'N/A'
    meta_data['Away_SP_ERA_26'] = 4.58
    meta_data['Home_SP_ERA_26'] = 3.92

    away_runs, home_runs, away_mean, home_mean = run_simulation(**game_params)
    analyze_results(away_runs, home_runs, away_mean, home_mean, meta_data)

if __name__ == '__main__':
    simulate_sdp_col()
