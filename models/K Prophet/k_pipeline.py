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
import os
from engine import KProphetEngine
from typing import Dict, List
from intelligence_hub import HUB

class KProphetMaster:
    """
    K PROPHET V10.0 — Pipeline Master
    Coordinates data flow between the Runner and the Physics Engine.
    """
    def __init__(self):
        self.engine = KProphetEngine()

    def get_momentum_factor(self, pitcher_name: str) -> float:
        """Analyze recent performance from the results CSV to determine 'Hot/Cold' state."""
        results_path = "/Users/danielreiss/Desktop/Antigravity/MLB/data/MLB + Strikeouts - Sheet1.csv"
        if not os.path.exists(results_path):
            return 1.0
            
        momentum = 1.0
        overs = 0
        unders = 0
        
        last_name = pitcher_name.split(' ')[-1]
        
        try:
            with open(results_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                # Find the most recent 3 occurrences of the pitcher
                matches = []
                for line in lines:
                    if last_name in line:
                        parts = line.split(',')
                        # Find which part is the pitcher's name and look for result
                        for i, part in enumerate(parts):
                            if last_name in part:
                                try:
                                    pred = float(parts[i+1])
                                    result = float(parts[i+3])
                                    matches.append((pred, result))
                                except:
                                    continue
                
                # Analyze last 2 starts
                recent = matches[-2:]
                for pred, res in recent:
                    if res > pred + 1.5: overs += 1
                    if res < pred - 1.5: unders += 1
                
                # Net Momentum
                net = overs - unders
                if net > 0: momentum = 1.0 + (net * 0.10)
                if net < 0: momentum = 1.0 + (net * 0.08)
                
        except Exception as e:
            pass
            
        return momentum

    def calculate_rolling_calibration(self) -> Dict:
        """
        Step 0: Rolling Calibration
        Computes DBS, BF Multiplier, and Under Gate status from performance_tracker.csv.
        """
        tracker_path = os.path.join(os.path.dirname(__file__), 'performance_tracker.csv')
        if not os.path.exists(tracker_path):
            return {'DBS': 0.0, 'BF_Multiplier': 1.0, 'Under_Gate': False, 'Flags': ['CAL_INSUFFICIENT']}
            
        overs_wrong = 0
        unders_wrong = 0
        under_hits = 0
        total_picks = 0
        
        try:
            import csv
            with open(tracker_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                # Filter for the last 20 completed picks
                completed = [r for r in rows if r.get('Result') in ['Win', 'Loss']]
                recent = completed[-20:]
                
                if len(recent) < 10:
                    return {'DBS': 0.0, 'BF_Multiplier': 1.0, 'Under_Gate': False, 'Flags': ['CAL_INSUFFICIENT']}
                
                for r in recent:
                    total_picks += 1
                    bet = r.get('Bet', '')
                    result = r.get('Result', '')
                    
                    if 'Under' in bet:
                        if result == 'Win': under_hits += 1
                        else: unders_wrong += 1
                    elif 'Over' in bet:
                        if result == 'Loss': overs_wrong += 1
                
                dbs = (overs_wrong - unders_wrong) / total_picks
                under_hit_rate = under_hits / sum(1 for r in recent if 'Under' in r.get('Bet', '')) if any('Under' in r.get('Bet', '') for r in recent) else 0.0
                
                bf_mult = 1.0
                flags = []
                if dbs > 0.20:
                    bf_mult = max(0.85, 1.0 - (dbs * 0.25))
                    flags.append('BF_DRIFT_DOWN')
                elif dbs < -0.20:
                    bf_mult = min(1.10, 1.0 + (abs(dbs) * 0.15))
                    flags.append('BF_DRIFT_UP')
                else:
                    flags.append('CAL_BALANCED')
                    
                under_gate = under_hit_rate >= 0.55
                if under_gate: flags.append('UNDER_GATE_ACTIVE')
                
                if abs(dbs) > 0.40: flags.append('CONVICTION_TIGHTENED')
                
                return {
                    'DBS': dbs,
                    'BF_Multiplier': bf_mult,
                    'Under_Gate': under_gate,
                    'Flags': flags
                }
        except Exception as e:
            return {'DBS': 0.0, 'BF_Multiplier': 1.0, 'Under_Gate': False, 'Flags': ['CAL_ERROR']}

    def execute_pipeline(self, pitcher_data: Dict, lineup_data: List[Dict], env_data: Dict, manager_data: Dict, live_telemetry: Dict = None) -> Dict:
        """
        Adapts the Runner's data format to the Engine's requirements.
        """
        calibration = self.calculate_rolling_calibration()
        
        # Build overrides bundle
        overrides = {
            'PitchLimit': manager_data.get('PitchLimit', 92),
            'ShortLeash': pitcher_data.get('ShortLeash', False),
            'TTT_Penalty': pitcher_data.get('TTT_Penalty', 0.85),
            'Hot_Streak': self.get_momentum_factor(pitcher_data.get('Name', 'Unknown')),
            'Calibration': calibration,
            'BF_Multiplier': calibration['BF_Multiplier']
        }
        
        if live_telemetry:
            overrides.update(live_telemetry)

        # Call the V11.0 Unified Projection Interface
        result = self.engine.project(pitcher_data, lineup_data, env_data, overrides)
        
        # V20 SYNC: Export to Intelligence Hub
        p_name = pitcher_data.get('Name', 'Unknown')
        game_id = env_data.get('GameID')
        
        HUB.set(f"Stuff_{p_name}", pitcher_data.get('Stuff', 100), game_id=game_id)
        HUB.set(f"Archetype_{p_name}", result.get('telemetry', {}).get('Archetype', 'Standard'), game_id=game_id)
        HUB.set(f"Umpire_Bias", env_data.get('Umpire', {}).get('zone_type', 'neutral'), game_id=game_id)
        
        return result