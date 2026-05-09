#!/usr/bin/env python3
"""
MLB OMNI-PROPHET V14.0 — UNIFIED FORENSIC ARCHITECTURE
Merges: Score (Quant-Elite), K-Prophet (DRE), and HR-Alpha engines.
"""
import sys
import os
import json
import statistics
from datetime import datetime

# Add subdirectories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'K Prophet'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'HR'))

try:
    from engine import KProphetEngine
    from hr_model import HRModel
    import quant_elite_v6_5 as qe
except ImportError as e:
    print(f"⚠ CRITICAL ERROR: Could not import required engines. {e}")
    sys.exit(1)

class OmniProphetV14:
    def __init__(self):
        self.k_engine = KProphetEngine()
        self.hr_engine = HRModel(os.path.join(os.path.dirname(__file__), "HR/MLB Stats"))
        self.qe = qe

    def run_omni_simulation(self, game_data):
        """
        Executes the unified forensic simulation.
        game_data should contain all necessary fields for all three engines.
        """
        print(f"激活 OMNI-PROPHET V14.0 ...")
        
        # 1. RUN K-PROPHET ENGINE
        print(f"  [1/3] Running K-Prophet V11.0 Engine...")
        away_k_proj = self.k_engine.project(
            game_data['away_sp_statcast'], 
            game_data['home_lineup_statcast'], 
            game_data['env'],
            game_data.get('away_sp_overrides')
        )
        home_k_proj = self.k_engine.project(
            game_data['home_sp_statcast'], 
            game_data['away_lineup_statcast'], 
            game_data['env'],
            game_data.get('home_sp_overrides')
        )

        # 2. RUN HR-ALPHA ENGINE
        print(f"  [2/3] Running HR-Alpha Engine...")
        hr_picks = []
        # Away Lineup vs Home SP
        for i, batter in enumerate(game_data['away_lineup_names']):
            prob = self.hr_engine.calculate_hr_probability(
                batter, game_data['home_sp_name'], batter_index=i,
                opp_team_name=game_data['home_team'],
                park_factor=game_data['park_factor'],
                temp=game_data['env']['Weather']['temp'],
                wind_speed=game_data['env']['Weather']['wind_speed'],
                wind_dir=game_data['env']['Weather']['wind_dir'],
                pitcher_hand=game_data['home_sp_hand'],
                umpire_name=game_data['env']['Umpire']['name'],
                lineup=game_data['away_lineup_names']
            )
            if prob > 0.15: # Only track relevant ones
                hr_picks.append({'player': batter, 'team': game_data['away_team'], 'prob': prob})
        
        # Home Lineup vs Away SP
        for i, batter in enumerate(game_data['home_lineup_names']):
            prob = self.hr_engine.calculate_hr_probability(
                batter, game_data['away_sp_name'], batter_index=i,
                opp_team_name=game_data['away_team'],
                park_factor=game_data['park_factor'],
                temp=game_data['env']['Weather']['temp'],
                wind_speed=game_data['env']['Weather']['wind_speed'],
                wind_dir=game_data['env']['Weather']['wind_dir'],
                pitcher_hand=game_data['away_sp_hand'],
                umpire_name=game_data['env']['Umpire']['name'],
                lineup=game_data['home_lineup_names']
            )
            if prob > 0.15:
                hr_picks.append({'player': batter, 'team': game_data['home_team'], 'prob': prob})
        
        hr_picks.sort(key=lambda x: x['prob'], reverse=True)

        # 3. RUN QUANT-ELITE SCORE ENGINE
        print(f"  [3/3] Running Quant-Elite V6.5 Score Engine...")
        # Prepare lineups in (Name, Hand) format for QE
        away_lineup_qe = list(zip(game_data['away_lineup_names'], game_data['away_lineup_hands']))
        home_lineup_qe = list(zip(game_data['home_lineup_names'], game_data['home_lineup_hands']))
        
        ar, hr, a_k, h_k = self.qe.run_v6_5_protocol(
            game_data['away_team'], game_data['home_team'], 
            game_data['away_sp_name'], game_data['home_sp_name'],
            game_data['away_sp_hand'], game_data['home_sp_hand'],
            game_data['away_sp_era'], game_data['home_sp_era'],
            away_lineup_qe, home_lineup_qe,
            game_data['park_factor'], game_data['is_dome'],
            game_data['env']['Weather']['temp'], 
            game_data['env']['Weather']['wind_speed'],
            game_data['env']['Weather']['wind_dir'],
            game_data['env']['Weather']['humidity'],
            game_data['env']['altitude'],
            game_data['env']['rain_intensity'],
            game_data['away_drs'], game_data['home_drs'],
            game_data['away_manager_hook'], game_data['home_manager_hook'],
            game_data['away_bp_pitches_d1'], game_data['away_bp_pitches_d2'],
            game_data['home_bp_pitches_d1'], game_data['home_bp_pitches_d2'],
            game_data['env']['Umpire']['zone_type'],
            game_data['away_catcher'], game_data['home_catcher'],
            game_data['game_time']
        )

        # 4. AGGREGATE & FORMAT OUTPUT
        self.print_final_report(game_data, away_k_proj, home_k_proj, hr_picks, ar, hr, a_k, h_k)

    def print_final_report(self, game_data, akp, hkp, hr_picks, ar, hr, a_k, h_k):
        n = len(ar)
        away_mu = sum(ar)/n
        home_mu = sum(hr)/n
        apct = (sum(1 for i in range(n) if ar[i]>hr[i]) + sum(1 for i in range(n) if ar[i]==hr[i])*0.48)/n*100
        hpct = (sum(1 for i in range(n) if hr[i]>ar[i]) + sum(1 for i in range(n) if ar[i]==hr[i])*0.52)/n*100
        total_mu = away_mu + home_mu
        blowout_prob = sum(1 for i in range(n) if ar[i]+hr[i] > 13) / n * 100

        print("\n" + "="*80)
        print(f"      MLB OMNI-PROPHET V14.0 | FORENSIC INTELLIGENCE REPORT")
        print(f"      {game_data['away_team']} @ {game_data['home_team']} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*80)
        
        print(f"\n── 1. SCORE PROJECTION & WIN PROBABILITIES ──────────────────────")
        print(f"  {game_data['away_team']}: {away_mu:.2f} runs ({apct:.1f}%)")
        print(f"  {game_data['home_team']}: {home_mu:.2f} runs ({hpct:.1f}%)")
        print(f"  PROJECTED TOTAL: {total_mu:.2f} | Blowout Prob: {blowout_prob:.1f}%")

        print(f"\n── 2. K-PROPHET PRECISION (V11.0) ───────────────────────────────")
        print(f"  {game_data['away_sp_name']}: {akp['exact_k']} K's (Mean: {akp['mean_k']:.2f}, EBF: {akp['telemetry']['ExpectedBF']:.1f})")
        print(f"  {game_data['home_sp_name']}: {hkp['exact_k']} K's (Mean: {hkp['mean_k']:.2f}, EBF: {hkp['telemetry']['ExpectedBF']:.1f})")

        print(f"\n── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ────────────────────────")
        high_conv = [h for h in hr_picks if h['prob'] >= 0.25]
        if not high_conv:
            print("  [NONE DETECTED]")
        for h in high_conv:
            print(f"  🔥 {h['player']} ({h['team']}): {h['prob']*100:.1f}%")

        print(f"\n── 4. FORENSIC TELEMETRY ────────────────────────────────────────")
        print(f"  ADI: {game_data['env'].get('adi', 'N/A')} | Park Factor: {game_data['park_factor']}")
        print(f"  Umpire: {game_data['env']['Umpire']['name']} ({game_data['env']['Umpire']['zone_type']})")
        print(f"  Shadow Dynamics: {'ACTIVE' if '16:' in game_data['game_time'] else 'INACTIVE'}")
        
        print("\n" + "="*80)

if __name__ == "__main__":
    # Test stub for integration verification
    omni = OmniProphetV14()
    # Dummy data for test
    test_game = {
        'away_team': 'LAA', 'home_team': 'KCR',
        'away_sp_name': 'Walbert Urena', 'home_sp_name': 'Cole Ragans',
        'away_sp_hand': 'R', 'home_sp_hand': 'L',
        'away_sp_era': 2.35, 'home_sp_era': 6.00,
        'away_lineup_names': ['Neto', 'Trout', 'Adell', 'Soler', 'Peraza', 'Schanuel', 'Grissom', 'O\'Hoppe', 'Teodosio'],
        'away_lineup_hands': ['R', 'R', 'R', 'R', 'R', 'L', 'R', 'R', 'R'],
        'home_lineup_names': ['Garcia', 'Witt', 'Pasquantino', 'Perez', 'Jensen', 'Massey', 'Caglianone', 'Collins', 'Isbel'],
        'home_lineup_hands': ['R', 'R', 'L', 'R', 'L', 'L', 'L', 'S', 'L'],
        'park_factor': 101, 'is_dome': False, 'game_time': '19:10',
        'away_sp_statcast': {'Name': 'Walbert Urena', 'Stuff': 105, 'VAA': -4.8, 'K_pct': 21.0, 'BB_pct': 9.0, 'IP': 20, 'Hand': 'R', 'xERA': 4.2},
        'home_sp_statcast': {'Name': 'Cole Ragans', 'Stuff': 118, 'VAA': -3.9, 'K_pct': 28.5, 'BB_pct': 7.5, 'IP': 120, 'Hand': 'L', 'xERA': 3.1},
        'away_lineup_statcast': [{'Name': n, 'Hand': h, 'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 85.0} for n, h in zip(['Neto', 'Trout'], ['R', 'R'])], # Shortened for test
        'home_lineup_statcast': [{'Name': n, 'Hand': h, 'K_pct': 20.0, 'O_Swing': 28.0, 'Z_Contact': 88.0} for n, h in zip(['Garcia', 'Witt'], ['R', 'R'])],
        'env': {
            'Weather': {'temp': 62, 'wind_speed': 9, 'wind_dir': 60, 'humidity': 50},
            'Umpire': {'name': 'Pat Hoberg', 'zone_type': 'neutral', 'CS_pct': 16.5},
            'altitude': 912, 'rain_intensity': 0.0, 'adi': 102.5
        },
        'away_drs': 0, 'home_drs': 0, 'away_manager_hook': 0.0, 'home_manager_hook': 0.0,
        'away_bp_pitches_d1': 0, 'away_bp_pitches_d2': 0,
        'home_bp_pitches_d1': 0, 'home_bp_pitches_d2': 0,
        'away_catcher': 'O\'Hoppe', 'home_catcher': 'Perez'
    }
    # Fix the test lineup statcast to match length of names for safety
    test_game['away_lineup_statcast'] = [{'Name': n, 'Hand': h, 'K_pct': 22.0, 'O_Swing': 30.0, 'Z_Contact': 85.0} for n, h in zip(test_game['away_lineup_names'], test_game['away_lineup_hands'])]
    test_game['home_lineup_statcast'] = [{'Name': n, 'Hand': h, 'K_pct': 20.0, 'O_Swing': 28.0, 'Z_Contact': 88.0} for n, h in zip(test_game['home_lineup_names'], test_game['home_lineup_hands'])]
    
    omni.run_omni_simulation(test_game)
