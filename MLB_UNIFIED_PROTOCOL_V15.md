# MLB OMNI-PROPHET V15.0: CALIBRATED FORENSIC PROTOCOL

**Status**: ACTIVE | **Engine**: Chaos Engine V15.0 | **Mandate**: Calibrated Deterministic Simulation

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

## PHASE 1: DATA HARVEST (Bind to `omni_prophet_v15.py` inputs)

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

### 2A. Run `omni_prophet_v15.py`
- K-Prophet V11.0 (10,000 iterations)
- HR-Alpha probability scan
- Quant-Elite V6.5 (100,000 iterations)

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
Total: X.XX [p15 — p85] | Blowout Prob: XX.X%
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
```
HIGH CONVICTION only when: Edge > 5% AND engines agree AND no Ace Trap.

---

## PHASE 4: DATA PERSISTENCE (AUTOMATIC)

All simulation runs are **automatically recorded** by `data_recorder.py`. No manual action required during simulation. The following data is persisted:

### 4.1 Automatic (Every Run)
- **`predictions_history.csv`** — Game scores, win probabilities, confidence bands, calibration modifiers, environment data, ace trap flags. Results columns left as TBD for post-game entry.
- **`K Prophet/performance_tracker.csv`** — K-prop projections with reconciliation status (KP median, QE median, ALIGNED/SPLIT_SIGNAL). Actuals left as TBD.
- **`audits/audit_[AWAY]_[HOME]_[DATE].json`** — Complete JSON audit trail with ALL inputs, ALL outputs, and accuracy metrics (filled post-game).
- **`intelligence/matchup_[AWAY]_[HOME]_[DATE].md`** — Structured intelligence report with projections and environment data.

### 4.2 Post-Game (Manual)
After the game completes, run:
```
python3 record_results.py
```
This interactive tool will:
1. Find all pending predictions for today (or a specified date)
2. Prompt for final scores and K actuals
3. Calculate PNL for any placed bets
4. Update all tracking files (CSV + JSON audits)
5. Feed data back into the calibration loop for the next simulation

### 4.3 Data Flow
```
Simulation → Auto-Record (CSV + JSON + MD) → Game Plays → record_results.py → 
calibration_check.py reads updated data → Next simulation is calibrated
```

---

## ACTIVATION COMMAND
"ENGAGE OMNI-PROPHET V15.0 PROTOCOL: [AWAY] @ [HOME] [DATE]"

**CRITICAL**: Do not proceed to simulation until the Intelligence Report is populated with verified 2026 data. No placeholders. Use real-time Statcast telemetry.
