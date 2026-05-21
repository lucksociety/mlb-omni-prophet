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
import math
import os
import csv
import json
from data_loader import DataLoader
from games_data import GAMES
from intelligence_hub import HUB

# ═══════════════════════════════════════════════════════════════
# LEAGUE BASELINES (2026 season)
# ═══════════════════════════════════════════════════════════════
LEAGUE_AVG_ISO = 0.155
LEAGUE_AVG_HR_PA = 0.031      # ~3.1% league-wide
LEAGUE_AVG_BARREL_PCT = 0.075
LEAGUE_AVG_EXIT_VELO = 88.5
LEAGUE_AVG_EV90 = 104.5
LEAGUE_AVG_HR9 = 1.15
LEAGUE_AVG_GB_PCT = 0.43
LEAGUE_AVG_LA = 11.2          # Avg Launch Angle
LEAGUE_AVG_XFIP = 4.10
LEAGUE_AVG_STUFF = 100
LEAGUE_AVG_BARREL_ALLOWED = 0.08  # 8% barrel rate against

# Layer 1: Power Gate Thresholds
POWER_GATE_ISO = 0.220
POWER_GATE_BARREL = 0.10
POWER_GATE_EV90 = 108.0

# Layer 1: Elite Thresholds
ELITE_ISO = 0.250
ELITE_BARREL = 0.15
ELITE_EV90 = 111.0

# Calibration constant: scales raw λ down to realistic probabilities
# V6.0 Bible: Calibrated for high-vulnerability synergy states.
CALIBRATION = 0.285

# Bullpen Quality Anchors (from Quant-Elite output)
BULLPEN_XFIP = {
    "Guardians": 3.93, "Orioles": 3.51, "Reds": 4.46, "Phillies": 4.02,
    "Pirates": 3.75, "Blue Jays": 2.75, "Mets": 3.65, "Braves": 3.83,
    "White Sox": 4.38, "Brewers": 3.81, "Twins": 4.59, "Rangers": 3.86,
    "Athletics": 4.34, "Padres": 3.51, "Dodgers": 3.67, "Mariners": 4.02,
    "Astros": 4.49, "Diamondbacks": 3.94, "Tigers": 4.12, "Royals": 4.46,
    "Cubs": 3.92, "Nationals": 4.80, "Rockies": 3.94, "Angels": 4.34,
    "Marlins": 4.41, "Red Sox": 3.85, "Yankees": 3.56, "Rays": 4.42,
    "Giants": 3.85, "Cardinals": 4.67
}


class HRModel:
    """World-class MLB Home Run prediction engine.
    
    Integrates:
    - Split-specific ISO for base rates
    - Pitcher quality from 4 data sources (MLB Stats, pitching_advanced, 
      pitching_statcast, pitching_plus, overrides.json, K Profit CSW%)
    - Statcast quality weights (Barrel%, EV, xwOBA)
    - Environmental adjustments (park factor, temp, wind vector)
    - Umpire strike zone tendencies
    - Calibrated Monte Carlo probability engine
    """

    def __init__(self, stats_path):
        self.loader = DataLoader(stats_path)
        
        # Primary data from MLB Stats file
        self.batting_adv = self.loader.get_section("Batting Advanced")
        self.batting_sc = self.loader.get_section("Batting Stat Cast")
        self.pitching_adv_main = self.loader.get_section("Pitching Advanced")
        self.pitching_sc_main = self.loader.get_section("Pitching Statcast")
        self.splits_rhp = self.loader.get_section("Batting Splits RHP")
        self.splits_lhp = self.loader.get_section("Batting Splits LHP")
        
        # Career data for multi-year anchors
        career_path = stats_path.replace(os.path.join(ROOT_DIR, 'data', "MLB Stats"), "MLB Stats Career")
        if not os.path.exists(career_path):
            career_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.path.join(ROOT_DIR, 'data', "MLB Stats Career.csv"))
        self.career_loader = DataLoader(career_path)
        self.pitching_car = self.career_loader.get_section("Pitching Advanced")
        self.batting_car = self.career_loader.get_section("Batting Advanced")

        # Secondary data from modular CSVs in data/
        self.pitching_adv_csv = self._load_csv("data/pitching_advanced.csv")
        self.pitching_sc_csv = self._load_csv("data/pitching_statcast.csv")
        self.pitching_plus_csv = self._load_csv("data/pitching_plus.csv")
        self.batting_sc_csv = self._load_csv("data/batting_statcast.csv")
        self.batting_adv_csv = self._load_csv("data/batting_advanced.csv")
        self.splits_lhp_csv = self._load_csv("data/batting_lhp.csv")
        self.splits_rhp_csv = self._load_csv("data/batting_rhp.csv")
        
        # Umpires
        self.umpires = {}
        ump_path = os.path.join(os.path.dirname(stats_path), "data/umpires.csv")
        if os.path.exists(ump_path):
            for row in self._load_csv(ump_path):
                try: self.umpires[row['Name']] = float(row['K_Factor'])
                except: pass
        
        # Overrides (manual data for pitchers missing from FanGraphs)
        self.overrides = {}
        override_path = os.path.join(os.path.dirname(stats_path), "data/overrides.json")
        if os.path.exists(override_path):
            with open(override_path, 'r') as f:
                data = json.load(f)
                self.overrides = data.get("Pitchers", {})
        
        # K Profit CSW% fallback
        self.k_profit = {}
        kp_path = os.path.join(os.path.dirname(stats_path), "K Profit Data - Sheet1.csv")
        if os.path.exists(kp_path):
            with open(kp_path, 'r') as f:
                lines = f.readlines()
                for line in lines[2:]:
                    parts = line.split(',')
                    if len(parts) > 13:
                        name = parts[1].strip()
                        try:
                            csw = float(parts[13].strip().replace('%', '')) / 100.0
                            self.k_profit[name] = csw
                        except: pass
        
        # Prospect Priors (for missing data)
        self.prospects = {}
        prospect_path = os.path.join(os.path.dirname(stats_path), "data/prospects.json")
        if os.path.exists(prospect_path):
            with open(prospect_path, 'r') as f:
                self.prospects = json.load(f)

        # Plate Discipline (Contact%)
        self.discipline = {}
        disc_path = os.path.join(os.path.dirname(stats_path), "data/batting_discipline.csv")
        if os.path.exists(disc_path):
            for row in self._load_csv(disc_path):
                try:
                    name = row['Name']
                    contact = float(row['Contact'].replace('%', ''))
                    self.discipline[name] = contact
                except: pass

        # Bullpen Attrition (Manual Overrides for tired/depleted bullpens)
        self.bp_attrition = {
            "Reds": 1.25,      # High usage last 2 days
            "Marlins": 1.15,
            "White Sox": 1.30, # Bullpen in "Tier C" state
        }

        # Hot Streak data (loaded from historical results)
        self.streak_multipliers = self._load_streak_data()

        # Manual overrides for pitchers with NO data anywhere
        self.manual_pitchers = {
            "Jacob deGrom":    {"hr9": 0.85, "xfip": 2.80, "gb_pct": 0.42, "stuff": 125, "barrel_allowed": 0.065, "note": "Elite stuff, low HR/9"},
            "Michael King":    {"hr9": 0.95, "xfip": 3.45, "gb_pct": 0.45, "stuff": 105, "barrel_allowed": 0.075, "note": "Solid SP"},
            "Braxton Ashcraft": {"hr9": 0.80, "xfip": 3.20, "gb_pct": 0.44, "stuff": 112, "barrel_allowed": 0.055, "note": "Elite prospect"},
            "Jordan Wicks":    {"hr9": 1.10, "xfip": 3.85, "gb_pct": 0.41, "stuff": 98,  "barrel_allowed": 0.085, "note": "LHP stabilizer"},
            "Leahy":           {"hr9": 1.45, "xfip": 4.60, "gb_pct": 0.38, "stuff": 92,  "barrel_allowed": 0.105, "note": "Gas Can risk"},
            "Payton Tolle":    {"hr9": 0.60, "xfip": 4.80, "gb_pct": 0.45, "stuff": 90,  "barrel_allowed": 0.09, "note": "AAA callup"},
            "Shohei Ohtani":   {"hr9": 0.80, "xfip": 3.10, "gb_pct": 0.45, "stuff": 120, "barrel_allowed": 0.050, "note": "Ace starter"},
            "Chase Burns":     {"hr9": 0.70, "xfip": 3.15, "gb_pct": 0.46, "stuff": 122, "barrel_allowed": 0.045, "note": "Elite rookie, 101mph"},
            "Trey Yesavage":   {"hr9": 1.05, "xfip": 3.55, "gb_pct": 0.43, "stuff": 108, "barrel_allowed": 0.075, "note": "Top prospect"},
            "Walker Buehler":  {"hr9": 1.25, "xfip": 3.95, "gb_pct": 0.42, "stuff": 102, "barrel_allowed": 0.090, "note": "Post-TJ recovery"},
            "Clay Holmes":     {"hr9": 0.45, "xfip": 2.95, "gb_pct": 0.62, "stuff": 110, "barrel_allowed": 0.040, "note": "Elite GB rate"},
        }

        # Manual overrides for batters missing from data files
        self.manual_batters = {
            "Munetaka Murakami": {"iso": 0.385, "wrc": 195, "barrel": 18.5, "ev": 94.5},
            "Yordan Alvarez": {"iso": 0.360, "wrc": 188, "barrel": 16.2, "ev": 93.8},
            "James Wood": {"iso": 0.285, "wrc": 165, "barrel": 17.5, "ev": 92.5},
            "Gunnar Henderson": {"iso": 0.310, "wrc": 172, "barrel": 12.7, "ev": 91.2},
            "Ben Rice": {"iso": 0.325, "wrc": 160, "barrel": 13.5, "ev": 90.5},
            "Jac Caglianone": {"iso": 0.255, "wrc": 140, "barrel": 14.0, "ev": 92.0},
            "Travis Bazzana": {"iso": 0.215, "wrc": 130, "barrel": 11.0, "ev": 90.0},
            "Brent Rooker": {"iso": 0.265, "wrc": 150, "barrel": 15.5, "ev": 91.5},
            "Isaac Paredes": {"iso": 0.128, "wrc": 93, "barrel": 5.5, "ev": 88.0},
            "JJ Bleday": {"iso": 0.202, "wrc": 105, "barrel": 8.5, "ev": 89.5},
            "Casey Schmitt": {"iso": 0.194, "wrc": 137, "barrel": 7.8, "ev": 89.2},
            "JJ Wetherholt": {"iso": 0.180, "wrc": 120, "barrel": 8.0, "ev": 90.0},
        }

        # Prospect Power Index (V5.0 Zero-Data Scaling)
        self.prospect_power_index = {
            "Drew Romo": 0.245,
            "Konnor Griffin": 0.255,
            "Brice Matthews": 0.235,
            "Victor Scott II": 0.185,
            "Colson Montgomery": 0.230,
            "Sam Antonacci": 0.210,
            "Alex Freeland": 0.220,
        }

    def _load_streak_data(self):
        """Load recent HR hitters and assign streak multipliers.
        V4.0: Homered in 3 of last 4 days: 1.40x.
        """
        multipliers = {}
        hr_path = os.path.join(os.path.dirname(__file__), "data/historical_results.json")
        if not os.path.exists(hr_path):
            return multipliers
        try:
            with open(hr_path, 'r') as f:
                history = json.load(f)
        except:
            return multipliers
        dates = sorted(history.keys(), reverse=True)
        if not dates:
            return multipliers
        from collections import Counter
        recent_hrs = Counter()
        for date in dates[:4]: # Check last 4 days
            for hr in history[date].get("actual_home_runs", []):
                recent_hrs[hr["player"]] += 1
        for player, count in recent_hrs.items():
            if count >= 3:
                multipliers[player] = 1.40  # White Hot
            elif count >= 2:
                multipliers[player] = 1.25  # Multi-day streak
            else:
                multipliers[player] = 1.15  # Recent HR
        return multipliers

    def _load_csv(self, path):
        """Load a CSV file into a list of dicts."""
        base = os.path.dirname(__file__)
        full = os.path.join(base, path) if not os.path.isabs(path) else path
        if not os.path.exists(full):
            return []
        rows = []
        with open(full, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows

    def _fuzzy(self, name, players):
        """Enhanced fuzzy match that handles abbreviations."""
        if not players:
            return None
        
        # Expand common abbreviations
        name_map = {
            "K. Griffin": "Konnor Griffin",
            "S. Antonacci": "Sam Antonacci",
            "A. Freeland": "Alex Freeland",
            "M. Harris": "Michael Harris II",
            "D. Smith": "Dominic Smith",
            "M. Dubon": "Mauricio Dubon",
            "M. Yastrzemski": "Mike Yastrzemski",
        }
        name = name_map.get(name, name)
        
        name_l = name.lower()
        last = name_l.split()[-1]
        
        # Exact match
        for p in players:
            if p.get('Name', '').lower() == name_l:
                return p
        # Last name match
        for p in players:
            if last in p.get('Name', '').lower():
                return p
        return None

    def _get_pitcher_data(self, name):
        """Multi-source pitcher lookup. Returns a unified dict of pitcher metrics.
        Priority: manual_pitchers > MLB Stats > data/pitching_*.csv > overrides.json > K Profit > defaults
        """
        result = {
            "hr9": LEAGUE_AVG_HR9,
            "xfip": LEAGUE_AVG_XFIP,
            "gb_pct": LEAGUE_AVG_GB_PCT,
            "la": LEAGUE_AVG_LA,
            "fip_spread": 0.0,
            "stuff": LEAGUE_AVG_STUFF,
            "ev90": LEAGUE_AVG_EV90,
            "barrel_allowed": LEAGUE_AVG_BARREL_ALLOWED,
            "hrfb": 12.0,
            "source": "default"
        }
        
        # Check manual overrides first (for pitchers we researched)
        if name in self.manual_pitchers:
            m = self.manual_pitchers[name]
            result.update(m)
            result["source"] = "manual_research"
            
        # V20 SYNC: Prefer live Stuff+ from K-Prophet if available
        live_stuff = HUB.get(f"Stuff_{name}")
        if live_stuff:
            result["stuff"] = live_stuff
            if result["source"] == "default":
                result["source"] = "k_prophet_live"
        
        if result["source"] != "default":
            return result
        
        # Check primary MLB Stats
        p_adv = self.loader.fuzzy_find_player(name, self.pitching_adv_main)
        if p_adv:
            try: result["hr9"] = float(p_adv.get('HR/9', result["hr9"]))
            except: pass
            try:
                gb = float(p_adv.get('GB%', '').replace('%', ''))
                result["gb_pct"] = gb / 100.0 if gb > 1 else gb
            except: pass
            try: result["xfip"] = float(p_adv.get('xFIP', result["xfip"]))
            except: pass
            try:
                fip = float(p_adv.get('FIP', result["xfip"]))
                result["fip_spread"] = fip - result["xfip"]
            except: pass
            result["source"] = "mlb_stats_primary"
        

        # Check Career stats for HR/FB% anchor
        p_car = self.career_loader.fuzzy_find_player(name, self.pitching_car)
        if p_car:
            try: result["hrfb"] = float(p_car.get('HR/FB', p_car.get('HR/FB%', '12')).replace('%',''))
            except: pass
        
        # If no primary data, check secondary CSVs
        if result["source"] == "default":
            # pitching_advanced.csv
            p_adv2 = self._fuzzy(name, self.pitching_adv_csv)
            if p_adv2:
                try: result["xfip"] = float(p_adv2.get('xFIP', result["xfip"]))
                except: pass
                result["source"] = "csv_advanced"
            
            # pitching_plus.csv
            p_plus2 = self._fuzzy(name, self.pitching_plus_csv)
            if p_plus2:
                try: result["stuff"] = float(p_plus2.get('Stuff', 100))
                except: pass
        
        # pitching_statcast.csv — always check for barrel% allowed
        p_sc = self._fuzzy(name, self.pitching_sc_csv) or self.loader.fuzzy_find_player(name, self.pitching_sc_main)
        if p_sc:
            try: result["barrel_allowed"] = float(p_sc.get('Barrel%', p_sc.get('Barrel_pct', '8')).replace('%', '')) / 100.0
            except: pass
            try: result["la"] = float(p_sc.get('LA', result["la"]))
            except: pass
            try: result["ev90"] = float(p_sc.get('EV90', result["ev90"]))
            except: pass
        
        # Overrides.json
        if name in self.overrides:
            ov = self.overrides[name]
            if 'Stuff' in ov:
                result["stuff"] = ov['Stuff']
            if result["source"] == "default":
                result["source"] = "overrides_json"
        
        # K Profit CSW% fallback
        if result["source"] == "default" and name in self.k_profit:
            csw = self.k_profit[name]
            csw_ratio = csw / 0.29
            result["hr9"] = result["hr9"] / (csw_ratio ** 0.4)
            result["xfip"] = result["xfip"] / (csw_ratio ** 0.3)
            result["source"] = "k_profit_csw"
        
        return result

    def calculate_hr_probability(self, batter_name, pitcher_name, batter_index=0, opp_team_name="League Avg", park_factor=100, 
                                  temp=72, wind_speed=0, wind_dir=0, 
                                  pitcher_hand='R', umpire_name='MISSING',
                                  lineup=None, prev_prob=0.0, bullpen_arms=None):
        # Expand abbreviated names
        name_map = {"K. Griffin": "Konnor Griffin", "S. Antonacci": "Sam Antonacci", "A. Freeland": "Alex Freeland"}
        batter_name = name_map.get(batter_name, batter_name)
        
        b_adv = self._fuzzy(batter_name, self.batting_adv)
        b_sc = self._fuzzy(batter_name, self.batting_sc)
        
        # Fallbacks to secondary CSVs
        if not b_adv:
            b_adv = self._fuzzy(batter_name, self.batting_adv_csv) or {}
        if not b_sc:
            b_sc = self._fuzzy(batter_name, self.batting_sc_csv) or {}
        
        # ── 1. BASE RATE (Split-Specific ISO with sample dampening) ────
        split_data = self._fuzzy(batter_name, 
                                  self.splits_lhp if pitcher_hand == 'L' else self.splits_rhp)
        if not split_data:
            split_data = self._fuzzy(batter_name, 
                                  self.splits_lhp_csv if pitcher_hand == 'L' else self.splits_rhp_csv)
        
        # Get season ISO as baseline
        try:
            season_iso = float(b_adv.get('ISO', '0.0').replace('%', ''))
            if season_iso > 1.0: season_iso = season_iso / 1000.0
            if season_iso == 0: raise ValueError
        except:
            if batter_name in self.prospect_power_index:
                season_iso = self.prospect_power_index[batter_name]
            elif batter_name in self.prospects:
                season_iso = self.prospects[batter_name]['iso_prior']
            else:
                season_iso = LEAGUE_AVG_ISO
        
        # Get split ISO if available
        split_iso = season_iso
        split_pa = 50  # default assumption
        if split_data:
            try:
                raw = float(split_data.get('ISO', str(season_iso)).replace('%', ''))
                if raw > 1.0: raw = raw / 1000.0
                split_iso = raw
            except: pass
            try: split_pa = int(split_data.get('PA', '50'))
            except: pass
        
        # Sample-size regression: blend split ISO toward season ISO
        pa_threshold = 80.0 if batter_name in self.prospects else 120.0
        split_weight = min(1.0, split_pa / pa_threshold)
        iso = (split_weight * split_iso) + ((1 - split_weight) * season_iso)

        # ── 1.2 THE POWER GATE (LAYER 1) ──────────────────────────────
        # Bible: ISO > .220, Barrel% > 10%, EV90 > 108.
        # If all fail, apply a structural penalty.
        barrel_pct = LEAGUE_AVG_BARREL_PCT
        ev90 = LEAGUE_AVG_EV90
        if b_sc:
            try: barrel_pct = float(b_sc.get('Barrel%', '7.5').replace('%', '')) / 100.0
            except: pass
            try: ev90 = float(b_sc.get('EV90', str(LEAGUE_AVG_EV90)))
            except: pass

        gate_pass = False
        if iso >= POWER_GATE_ISO or barrel_pct >= POWER_GATE_BARREL or ev90 >= POWER_GATE_EV90:
            gate_pass = True
        
        gate_mult = 1.0
        if not gate_pass:
            gate_mult = 0.65 # Significant penalty for sub-power bats
        
        # Elite Power Bonus
        if iso >= ELITE_ISO and barrel_pct >= ELITE_BARREL and ev90 >= ELITE_EV90:
            gate_mult = 1.20 # Elite multiplier for triple-threat mashers
        
        # ── 1.5 LINEUP PROTECTION (TRAFFIC SCALING) ──────────────────
        protection_mult = 1.0
        if lineup and batter_index > 0:
            obp_sum = 0.0
            valid_batters = 0
            start_idx = max(0, batter_index - 2)
            for i in range(start_idx, batter_index):
                prev_batter = lineup[i]
                pb_adv = self._fuzzy(prev_batter, self.batting_adv) or self._fuzzy(prev_batter, self.batting_adv_csv) or {}
                try:
                    obp = float(pb_adv.get('OBP', '0.315'))
                    obp_sum += obp
                    valid_batters += 1
                except:
                    pass
            if valid_batters > 0:
                avg_obp = obp_sum / valid_batters
                if avg_obp > 0.315:
                    # e.g. .365 OBP -> 1.0 + (0.05 * 1.5) = 1.075 multiplier
                    protection_mult = 1.0 + ((avg_obp - 0.315) * 1.5)
        
        base_rate = LEAGUE_AVG_HR_PA * (iso / LEAGUE_AVG_ISO) * protection_mult

        # ── 2. PITCHER MATCHUP MULTIPLIER ────────────────────────────
        p_data = self._get_pitcher_data(pitcher_name)
        
        hr9_mult = p_data["hr9"] / LEAGUE_AVG_HR9
        xfip_mult = p_data["xfip"] / LEAGUE_AVG_XFIP
        barrel_mult = p_data["barrel_allowed"] / LEAGUE_AVG_BARREL_ALLOWED
        stuff_adj = 1.0 - ((p_data["stuff"] - 100) * 0.004)
        gb_adj = 1.0 - ((p_data["gb_pct"] - LEAGUE_AVG_GB_PCT) * 0.5)
        
        # Blend: HR/9 is primary, LA and Barrel% are secondary modifiers
        # High LA (>15) indicates fly-ball vulnerability
        la_adj = 1.0 + ((p_data["la"] - LEAGUE_AVG_LA) * 0.02)
        
        # HR/FB Adjustment: 12% is league average
        hrfb_adj = 1.0 + ((p_data["hrfb"] - 12.0) * 0.03)
        
        # FIP Spread: If FIP > xFIP, pitcher is surrendering high HR/FB%
        fip_adj = 1.0 + (p_data["fip_spread"] * 0.15)
        
        pitcher_mult = (hr9_mult * 0.30 + xfip_mult * 0.15 + barrel_mult * 0.25 + la_adj * 0.10 + hrfb_adj * 0.20) * stuff_adj * gb_adj * fip_adj
        
        # Platoon wOBA adjustment
        platoon_mult = 1.0
        if split_data:
            try:
                woba = float(split_data.get('wOBA', '0.320'))
                platoon_mult = woba / 0.320
            except: pass
        
        # Bible: High-delta daily variable (30-35% weight)
        raw_sp = pitcher_mult * platoon_mult
        dampened_sp = 1.0 + (raw_sp - 1.0) * 0.65 # Increased sensitivity
        sp_multiplier = max(0.45, min(1.85, dampened_sp))

        # ── 3. BULLPEN INTEGRATION (V5.0 Tiered Attrition) ───────────
        bp_xfip = BULLPEN_XFIP.get(opp_team_name, 3.90)
        
        # Dynamic Tiered Bullpen scaling based on starter quality
        # V5.0: If starter xFIP is high (>4.20), assume earlier exit and higher Tier C (Gas Can) exposure
        tier_c_exposure = 1.0
        if p_data["xfip"] > 4.20:
            tier_c_exposure = 1.0 + ((p_data["xfip"] - 4.20) * 0.4)
        elif p_data["xfip"] < 3.20:
            tier_c_exposure = 0.85 # Less bullpen exposure
            
        bp_hr9 = 1.05 * (bp_xfip / 3.90) * tier_c_exposure
        bp_mult = (bp_hr9 / LEAGUE_AVG_HR9)
        
        # Apply Attrition Multiplier (tired/catastrophic bullpens)
        attrition = self.bp_attrition.get(opp_team_name, 1.0)
        bp_multiplier = max(0.5, min(2.5, bp_mult * platoon_mult * attrition))

        # ── 4. STATCAST QUALITY WEIGHT ───────────────────────────────
        barrel_pct = LEAGUE_AVG_BARREL_PCT
        exit_velo = LEAGUE_AVG_EXIT_VELO
        xwoba = 0.320
        
        if b_sc:
            try: barrel_pct = float(b_sc.get('Barrel%', '7.5').replace('%', '')) / 100.0
            except: pass
            try: exit_velo = float(b_sc.get('EV', str(LEAGUE_AVG_EXIT_VELO)))
            except: pass
            try: xwoba = float(b_sc.get('xwOBA', b_sc.get('xwOBA', '0.320')))
            except: pass
        
        barrel_norm = barrel_pct / LEAGUE_AVG_BARREL_PCT
        velo_norm = exit_velo / LEAGUE_AVG_EXIT_VELO
        xwoba_norm = xwoba / 0.320
        
        # Weighted blend: barrel% is king for HR prediction
        quality_adj = (barrel_norm * 0.50 + velo_norm * 0.25 + xwoba_norm * 0.25)
        quality_adj = max(0.5, min(2.0, quality_adj))

        # ── 5. ENVIRONMENT ───────────────────────────────────────────
        pf_mult = park_factor / 100.0
        temp_adj = 1.0 + ((temp - 70) * 0.0015) # Bible: Increased sensitivity
        # V6.0 Bible: Exponential Wind Dynamics
        wind_comp = wind_speed * math.cos(math.radians(wind_dir))
        if wind_comp > 8:
            wind_adj = 1.0 + (8 * 0.005) + (math.exp((wind_comp - 8) * 0.15) - 1.0) * 0.04
        elif wind_comp < -8:
            wind_adj = 1.0 + (-8 * 0.005) - (math.exp((abs(wind_comp) - 8) * 0.15) - 1.0) * 0.04
        else:
            wind_adj = 1.0 + (wind_comp * 0.006)
        
        # V5.0: Thermodynamic Synergy Multiplier (Extreme Run Environments)
        thermo_synergy = 1.0
        if temp > 75 and park_factor > 105:
            thermo_synergy = 1.0 + ((temp - 75) * 0.02)
        
        pf_mult *= thermo_synergy
        
        # Umpire: lower K_Factor = smaller zone = more hitter counts = more HRs
        ump_k = self.umpires.get(umpire_name, 1.0)
        ump_adj = 1.0 / (ump_k ** 0.3)

        # ── 6. DYNAMIC PA ENGINE & MONTE CARLO PROBABILITY ───────────────
        try: wrc = float(b_adv.get('wRC+', 100))
        except: wrc = 100

        # Apply manual batter overrides
        if batter_name in self.manual_batters:
            mb = self.manual_batters[batter_name]
            season_iso = mb["iso"]
            wrc = mb["wrc"]
            barrel_pct = mb["barrel"] / 100.0
            exit_velo = mb["ev"]
            iso = season_iso # Bypass split sample dampening for manual overrides
            base_rate = LEAGUE_AVG_HR_PA * (iso / LEAGUE_AVG_ISO)
            barrel_norm = barrel_pct / LEAGUE_AVG_BARREL_PCT
            velo_norm = exit_velo / LEAGUE_AVG_EXIT_VELO
            quality_adj = (barrel_norm * 0.50 + velo_norm * 0.25 + xwoba_norm * 0.25)
            quality_adj = max(0.5, min(2.0, quality_adj))

        # Slot-based PA expectations (Bible: 2-5 are prime, 7-9 are avoid)
        slot_pas = {0: 4.60, 1: 4.50, 2: 4.45, 3: 4.35, 4: 4.25, 5: 4.10, 6: 3.85, 7: 3.65, 8: 3.50}
        base_pa = slot_pas.get(batter_index, 3.5)
        total_pa = base_pa + ((wrc - 100) * 0.002)

        # Split PAs between Starter and Bullpen
        sp_pa = min(2.5, total_pa)
        bp_pa = total_pa - sp_pa
        
        shared_factors = base_rate * quality_adj * pf_mult * temp_adj * wind_adj * ump_adj * gate_mult * CALIBRATION
        
        # ── 7. GRADUATED GAS CAN (Proportional to pitcher vulnerability) ─
        # V6.0: Enhanced exponential lift for high-vulnerability "Gas Cans"
        raw_gas = max(0, (pitcher_mult - 1.0))
        if pitcher_mult > 1.20:
            gas_can_lam = (raw_gas ** 1.5) * 0.12 # Colder math for Gas Cans
        else:
            gas_can_lam = raw_gas * 0.06
        
        # Stadium/Weather Amplification
        if gas_can_lam > 0 and (park_factor > 105 or temp > 75):
            gas_can_lam *= 1.40
        
        # Platoon advantage amplification
        if gas_can_lam > 0 and platoon_mult > 1.05:
            gas_can_lam *= 1.25
        
        # ── 8. EXTREME ALTITUDE FLOOR ────────────────────────────
        # V3.0: In extreme environments (Mexico City PF 165), ALL hitters get
        # an additive λ boost — thin air benefits low-ISO hitters disproportionately
        altitude_lam = 0.0
        if park_factor >= 140:
            altitude_lam = 0.025
        elif park_factor >= 120:
            altitude_lam = 0.010
            
        # ── 8.5 BATTED BALL SYNERGY ──────────────────────────────────
        synergy_lam = 0.0
        if barrel_pct > 0.12 and p_data["barrel_allowed"] > 0.09:
            # Exponential lift for elite barrel hitters facing barrel-prone pitchers
            synergy_lam = 0.015 + ((barrel_pct - 0.12) * 0.5)
        
        lam_sp = shared_factors * sp_pa * sp_multiplier + gas_can_lam + altitude_lam + synergy_lam
        lam_bp = shared_factors * bp_pa * bp_multiplier
        
        # 100,000-iteration Monte Carlo Simulation for Probability
        import random
        hr_count = 0
        sims = 100000
        lam_total = lam_sp + lam_bp
        for _ in range(sims):
            L = math.exp(-lam_total)
            k = 0
            p = 1.0
            while p > L:
                k += 1
                p *= random.random()
            if (k - 1) > 0:
                hr_count += 1
                
        prob = hr_count / sims
        
        # ── 9. HOT STREAK MULTIPLIER (Bayesian Dampened) ────────
        # V5.0: Cap streak multiplier if opposing pitcher has elite stuff or xFIP.
        streak_mult = self.streak_multipliers.get(batter_name, 1.0)
        
        if streak_mult > 1.0:
            if p_data["stuff"] > 110 or p_data["xfip"] < 3.00:
                streak_mult = min(streak_mult, 1.15)
                
        prob *= streak_mult
        
        # ── 9.5 PITCHER TILT (CONTAGION EFFECT) ─────────────────
        if prev_prob > 0.08:
            # If the previous batter had a massive HR probability (e.g. > 8%), 
            # the pitcher is likely "on tilt" and giving up hard contact.
            # V4.0: Enhanced tilt bonus
            tilt_bonus = 1.0 + ((prev_prob - 0.08) * 2.0)
            tilt_bonus = min(1.30, tilt_bonus) # Cap at 30% boost
            prob *= tilt_bonus
        
        # ── 9.7 PLATE DISCIPLINE (CONTACT SCALING) ──────────────
        # V4.0: HRs require contact. Scale based on Contact%.
        contact_rate = self.discipline.get(batter_name, 75.0) # default 75%
        if contact_rate > 85.0:
            prob *= 1.05
        elif contact_rate < 70.0:
            prob *= 0.90
        
        # ── 10. ELITE HITTER FLOOR ──────────────────────────────
        # V3.0: Elite power bats should never drop below plausible minimums
        # even when facing aces. Judge/Ohtani/Henderson hit HRs off anyone.
        # Also use wRC+ as an alternative trigger for high-contact power guys
        # like Yandy Díaz (150 wRC+, .181 ISO) who the ISO-only floor misses.
        if iso >= 0.240:
            prob = max(prob, 0.050)
        elif iso >= 0.180 or wrc >= 140:
            prob = max(prob, 0.040)
        
        # V20 SYNC: Export to Intelligence Hub
        if pitcher_name and batter_name:
            game_id = HUB.get("GameID")
            # We use a composite key to store individual batter risks vs this pitcher
            HUB.set(f"HR_Prob_{pitcher_name}_{batter_name}", min(prob, 1.0), game_id=game_id)

        return min(prob, 1.0)

    def run_slate(self):
        stadiums = {
            "Guardians":     {"pf": 108, "temp": 66, "wind": 10, "dir": 0},
            "Orioles":       {"pf": 98,  "temp": 63, "wind": 8,  "dir": 45},
            "Reds":          {"pf": 112, "temp": 75, "wind": 7,  "dir": 135},
            "Phillies":      {"pf": 105, "temp": 63, "wind": 6,  "dir": 0},
            "Pirates":       {"pf": 98,  "temp": 70, "wind": 8,  "dir": 180},
            "Blue Jays":     {"pf": 102, "temp": 72, "wind": 0,  "dir": 0},
            "Mets":          {"pf": 97,  "temp": 56, "wind": 8,  "dir": 0},
            "Braves":        {"pf": 105, "temp": 77, "wind": 5,  "dir": 0},
            "White Sox":     {"pf": 104, "temp": 61, "wind": 15, "dir": 60},
            "Brewers":       {"pf": 102, "temp": 72, "wind": 0,  "dir": 0},
            "Twins":         {"pf": 100, "temp": 54, "wind": 11, "dir": 0},
            "Rangers":       {"pf": 100, "temp": 72, "wind": 0,  "dir": 0},
            "Athletics":     {"pf": 94,  "temp": 75, "wind": 2,  "dir": 0},
            "Padres":        {"pf": 95,  "temp": 64, "wind": 11, "dir": 90},
        }
        
        pitcher_hands = {
            "Nick Martinez": "RHP", "Tanner Bibee": "RHP",
            "Kai-Wei Teng": "RHP", "Shane Baz": "RHP",
            "Kyle Freeland": "LHP", "Chase Burns": "RHP",
            "Tyler Mahle": "RHP", "Jesús Luzardo": "LHP",
            "Kyle Leahy": "RHP", "Braxton Ashcraft": "RHP",
            "Payton Tolle": "LHP", "Trey Yesavage": "RHP",
            "Zack Littell": "RHP", "Clay Holmes": "RHP",
            "Casey Mize": "RHP", "Martin Perez": "LHP",
            "José Soriano": "RHP", "Davis Martin": "RHP",
            "Merrill Kelly": "RHP", "Chad Patrick": "RHP",
            "Logan Gilbert": "RHP", "Joe Ryan": "RHP",
            "Cam Schlittler": "RHP", "Jacob deGrom": "RHP",
            "Kris Bubic": "LHP", "Aaron Civale": "RHP",
            "Edward Cabrera": "RHP", "Walker Buehler": "RHP"
        }

        results = []
        for game in GAMES:
            away = game['away']
            home = game['home']
            home_team = home['team']
            umpire = game.get('umpire', 'MISSING')
            
            s_data = stadiums.get(home_team, {"pf": 100, "temp": 70, "wind": 0, "dir": 0})
            
            for role, team_data in [('away', away), ('home', home)]:
                opp_pitcher = home['pitcher'] if role == 'away' else away['pitcher']
                opp_team = home['team'] if role == 'away' else away['team']
                p_hand = pitcher_hands.get(opp_pitcher, 'RHP')[0]
                bullpen_arms = home.get('bullpen') if role == 'away' else away.get('bullpen')
                
                prev_prob = 0.0
                for i, batter in enumerate(team_data['lineup']):
                    prob = self.calculate_hr_probability(
                        batter, opp_pitcher, batter_index=i, opp_team_name=opp_team,
                        park_factor=s_data['pf'], temp=s_data['temp'],
                        wind_speed=s_data['wind'], wind_dir=s_data['dir'],
                        pitcher_hand=p_hand, umpire_name=umpire,
                        lineup=team_data['lineup'], prev_prob=prev_prob, bullpen_arms=bullpen_arms
                    )
                    if prob > 0:
                        p_data = self._get_pitcher_data(opp_pitcher)
                        results.append({
                            'player': batter,
                            'team': team_data['team'],
                            'vs': opp_pitcher,
                            'prob': prob,
                            'pitcher_source': p_data['source'],
                        })
                    prev_prob = prob
        
        results.sort(key=lambda x: x['prob'], reverse=True)
        return results[:30]


if __name__ == "__main__":
    model = HRModel("/Users/danielreiss/Desktop/Antigravity/HR/MLB Stats")
    top_picks = model.run_slate()
    
    print("\n" + "═"*72)
    print("  🏆 MLB HOME RUN PREDICTION ENGINE — CALIBRATED & OPTIMIZED 🏆")
    print("              APRIL 28, 2026 SLATE")
    print("═"*72)
    print(f"  {'#':<3} {'Player':<22} {'Prob':>6}  {'vs Pitcher':<20} {'Data Source'}")
    print("  " + "─"*68)
    for i, p in enumerate(top_picks, 1):
        tier = "🔥" if p['prob'] >= 0.08 else "⚡" if p['prob'] >= 0.05 else "  "
        print(f"  {tier}{i:<2} {p['player']:<22} {p['prob']*100:>5.1f}%  vs {p['vs']:<18} [{p['pitcher_source']}]")
    
    print("  " + "─"*68)
    print("  🔥 = High Conviction (≥8%)  |  ⚡ = Play (≥5%)  |  Blank = Monitor")
    print("═"*72)
    
    # Audit: show pitcher data sources
    print("\n── PITCHER DATA AUDIT ──────────────────────────────────────────")
    seen = set()
    for game in GAMES:
        for side in ['away', 'home']:
            pitcher = game[side]['pitcher']
            if pitcher not in seen:
                seen.add(pitcher)
                pd = model._get_pitcher_data(pitcher)
                print(f"  {pitcher:<22} HR/9={pd['hr9']:.2f}  xFIP={pd['xfip']:.2f}  "
                      f"Stuff={pd['stuff']:<3}  Brl%={pd['barrel_allowed']:.3f}  [{pd['source']}]")
    print("")