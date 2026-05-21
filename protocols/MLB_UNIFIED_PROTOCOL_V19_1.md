# MLB OMNI-PROPHET V19.1: UNIFIED SYNDICATE PROTOCOL

**Status**: ACTIVE | **Engine**: Omni-Prophet V19.1 (V16.3 Expert Calibrated) | **Mandate**: Multi-Engine Syndicate Simulation

---

## MANDATE
Execute a forensic deep-audit, calibration check, and Chaos Engine simulation. Data Integrity > Speed. If a metric is unavailable, state "DATA NULL"—DO NOT HALLUCINATE. Use the attached lineup screenshot as absolute ground-truth for roster verification.

---

## PHASE 0: CALIBRATION & HISTORICAL CHECK
Before ANY research:
1. Run `calibration_check.py` (or manually load `predictions_history.csv` and `K Prophet/performance_tracker.csv`).
2. Report:
   - Last 10 game total MAE and directional bias (Under/Over tendency)
   - Last 20 K-prop hit rate and mean signed error
3. Determine CALIBRATION MODIFIER:
   - If totals consistently undershot by >1.5 runs: apply +0.3 to final total
   - If K-props consistently overshot: reduce K/9 anchor by 3%
4. Report the modifier explicitly in output.

---

## PHASE 0.5: DATA READINESS & YRFI AUDIT
Before simulation:
1. Verify both SPs are in `nrfi_yrfi_model.py`'s `PITCHER_RATINGS`.
2. Verify both Teams are in `TEAM_FI_RATES`.
3. Verify Ballpark is in `PARK_FACTORS`.
4. **MANDATE**: If any value is missing or "TBD", STOP and request the specific ERA+ / xFIP percentile or FI Rate from the USER. No "placeholders" allowed for high-conviction plays.

---

## PHASE 1: DATA HARVEST (Bind to `omni_prophet_v16.py` inputs)

### 1A. Pitcher Audit (EACH SP)
Research and bind to `game_data`:
- **Stuff+** (2026) → `sp_statcast['Stuff']`
- **VAA** → `sp_statcast['VAA']`
- **K%** → `sp_statcast['K_pct']`
- **BB%** → `sp_statcast['BB_pct']`
- **IP** → `sp_statcast['IP']`
- **xERA** → `sp_statcast['xERA']`
- **ERA** → `game_data['*_sp_era']`
- **CSW% and SwStr%** (last 3 starts — detect drift)
- **Archetype**: Determine dynamically:
  - VAA > -4.0 OR FB Stuff+ > 115 → North-South
  - SI Stuff+ > 110 AND SL Stuff+ > 115 → Unicorn
  - SI Stuff+ > 110 → East-West
  - Else → Standard
- **OPENER CHECK**: If SP avg IP < 3.0 in 2026 → flag OPENER, identify bulk pitcher, set PitchLimit=50, ShortLeash=True.

### 1B. Lineup Audit (EACH of 9 batters)
- **K%** (vs SP handedness splits) → `lineup_statcast[i]['K_pct']`
- **O-Swing%** (Chase Rate) → `lineup_statcast[i]['O_Swing']`
- **Z-Contact%** → `lineup_statcast[i]['Z_Contact']`
- **Batting Hand** → `lineup_statcast[i]['Hand']`
- Identify **K-Density clusters** (consecutive high-whiff batters)

### 1C. Environment & Operations
- Temperature, Wind Speed/Direction (degrees from CF), Humidity, Altitude, Rain Intensity (0-1), ADI
- **Umpire**: Name, CS% (2026), Zone Type (tight/neutral/wide)
- Park Factor, Is Dome, Game Time
- Shadow Dynamics: Active if west-coast park + 16:xx start

### 1D. Operational Modifiers
- DRS (Away/Home), Manager Hook Tendency
- Bullpen Pitches D-1 and D-2 (both teams)
- Catcher Name → lookup 2026 framing runs → assign Tier (1-4)
- Travel Fatigue / Getaway Day flag

---

## PHASE 1.5: PRE-FLIGHT SANITY CHECK
Before simulation, verify:
- ☐ Both lineups = exactly 9 batters
- ☐ SP ERA in [1.50, 8.00] range
- ☐ Park Factor in [85, 120] range
- ☐ Zero "DATA NULL" in critical fields (Stuff+, K%, lineup K%)
- ☐ Bullpen fatigue values populated (not all zeros)
- ☐ Random seed is DYNAMIC (not fixed)

If ANY check fails: **STOP and report before simulating.**

---

## PHASE 2: ENGINE EXECUTION

### 2A. Run Syndicate Engines
- **K-Prophet V2.0 (DRE)**: Stochastic Volatility & Chaos Injection. Widened distributions for tail-risk preservation. Includes **V16.3 Structural Entropy** (4% disaster chance).
- **HR-Alpha V6.0**: Barrel-rate synergy and ISO-gate thresholding. Attenuated by 50% weight (V16.3 patch).
- **NRFI/YRFI V2.0 (DRE)**: 10,000-iteration Monte Carlo first-inning simulation. **YRFI Disabled** (V16.3 Muzzle).
- **Quant-Elite V6.6**: Anchored to market totals, setting the base-rate atmosphere. Includes **V16.3 Environmental Dampener** (0.90x for standard games).

### 2B. K-PROPHET RECONCILIATION
K-Prophet and QE produce INDEPENDENT K distributions:
- If median K agrees (±1): **HIGH CONVICTION** → use K-Prophet median
- If disagree by ≥2: **FLAG "SPLIT SIGNAL"** → Use weighted: `(K-Prophet × 0.6) + (QE × 0.4)`
- Report disagreement explicitly

### 2C. CALIBRATION APPLICATION
Apply Phase 0 modifier to `total_mu` before reporting.

---

## PHASE 3: DETERMINISTIC OUTPUT

### 3.1 Score Projection (with confidence bands)
```
Away: X.XX [p15 — p85] runs | Win Prob: XX.X%
Home: X.XX [p15 — p85] runs | Win Prob: XX.X%
Total: X.XX [p15 — p85] | Blowout Prob: XX.X% | YRFI Prob: XX.X% (V17 Forensic Model)
```

### 3.2 K-Prophet Precision (Reconciled)
```
SP Name: X K's [ALIGNED/SPLIT SIGNAL]
  K-Prophet: X (μ X.XX) | QE: X (μ X.XX) | Δ=X
  O/U Probabilities: 3.5, 4.5, 5.5, 6.5, 7.5
```

### 3.3 HR-Alpha Targets (>25% probability)

### 3.4 ACE TRAP SCAN
Flag if 2+ conditions met:
1. Stuff+ > 110 but lineup O-Swing% < 27% (discipline kills stuff)
2. xERA > ERA by 0.80+ (regression imminent)
3. Park Factor > 105 AND wind out > 10mph
4. SP on short rest or 100+ pitches last start
5. Bullpen degraded to Tier B/C
6. Umpire zone = 'tight'

### 3.5 BETTING INTELLIGENCE (for each market)
```
MARKET: [Team/Prop] @ [Odds] (implied XX.X%)
MODEL:  XX.X%
EDGE:   +X.X% EV
KELLY:  X.X% (Quarter-Kelly: X.XX%)
VERDICT: BET / FADE / NO EDGE

MARKET: [YRFI/NRFI] @ [Odds] (implied XX.X%)
MODEL:  XX.X%
EDGE:   +X.X% EV
VERDICT: BET / FADE
```
- **V16.3 Financial Guardrail**: Any bet with odds steeper than -250 is an automatic SKIP unless Edge > 10.0%.
- **V16.3 Batter Prop Rule**: Hit props require >= 62% Monte Carlo probability for a BET verdict.
HIGH CONVICTION only when: Edge > 5% AND engines agree AND no Ace Trap AND satisfies V16.3 Guardrails.

---

## PHASE 4: DATA PERSISTENCE (AUTOMATIC)

All simulation runs are **automatically recorded** by `data_recorder.py`. No manual action required during simulation. The following data is persisted:

### 4.1 Automatic (Every Run)
- **`predictions_history.csv`** — Game scores, win probabilities, confidence bands, calibration modifiers, environment data, ace trap flags. Results columns left as TBD for post-game entry.
- **`K Prophet/performance_tracker.csv`** — K-prop projections with reconciliation status (KP median, QE median, ALIGNED/SPLIT_SIGNAL). Actuals left as TBD.
- **`audits/audit_[AWAY]_[HOME]_[DATE].json`** — Complete JSON audit trail with ALL inputs, ALL outputs, and accuracy metrics (filled post-game).
- **`intelligence/matchup_[AWAY]_[HOME]_[DATE].md`** — Structured intelligence report with projections and environment data.

### 4.2 Post-Game Results Recording (MANDATORY AGENT DIRECTIVE — ZERO DATA LOSS POLICY)
When the USER provides game results or player stats directly in a chat, the Agent MUST NOT close the conversation or end its turn without persisting the data. Relying on conversational memory is strictly forbidden. 
The Agent must immediately execute (filling in actual values):
```bash
py record_game.py --away "[AWAY]" --home "[HOME]" --away_score [SCORE] --home_score [SCORE] --away_sp "[NAME]" --home_sp "[NAME]" --away_sp_k [K] --home_sp_k [K] --date [YYYY-MM-DD]
```
If the user provides a full box score, save it to `scratch/raw_box_scores.txt` and add `--box_score "scratch/raw_box_scores.txt"` to the command.

This single command will:
1. Find the matching prediction in `predictions_history.csv` and fill in the result
2. Find the matching K-prop predictions in `performance_tracker.csv` and fill in actuals
3. Update the audit JSON with result data and accuracy metrics
4. (Optional) Parse box score text into `MLB Stats` player game logs

### 4.2.1 Pre-Game Research Data Persistence
When the USER provides pitcher stats, batter stats, or any other data during pre-game research (e.g., Stuff+, K%, wOBA, ERA):
- The `--save_overrides` flag on `auto_sim_v16.py` MUST be used to persist these stats
- If data is provided outside of the sim command (e.g., pasted in chat), the Agent MUST write it to `MLB Stats` directly using an ingestion script
- **NEVER discard user-provided stats** — they represent real-time intelligence that improves future predictions

### 4.2.2 Post-Game Results Persistence
This process will:
1. Find all pending predictions for today
2. Record final scores, K actuals, and player game stats
3. Calculate PNL for any placed bets
4. Update all tracking files (CSV + JSON audits + MLB Stats Database)
5. Feed data back into the calibration loop for the next simulation

### 4.3 Data Flow
```
Simulation → Auto-Record (CSV + JSON + MD) → Game Plays → record_results.py → 
calibration_check.py reads updated data → Next simulation is calibrated
```

---

## ACTIVATION COMMAND
"ENGAGE OMNI-PROPHET V19.1 PROTOCOL: [AWAY] @ [HOME] [DATE]"

**CRITICAL**: Do not proceed to simulation until the Intelligence Report is populated with verified 2026 data. No placeholders. Ensure K-Prophet V2.0 is initialized with Stochastic Volatility enabled.
