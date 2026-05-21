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
#!/usr/bin/env python3
"""
K Prophet V8.1 - Statcast Pipeline (Layer 6 Convergence)
This module acts as the ingestion layer for pybaseball's statcast data.
Currently uses mock data to simulate API responses for backtesting.
"""
import random
import math

class StatcastPipeline:
    def __init__(self):
        self.pitcher_baselines = {
            "Luis Severino": {"avg_velo": 96.5, "sd_release_x": 0.45, "sd_release_z": 0.38},
            "Michael Wacha": {"avg_velo": 93.0, "sd_release_x": 0.52, "sd_release_z": 0.41},
            "Tarik Skubal": {"avg_velo": 96.8, "sd_release_x": 0.35, "sd_release_z": 0.31},
        }

    def fetch_pitcher_baseline(self, pitcher_name: str, season: int = 2026) -> dict:
        """
        Simulates `pybaseball.statcast_pitcher(start_dt, end_dt, player_id)` to get 
        the yearly averages for release metrics.
        """
        return self.pitcher_baselines.get(pitcher_name, {"avg_velo": 94.0, "sd_release_x": 0.5, "sd_release_z": 0.5})

    def fetch_live_telemetry(self, game_id: str, pitcher_name: str) -> dict:
        """
        Simulates fetching the first 15 pitches of a live game via pybaseball.statcast()
        to calculate Layer 6 drift.
        """
        baseline = self.fetch_pitcher_baseline(pitcher_name)
        
        # Inject deterministic noise to simulate real games
        velo_noise = random.uniform(-1.8, 0.5)
        release_noise = random.uniform(0.1, 7.5) # mm drift
        
        live_velo = baseline["avg_velo"] + velo_noise
        
        return {
            "Live_Velo_Delta": round(live_velo - baseline["avg_velo"], 1),
            "Live_Release_SD_Drift": round(release_noise, 1)
        }

    def fetch_historical_slate(self, date_str: str) -> list:
        """
        Simulates pulling all starting pitchers and their actual strikeout totals 
        from a historical date.
        """
        # Mocking an April 2026 backtest date
        return [
            {"Pitcher": "Luis Severino", "Team": "ATH", "Actual_Ks": 4, "Score_Context": "Neutral"},
            {"Pitcher": "Michael Wacha", "Team": "KC", "Actual_Ks": 1, "Score_Context": "Trailing_Big"},
            {"Pitcher": "Tarik Skubal", "Team": "DET", "Actual_Ks": 9, "Score_Context": "Leading_Close"},
        ]