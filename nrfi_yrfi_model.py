"""
MLB NRFI / YRFI Prediction Model V2.0 (Data-Driven)
===================================================
Estimates the probability of a run scoring in the first inning for any matchup
using a Monte Carlo simulation of the first 5-6 batters.

Logic:
  - Simulation runs 10,000 iterations for each half-inning.
  - A pitcher faces batters 1-5 in order.
  - If 3 outs are recorded before facing the 6th batter, it's a No Run (NR).
  - If the 6th batter is reached, a run is assumed to have scored (YR).
  - Final Prob(NRFI) = P(Top NR) * P(Bottom NR).

Data Sources:
  - K Prophet/data/pitching_advanced.csv
  - K Prophet/data/pitching_plus.csv
  - K Prophet/data/batting_advanced.csv
  - K Prophet/data/overrides.json
"""

import math
import random
import os
import sys
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# Add workspace to path to allow importing local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from nrfi_data_bridge import NRFI_DataLoader

# ---------------------------------------------------------------------------
# CONSTANTS & GLOBALS
# ---------------------------------------------------------------------------

LOADER = NRFI_DataLoader()

# Ballpark multipliers (Park Factors for Runs)
PARK_FACTORS: Dict[str, float] = {
    "Coors Field":              1.30,
    "Great American Ball Park": 1.18,
    "Fenway Park":              1.14,
    "Globe Life Field":         1.08,
    "Wrigley Field":            1.06,
    "Yankee Stadium":           1.05,
    "Oracle Park":              0.96,
    "Dodger Stadium":           0.97,
    "Petco Park":               0.93,
    "T-Mobile Park":            0.88,
    "Truist Park":              1.03,
    "American Family Field":    1.07,
    "Chase Field":              1.10,
    "Camden Yards":             1.04,
    "Kauffman Stadium":         0.99,
    "PNC Park":                 0.95,
    "Busch Stadium":            0.97,
    "Guaranteed Rate Field":    1.05,
    "Citizens Bank Park":       1.09,
    "Target Field":             0.98,
    "Tropicana Field":          0.95,
    "loanDepot Park":           0.93,
    "Nationals Park":           1.01,
    "Progressive Field":        1.00,
    "Minute Maid Park":         1.02,
    "Comerica Park":            0.94,
    "Angel Stadium":            1.00,
    "Oakland Coliseum":         0.92,
    "Rogers Centre":            1.06,
    "Citi Field":               0.97,
    "Sahlen Field":             1.00,
}

# ---------------------------------------------------------------------------
# MODELS
# ---------------------------------------------------------------------------

@dataclass
class GameInput:
    home_team:      str
    away_team:      str
    home_pitcher:   str
    away_pitcher:   str
    ballpark:       str
    home_lineup:    List[str] = field(default_factory=list) # List of names
    away_lineup:    List[str] = field(default_factory=list) # List of names
    
    # V2.5 Calibration Data
    home_pitcher_1st_era: Optional[float] = None
    away_pitcher_1st_era: Optional[float] = None
    home_team_1st_rank_30d: Optional[int] = None
    away_team_1st_rank_30d: Optional[int] = None
    home_lineup_1st_pct_recent: Optional[float] = None
    away_lineup_1st_pct_recent: Optional[float] = None

@dataclass
class Prediction:
    game:            GameInput
    yrfi_prob:       float
    nrfi_prob:       float
    top_nr_prob:     float
    bottom_nr_prob:  float
    confidence:      str
    implied_american_yrfi: int
    implied_american_nrfi: int
    verdict:         str = "NO BET"
    bet_recommendation: str = "SKIP"
    notes:           List[str] = field(default_factory=list)

    def __str__(self) -> str:
        line = "=" * 58
        g = self.game
        return (
            f"\n{line}\n"
            f"  {g.away_team} @ {g.home_team}  |  {g.ballpark}\n"
            f"  {g.away_pitcher} vs {g.home_pitcher}\n"
            f"{line}\n"
            f"  YRFI probability : {self.yrfi_prob * 100:.1f}%  "
            f"(American: {self.implied_american_yrfi:+d})\n"
            f"  NRFI probability : {self.nrfi_prob * 100:.1f}%  "
            f"(American: {self.implied_american_nrfi:+d})\n"
            f"{line}\n"
            f"  VERDICT           : {self.verdict}\n"
            f"  RECOMMENDATION    : {self.bet_recommendation}\n"
            f"{line}\n"
            f"  Breakdown:\n"
            f"    Top 1st NR Prob   : {self.top_nr_prob * 100:.1f}%\n"
            f"    Bottom 1st NR Prob: {self.bottom_nr_prob * 100:.1f}%\n"
            f"    Confidence        : {self.confidence}\n"
            + (("\n  Notes:\n" + "".join(f"    • {n}\n" for n in self.notes)) if self.notes else "")
            + f"{line}\n"
        )

# ---------------------------------------------------------------------------
# CALIBRATION CONSTANTS (2026 V3.0)
# ---------------------------------------------------------------------------
# Global multiplier to account for 2026 "NRFI-heavy" environment (42.6% YRFI)
# Adjusted to produce ~42.6% YRFI for average matchups
SEASON_ENVIRONMENT_MODIFIER = 1.03 

# Pitcher Vulnerability Factor (Accounts for "Settling In")
# Users says pitchers are most vulnerable in first 15-20 pitches
PITCHER_SETTLING_IN_MOD = 1.05

class FirstInningSim:
    def __init__(self, pitcher_name: str, lineup_names: List[str], team_name: str, ballpark: str):
        self.p_name = pitcher_name
        self.p_stats = LOADER.get_pitcher(pitcher_name)
        self.park_factor = PARK_FACTORS.get(ballpark, 1.0)
        
        # Resolve Lineup
        if not lineup_names:
            # Fallback to top batters from data
            self.lineup = LOADER.get_team_top_batters(team_name, 5)
        else:
            self.lineup = [LOADER.get_batter(name) for name in lineup_names[:5]]

    def calculate_outcome_probs(self, batter: Dict[str, Any]) -> Dict[str, float]:
        """Blend pitcher and batter stats to get PA outcome probabilities."""
        # K% Blend
        p_k = self.p_stats.get("K_pct", 22.7) / 100.0
        b_k = batter.get("K_pct", 22.7) / 100.0
        stuff_mod = (self.p_stats.get("Stuff", 100) / 100.0) ** 1.0 # Reduced power from 1.2
        prob_k = (p_k * b_k / 0.227) * stuff_mod
        
        # BB% Blend
        p_bb = self.p_stats.get("BB_pct", 8.5) / 100.0
        b_bb = batter.get("BB_pct", 8.5) / 100.0
        prob_bb = (p_bb * b_bb / 0.085)
        
        # Hit Probability (V3.0 Dampened Scaling)
        base_babip = 0.295
        
        # Dampening: wRC+ and xERA shouldn't scale BABIP linearly
        # A 185 wRC+ hitter shouldn't have a .540 BABIP purely from the model
        batter_wrc = batter.get("wRC_plus", 100)
        pitcher_xera = self.p_stats.get("xERA", 4.0)
        
        wrc_mod = 1.0 + (batter_wrc - 100) * 0.003
        xera_mod = 1.0 + (pitcher_xera - 4.0) * 0.1
        
        adj_babip = base_babip * wrc_mod * xera_mod * self.park_factor * SEASON_ENVIRONMENT_MODIFIER * PITCHER_SETTLING_IN_MOD
        
        prob_in_play = 1.0 - prob_k - prob_bb
        prob_hit = prob_in_play * adj_babip
        prob_out = prob_in_play * (1.0 - adj_babip)
        
        # V3.1: Dynamic Hit Distribution
        # Use wRC+ as a proxy for power density if ISO is missing
        hr_share = 0.13 + (batter_wrc - 100) * 0.001
        hr_share = max(0.05, min(0.25, hr_share))
        
        t3b_share = 0.02
        doub_share = 0.20 + (batter_wrc - 100) * 0.0005
        doub_share = max(0.10, min(0.30, doub_share))
        
        # Normalize
        total = prob_k + prob_bb + prob_hit + prob_out
        return {
            "K": prob_k / total,
            "BB": prob_bb / total,
            "Hit": prob_hit / total,
            "Out": prob_out / total,
            "HR_share": hr_share,
            "3B_share": t3b_share,
            "2B_share": doub_share
        }

    def simulate_half_inning(self, n_sims: int = 10000) -> float:
        """Returns the probability of No Run (NR) in the half-inning."""
        nr_count = 0
        
        lineup_to_sim = self.lineup
        while len(lineup_to_sim) < 9:
            lineup_to_sim.append({"K_pct": 22.7, "BB_pct": 8.5, "wRC_plus": 100})
            
        batter_probs = [self.calculate_outcome_probs(b) for b in lineup_to_sim]
        
        for _ in range(n_sims):
            outs = 0
            batters_faced = 0
            runs = 0
            bases = [False, False, False] # 1B, 2B, 3B
            
            while outs < 3:
                b_probs = batter_probs[batters_faced % 9]
                batters_faced += 1
                
                roll = random.random()
                if roll < b_probs["K"]:
                    outs += 1
                elif roll < b_probs["K"] + b_probs["BB"]:
                    # Walk
                    if bases[0] and bases[1] and bases[2]:
                        runs += 1
                    elif bases[0] and bases[1]:
                        bases[2] = True
                    elif bases[0]:
                        bases[1] = True
                    bases[0] = True
                elif roll < b_probs["K"] + b_probs["BB"] + b_probs["Hit"]:
                    hit_roll = random.random()
                    hr_thr = b_probs.get("HR_share", 0.13)
                    t3b_thr = hr_thr + b_probs.get("3B_share", 0.02)
                    doub_thr = t3b_thr + b_probs.get("2B_share", 0.20)
                    
                    if hit_roll < hr_thr: # HR
                        runs += 1 + sum(bases)
                        bases = [False, False, False]
                    elif hit_roll < t3b_thr: # 3B
                        runs += sum(bases)
                        bases = [False, False, True]
                    elif hit_roll < doub_thr: # 2B
                        runs += bases[1] + bases[2]
                        bases[2] = bases[0]
                        bases[1] = True
                        bases[0] = False
                    else: # 1B
                        runs += bases[2]
                        if bases[1]:
                            # ~50% chance to score from second on a single
                            if random.random() < 0.50:
                                runs += 1
                                bases[2] = False
                            else:
                                bases[2] = True
                        else:
                            bases[2] = False
                        bases[1] = bases[0]
                        bases[0] = True
                else: # In-play out
                    if bases[0] and outs < 2 and random.random() < 0.11: # Double play
                        outs += 2
                        bases[0] = False
                    else:
                        outs += 1
                        
                if runs > 0:
                    break # YRFI
            
            if runs == 0:
                nr_count += 1
            
        return nr_count / n_sims

# ---------------------------------------------------------------------------
# CORE FUNCTIONS
# ---------------------------------------------------------------------------

def _prob_to_american(prob: float) -> int:
    if prob <= 0 or prob >= 1: return 0
    if prob >= 0.5:
        return -round((prob / (1 - prob)) * 100)
    else:
        return round(((1 - prob) / prob) * 100)

def _confidence_label(prob: float) -> str:
    distance = abs(prob - 0.50)
    if distance >= 0.15: return "HIGH"
    elif distance >= 0.08: return "MEDIUM"
    else: return "LOW"

def predict_game(game: GameInput) -> Prediction:
    notes: List[str] = []
    
    # 1. Sim Top 1st (Away Batters vs Home Pitcher)
    top_sim = FirstInningSim(game.home_pitcher, game.away_lineup, game.away_team, game.ballpark)
    top_nr_prob = top_sim.simulate_half_inning()
    
    # 2. Sim Bottom 1st (Home Batters vs Away Pitcher)
    bottom_sim = FirstInningSim(game.away_pitcher, game.home_lineup, game.home_team, game.ballpark)
    bottom_nr_prob = bottom_sim.simulate_half_inning()
    
    # 3. Combine
    nrfi_prob = top_nr_prob * bottom_nr_prob
    yrfi_prob = 1.0 - nrfi_prob
    
    # Dynamic Notes
    if top_nr_prob > 0.85 and bottom_nr_prob > 0.85:
        notes.append("Dual-Ace dominance expected — elite NRFI potential.")
    if top_nr_prob < 0.65 or bottom_nr_prob < 0.65:
        notes.append("Explosive early-inning potential for one side — YRFI risk.")
    
    park_f = PARK_FACTORS.get(game.ballpark, 1.0)
    if park_f > 1.10:
        notes.append(f"Park factor at {game.ballpark} favors runs (+{int((park_f-1)*100)}%).")
    elif park_f < 0.92:
        notes.append(f"Park factor at {game.ballpark} supresses runs (-{int((1-park_f)*100)}%).")

    # 4. Calibration V2.5: Dual Confirmation Logic
    verdict = "NO BET"
    bet_rec = "SKIP"
    
    # NRFI Logic
    nrfi_conf = nrfi_prob >= 0.57
    p_era_ok = (game.home_pitcher_1st_era is not None and game.home_pitcher_1st_era < 3.50 and
                game.away_pitcher_1st_era is not None and game.away_pitcher_1st_era < 3.50)
    t_rank_ok = (game.home_team_1st_rank_30d is not None and game.home_team_1st_rank_30d > 8 and
                 game.away_team_1st_rank_30d is not None and game.away_team_1st_rank_30d > 8)
    
    if nrfi_conf and p_era_ok and t_rank_ok:
        verdict = "NRFI (NO RUN FIRST INNING)"
        bet_rec = "PLACE BET"
    elif nrfi_conf:
        verdict = "LEAN NRFI (FAILED CONFIRMATION)"
        if not p_era_ok: notes.append("NRFI Alert: One or more pitchers have 1st-inning ERA > 3.50.")
        if not t_rank_ok: notes.append("NRFI Alert: One or more teams rank in top 8 for 1st-inning runs.")

    # YRFI Logic
    yrfi_conf = yrfi_prob >= 0.65
    p_era_bad = (game.home_pitcher_1st_era is not None and game.home_pitcher_1st_era > 4.50 or
                 game.away_pitcher_1st_era is not None and game.away_pitcher_1st_era > 4.50)
    t_pct_bad = (game.home_lineup_1st_pct_recent is not None and game.home_lineup_1st_pct_recent >= 0.55 or
                 game.away_lineup_1st_pct_recent is not None and game.away_lineup_1st_pct_recent >= 0.55)
    
    if yrfi_conf and p_era_bad and t_pct_bad:
        verdict = "YRFI (YES RUN FIRST INNING)"
        bet_rec = "PLACE BET"
    elif yrfi_conf:
        if verdict == "NO BET": # Don't overwrite if NRFI was somehow already set (unlikely)
            verdict = "LEAN YRFI (FAILED CONFIRMATION)"
            if not p_era_bad: notes.append("YRFI Alert: Neither pitcher has 1st-inning ERA > 4.50.")
            if not t_pct_bad: notes.append("YRFI Alert: Neither lineup scores in 1st-inning in 55%+ of games.")

    # Coin Flip Filter
    if 0.50 <= nrfi_prob <= 0.56:
        verdict = "NO BET (COIN FLIP)"
        bet_rec = "SKIP"
        notes.append("Strict calibration: 50-56% confidence is coin flip territory with juice.")

    return Prediction(
        game=game,
        yrfi_prob=yrfi_prob,
        nrfi_prob=nrfi_prob,
        top_nr_prob=top_nr_prob,
        bottom_nr_prob=bottom_nr_prob,
        confidence=_confidence_label(nrfi_prob),
        implied_american_yrfi=_prob_to_american(yrfi_prob),
        implied_american_nrfi=_prob_to_american(nrfi_prob),
        verdict=verdict,
        bet_recommendation=bet_rec,
        notes=notes
    )

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n🔮 MLB NRFI / YRFI PREDICTION MODEL V2.0 (DRE)")
    print("    Integrating K Prophet & MLB Workspace Data\n")

    # Try to load live games from games_data.py if it exists
    SLATE = []
    games_data_path = os.path.join(os.path.dirname(__file__), "K Prophet/games_data.py")
    if os.path.exists(games_data_path):
        try:
            # We add the directory to sys.path and import
            sys.path.append(os.path.join(os.path.dirname(__file__), "K Prophet"))
            from games_data import GAMES as LIVE_GAMES
            for g in LIVE_GAMES:
                SLATE.append(GameInput(
                    home_team=g['home']['team'],
                    away_team=g['away']['team'],
                    home_pitcher=g['home']['pitcher'],
                    away_pitcher=g['away']['pitcher'],
                    ballpark=g.get('ballpark', 'Neutral'),
                    home_lineup=[p[0] for p in g['home']['lineup']],
                    away_lineup=[p[0] for p in g['away']['lineup']]
                ))
            print(f"✅ Loaded {len(LIVE_GAMES)} games from K Prophet/games_data.py")
        except Exception as e:
            print(f"⚠️ Error loading games_data.py: {e}")
            # Fallback
    
    if not SLATE:
        # Fallback to manual examples
        SLATE = [
            GameInput("Phillies", "Mets", "Zack Wheeler", "David Peterson", "Citizens Bank Park"),
            GameInput("Rockies", "Dodgers", "Chase Dollander", "Shohei Ohtani", "Coors Field")
        ]

    predictions = [predict_game(g) for g in SLATE]
    predictions.sort(key=lambda p: p.nrfi_prob, reverse=True)

    for pred in predictions:
        print(pred)
