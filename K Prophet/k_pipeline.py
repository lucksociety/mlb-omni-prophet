import os
from engine import KProphetEngine
from typing import Dict, List

class KProphetMaster:
    """
    K PROPHET V10.0 — Pipeline Master
    Coordinates data flow between the Runner and the Physics Engine.
    """
    def __init__(self):
        self.engine = KProphetEngine()

    def get_momentum_factor(self, pitcher_name: str) -> float:
        """Analyze recent performance from the results CSV to determine 'Hot/Cold' state."""
        results_path = "/Users/danielreiss/Desktop/Antigravity/MLB/MLB + Strikeouts - Sheet1.csv"
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
                    print(f"DEBUG [Momentum]: {pitcher_name} | Pred: {pred} | Res: {res}")
                    if res > pred + 1.5: overs += 1
                    if res < pred - 1.5: unders += 1
                
                # Net Momentum
                net = overs - unders
                if net > 0: momentum = 1.0 + (net * 0.10)
                if net < 0: momentum = 1.0 + (net * 0.08)
                
                if momentum != 1.0:
                    print(f"DEBUG [Momentum]: {pitcher_name} Net Momentum Applied: {momentum}")
        except Exception as e:
            print(f"DEBUG [Momentum] Error: {e}")
            pass
            
        return momentum

    def execute_pipeline(self, pitcher_data: Dict, lineup_data: List[Dict], env_data: Dict, manager_data: Dict, live_telemetry: Dict = None) -> Dict:
        """
        Adapts the Runner's data format to the Engine's requirements.
        """
        # Build overrides bundle
        overrides = {
            'PitchLimit': manager_data.get('PitchLimit', 92),
            'ShortLeash': pitcher_data.get('ShortLeash', False),
            'TTT_Penalty': pitcher_data.get('TTT_Penalty', 0.85),
            'Hot_Streak': self.get_momentum_factor(pitcher_data['Name'])
        }
        
        if live_telemetry:
            overrides.update(live_telemetry)

        # Call the V11.0 Unified Projection Interface
        return self.engine.project(pitcher_data, lineup_data, env_data, overrides)
