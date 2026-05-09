import csv
import json
import os
from typing import Dict, Any, List, Optional

class NRFI_DataLoader:
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.base_path = base_path
        self.k_prophet_path = os.path.join(base_path, "K Prophet")
        self.data_path = os.path.join(self.k_prophet_path, "data")
        
        self.pitchers = {}
        self.batters = {}
        self.overrides = {}
        self.games_data = []

        self._load_data()

    def _load_csv(self, filename: str) -> List[Dict[str, str]]:
        path = os.path.join(self.data_path, filename)
        if not os.path.exists(path):
            print(f"Warning: {path} not found.")
            return []
        
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def _load_data(self):
        # 1. Load Overrides
        overrides_path = os.path.join(self.data_path, "overrides.json")
        if os.path.exists(overrides_path):
            with open(overrides_path, 'r') as f:
                self.overrides = json.load(f).get("Pitchers", {})

        def safe_float(val, default=0.0):
            if val is None: return default
            try:
                return float(str(val).replace('%', '').strip() or default)
            except:
                return default

        # 2. Load Pitching Advanced from root "MLB Stats"
        mlb_stats_path = os.path.join(self.base_path, "MLB Stats")
        if os.path.exists(mlb_stats_path):
            current_section = None
            headers = []
            with open(mlb_stats_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or not any(row): continue
                    fv = row[0].strip()
                    if fv in ["Batting Advanced", "Pitching Advanced"]:
                        current_section = fv
                        headers = []
                        continue
                    if current_section == "Pitching Advanced":
                        if fv == '#' and not headers:
                            headers = [h.strip() for h in row]
                            continue
                        if headers and fv != '#':
                            row_dict = dict(zip(headers, row))
                            name = row_dict.get("Name")
                            if name:
                                self.pitchers[name] = {
                                    "K_pct": safe_float(row_dict.get("K%"), 0.0),
                                    "BB_pct": safe_float(row_dict.get("BB%"), 0.0),
                                    "xFIP": safe_float(row_dict.get("xFIP"), 4.0),
                                    "xERA": safe_float(row_dict.get("xFIP"), 4.0),
                                    "Team": row_dict.get("Team")
                                }
                    elif current_section == "Batting Advanced":
                        if fv == '#' and not headers:
                            headers = [h.strip() for h in row]
                            continue
                        if headers and fv != '#':
                            row_dict = dict(zip(headers, row))
                            name = row_dict.get("Name")
                            if name:
                                self.batters[name] = {
                                    "PA": int(safe_float(row_dict.get("PA"), 0)),
                                    "K_pct": safe_float(row_dict.get("K%"), 0.0),
                                    "BB_pct": safe_float(row_dict.get("BB%"), 0.0),
                                    "wRC_plus": safe_float(row_dict.get("wRC+"), 100.0),
                                    "Team": row_dict.get("Team")
                                }
        else:
            # Fallback to legacy csv loading if root file missing
            pitching_adv = self._load_csv("pitching_advanced.csv")
            for row in pitching_adv:
                name = row.get("Name")
                if name:
                    self.pitchers[name] = {
                        "K_pct": safe_float(row.get("K_pct"), 0.0),
                        "BB_pct": safe_float(row.get("BB_pct"), 0.0),
                        "xFIP": safe_float(row.get("xFIP"), 4.0),
                        "Team": row.get("Team")
                    }

        # 3. Load Pitching Plus (Stuff+, etc)
        pitching_plus = self._load_csv("pitching_plus.csv")
        for row in pitching_plus:
            name = row.get("Name")
            if name in self.pitchers:
                self.pitchers[name]["Stuff"] = float(row.get("Stuff", 100) or 100)
                self.pitchers[name]["IP"] = float(row.get("IP", 0) or 0)

        # 4. Apply Pitcher Overrides
        for name, data in self.overrides.items():
            if name not in self.pitchers:
                self.pitchers[name] = {}
            self.pitchers[name].update(data)

    def get_pitcher(self, name: str) -> Dict[str, Any]:
        return self.pitchers.get(name, {
            "K_pct": 22.7,
            "BB_pct": 8.5,
            "Stuff": 100,
            "xFIP": 4.0,
            "xERA": 4.0
        })

    def get_batter(self, name: str) -> Dict[str, Any]:
        return self.batters.get(name, {
            "PA": 100,
            "K_pct": 22.7,
            "BB_pct": 8.5,
            "wRC_plus": 100
        })

    def get_team_top_batters(self, team: str, count: int = 5) -> List[Dict[str, Any]]:
        team_batters = [
            {"Name": name, **data} 
            for name, data in self.batters.items() 
            if data["Team"] == team or team in (data["Team"] or "")
        ]
        # Sort by PA as a proxy for being a regular starter / top of lineup
        team_batters.sort(key=lambda x: x["PA"], reverse=True)
        return team_batters[:count]

if __name__ == "__main__":
    loader = NRFI_DataLoader()
    print(f"Loaded {len(loader.pitchers)} pitchers and {len(loader.batters)} batters.")
    test_p = "Zack Wheeler"
    print(f"Stats for {test_p}: {loader.get_pitcher(test_p)}")
