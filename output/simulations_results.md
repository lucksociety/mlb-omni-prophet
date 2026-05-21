# MLB Omni-Prophet V16.0 - Tonight's Slate Simulations

## BOS @ DET
**SP:** Brayan Bello vs Framber Valdez

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  BOS @ DET | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  ⚠ WARNING: AWAY SP ERA 9.12 outside [1.50, 8.00] — possible sample size issue
  STATUS: PASS (with warnings)

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x
  [DEBUG] BOS Bullpen: {'A': 2.8449999999999998, 'B': 4.743333333333333, 'C': 5.628000000000001, 'AVG': 4.111585365853659}
  [DEBUG] DET Bullpen: {'A': 2.77, 'B': 4.84, 'C': 5.1450000000000005, 'AVG': 4.124657534246576}
  [DEBUG] Env Factor: 1.000 (PF:1.0 T:1.000 W:1.000 H:1.000 Alt:1.000)
  [DEBUG] BOS: Blended ERA 5.19, wRC+ 84.6, Exp IP 4.66
  [DEBUG] DET: Blended ERA 4.14, wRC+ 112.0, Exp IP 5.74
  [V6.6.1 CALIBRATION] Env factor adjusted: 0.939x (aggressive)
╔══════════════════════════════════════════════════════════════════╗
║        MLB QUANT-ELITE V6.6 | CALIBRATED ENGINE               ║
║        BOS @ DET | DETERMINISTIC STATE ENGINE         ║
╚══════════════════════════════════════════════════════════════════╝

── 1. STATE ENGINE EXPECTANCY (100,000 SIMS) ───────────────────
  BOS: 3.177 runs  |  DET: 5.847 runs
  TOTAL: 9.024 runs
  WIN PROBABILITY: BOS 29.6% | DET 70.4%
  BLOWOUT PROBABILITY (>13 RUNS): 18.6%

── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────
  Brayan Bello - 3.50 K's - Final Prediction: 3 K's
  Framber Valdez - 3.94 K's - Final Prediction: 4 K's

── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────
  [EDGE DETECTED] Run Diff 2.67 >= 1.4. MASSIVE EDGE: CONSIDER RUNLINE (-1.5) FOR DET.

==================================================================
  V6.6 FINAL: BOS 3.18 — DET 5.85
==================================================================

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED FORENSIC REPORT
======================================================================

── 1. SCORE PROJECTION (Calibrated) ────────────────────────────
  BOS: 3.18 [1.0 — 6.0] runs (29.6%)
  DET: 5.85 [2.0 — 11.0] runs (70.4%)
  TOTAL: 8.41 [4.0 — 14.0]
  [CALIBRATION] Systematic SYSTEMATIC_OVER detected. Applied -0.61 run correction.
  BLOWOUT PROB (>13 runs): 18.6%

── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────
  Brayan Bello: 3 K's ✅ [ALIGNED]
    K-Prophet: 3 (μ 3.47) | QE: 3 (μ 3.50) | Δ=0
  Framber Valdez: 4 K's ✅ [ALIGNED]
    K-Prophet: 4 (μ 4.25) | QE: 4 (μ 3.94) | Δ=0

── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────
  [NONE DETECTED]

── 4. ACE TRAP SCAN ────────────────────────────────────────────
  [NO ACE TRAPS DETECTED]

── 5. BETTING INTELLIGENCE ─────────────────────────────────────
  [MASSIVE EDGE] Run Diff 2.67. CONSIDER RUNLINE (-1.5) DET (70.4%)
  (Provide market_odds dict for full Kelly/EV analysis)

── 6. TELEMETRY ────────────────────────────────────────────────
  ADI: N/A | PF: 100
  Umpire: Unknown (neutral)
  Calibration: Total SYSTEMATIC_OVER | K NEUTRAL

======================================================================

── DATA RECORDER ───────────────────────────────────────────────
  ✅ predictions_history.csv  — game score prediction appended
  ✅ performance_tracker.csv  — K-prop predictions appended
  ✅ audits/audit_BOS_DET_2026-05-05_4.json  — full audit trail saved
  ✅ intelligence/matchup_BOS_DET_2026-05-05.md  — intel report saved
  📝 Run 'python3 record_results.py' after game to enter actuals

----------------------------------------
## ATH @ PHI
**SP:** Luis Severino vs Cristopher Sanchez

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  ATH @ PHI | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x
  [DEBUG] ATH Bullpen: {'A': 2.8150000000000004, 'B': 5.37, 'C': 5.9639999999999995, 'AVG': 4.1675}
  [DEBUG] PHI Bullpen: {'A': 3.2249999999999996, 'B': 5.153333333333333, 'C': 7.014, 'AVG': 4.151621621621622}
  [DEBUG] Env Factor: 1.000 (PF:1.0 T:1.000 W:1.000 H:1.000 Alt:1.000)
  [DEBUG] ATH: Blended ERA 4.81, wRC+ 111.9, Exp IP 5.02
  [DEBUG] PHI: Blended ERA 3.28, wRC+ 103.8, Exp IP 5.62
  [V6.6.1 CALIBRATION] Env factor adjusted: 0.939x (aggressive)
╔══════════════════════════════════════════════════════════════════╗
║        MLB QUANT-ELITE V6.6 | CALIBRATED ENGINE               ║
║        ATH @ PHI | DETERMINISTIC STATE ENGINE         ║
╚══════════════════════════════════════════════════════════════════╝

── 1. STATE ENGINE EXPECTANCY (100,000 SIMS) ───────────────────
  ATH: 3.960 runs  |  PHI: 5.007 runs
  TOTAL: 8.968 runs
  WIN PROBABILITY: ATH 41.3% | PHI 58.7%
  BLOWOUT PROBABILITY (>13 RUNS): 18.4%

── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────
  Luis Severino - 4.30 K's - Final Prediction: 4 K's
  Cristopher Sánchez - 6.13 K's - Final Prediction: 6 K's

── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────
  [VOLATILITY WARNING] Cristopher Sánchez projected for high K's but carries early-hook tail risk.
  [EDGE DETECTED] Run Diff 1.05. CONSIDER MONEYLINE FOR PHI.

==================================================================
  V6.6 FINAL: ATH 3.96 — PHI 5.01
==================================================================

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED FORENSIC REPORT
======================================================================

── 1. SCORE PROJECTION (Calibrated) ────────────────────────────
  ATH: 3.96 [1.0 — 7.0] runs (41.3%)
  PHI: 5.01 [1.0 — 9.0] runs (58.7%)
  TOTAL: 8.35 [4.0 — 14.0]
  [CALIBRATION] Systematic SYSTEMATIC_OVER detected. Applied -0.61 run correction.
  BLOWOUT PROB (>13 runs): 18.4%

── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────
  Luis Severino: 4 K's ✅ [ALIGNED]
    K-Prophet: 4 (μ 4.36) | QE: 4 (μ 4.30) | Δ=0
  Cristopher Sánchez: 5 K's ✅ [ALIGNED]
    K-Prophet: 5 (μ 5.98) | QE: 6 (μ 6.13) | Δ=1

── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────
  🔥 Kyle Schwarber (PHI): 37.9%

── 4. ACE TRAP SCAN ────────────────────────────────────────────
  [NO ACE TRAPS DETECTED]

── 5. BETTING INTELLIGENCE ─────────────────────────────────────
  [EDGE] Run Diff 1.05. CONSIDER ML PHI (58.7%)
  (Provide market_odds dict for full Kelly/EV analysis)

── 6. TELEMETRY ────────────────────────────────────────────────
  ADI: N/A | PF: 100
  Umpire: Unknown (neutral)
  Calibration: Total SYSTEMATIC_OVER | K NEUTRAL

======================================================================

── DATA RECORDER ───────────────────────────────────────────────
  ✅ predictions_history.csv  — game score prediction appended
  ✅ performance_tracker.csv  — K-prop predictions appended
  ✅ audits/audit_ATH_PHI_2026-05-05_2.json  — full audit trail saved
  ✅ intelligence/matchup_ATH_PHI_2026-05-05.md  — intel report saved
  📝 Run 'python3 record_results.py' after game to enter actuals

----------------------------------------
## BAL @ MIA
**SP:** Chris Bassitt vs Sandy Alcantara

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  BAL @ MIA | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x
  [DEBUG] BAL Bullpen: {'A': 2.23, 'B': 4.906666666666666, 'C': 6.09, 'AVG': 4.067083333333334}
  [DEBUG] MIA Bullpen: {'A': 3.92, 'B': 4.766666666666667, 'C': 5.25, 'AVG': 4.18025641025641}
  [DEBUG] Env Factor: 1.000 (PF:1.0 T:1.000 W:1.000 H:1.000 Alt:1.000)
  [DEBUG] BAL: Blended ERA 4.91, wRC+ 106.3, Exp IP 4.78
  [DEBUG] MIA: Blended ERA 3.90, wRC+ 113.2, Exp IP 5.42
  [V6.6.1 CALIBRATION] Env factor adjusted: 0.939x (aggressive)
╔══════════════════════════════════════════════════════════════════╗
║        MLB QUANT-ELITE V6.6 | CALIBRATED ENGINE               ║
║        BAL @ MIA | DETERMINISTIC STATE ENGINE         ║
╚══════════════════════════════════════════════════════════════════╝

── 1. STATE ENGINE EXPECTANCY (100,000 SIMS) ───────────────────
  BAL: 4.320 runs  |  MIA: 5.741 runs
  TOTAL: 10.061 runs
  WIN PROBABILITY: BAL 42.3% | MIA 57.7%
  BLOWOUT PROBABILITY (>13 RUNS): 25.0%

── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────
  Chris Bassitt - 3.65 K's - Final Prediction: 3 K's
  Sandy Alcantara - 3.39 K's - Final Prediction: 3 K's

── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────
  [EDGE DETECTED] Run Diff 1.42 >= 1.4. MASSIVE EDGE: CONSIDER RUNLINE (-1.5) FOR MIA.

==================================================================
  V6.6 FINAL: BAL 4.32 — MIA 5.74
==================================================================

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED FORENSIC REPORT
======================================================================

── 1. SCORE PROJECTION (Calibrated) ────────────────────────────
  BAL: 4.32 [1.0 — 7.0] runs (42.3%)
  MIA: 5.74 [2.0 — 11.0] runs (57.7%)
  TOTAL: 9.45 [5.0 — 16.0]
  [CALIBRATION] Systematic SYSTEMATIC_OVER detected. Applied -0.61 run correction.
  BLOWOUT PROB (>13 runs): 25.0%

── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────
  Chris Bassitt: 3 K's ✅ [ALIGNED]
    K-Prophet: 3 (μ 3.31) | QE: 3 (μ 3.65) | Δ=0
  Sandy Alcantara: 4 K's ✅ [ALIGNED]
    K-Prophet: 4 (μ 4.15) | QE: 3 (μ 3.39) | Δ=1

── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────
  [NONE DETECTED]

── 4. ACE TRAP SCAN ────────────────────────────────────────────
  [NO ACE TRAPS DETECTED]

── 5. BETTING INTELLIGENCE ─────────────────────────────────────
  [MASSIVE EDGE] Run Diff 1.42. CONSIDER RUNLINE (-1.5) MIA (57.7%)
  (Provide market_odds dict for full Kelly/EV analysis)

── 6. TELEMETRY ────────────────────────────────────────────────
  ADI: N/A | PF: 100
  Umpire: Unknown (neutral)
  Calibration: Total SYSTEMATIC_OVER | K NEUTRAL

======================================================================

── DATA RECORDER ───────────────────────────────────────────────
  ✅ predictions_history.csv  — game score prediction appended
  ✅ performance_tracker.csv  — K-prop predictions appended
  ✅ audits/audit_BAL_MIA_2026-05-05_3.json  — full audit trail saved
  ✅ intelligence/matchup_BAL_MIA_2026-05-05.md  — intel report saved
  📝 Run 'python3 record_results.py' after game to enter actuals

----------------------------------------
## TB @ TOR
**SP:** Drew Rasmussen vs Kevin Gausman

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  TB @ TOR | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x
  [DEBUG] TB Bullpen: {'A': 3.5, 'B': 5.0, 'C': 6.0, 'AVG': 4.15}
  [DEBUG] TOR Bullpen: {'A': 1.755, 'B': 4.15, 'C': 4.357500000000001, 'AVG': 3.9420289855072466}
  [DEBUG] Env Factor: 1.000 (PF:1.0 T:1.000 W:1.000 H:1.000 Alt:1.000)
  [DEBUG] TB: Blended ERA 3.22, wRC+ 96.4, Exp IP 5.80
  [DEBUG] TOR: Blended ERA 3.24, wRC+ 104.7, Exp IP 5.95
  [V6.6.1 CALIBRATION] Env factor adjusted: 0.939x (aggressive)
╔══════════════════════════════════════════════════════════════════╗
║        MLB QUANT-ELITE V6.6 | CALIBRATED ENGINE               ║
║        TB @ TOR | DETERMINISTIC STATE ENGINE         ║
╚══════════════════════════════════════════════════════════════════╝

── 1. STATE ENGINE EXPECTANCY (100,000 SIMS) ───────────────────
  TB: 2.963 runs  |  TOR: 3.721 runs
  TOTAL: 6.685 runs
  WIN PROBABILITY: TB 41.6% | TOR 58.4%
  BLOWOUT PROBABILITY (>13 RUNS): 6.7%

── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────
  Drew Rasmussen - 5.73 K's - Final Prediction: 6 K's
  Kevin Gausman - 6.62 K's - Final Prediction: 7 K's

── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────
  [VOLATILITY WARNING] Drew Rasmussen projected for high K's but carries early-hook tail risk.
  [VOLATILITY WARNING] Kevin Gausman projected for high K's but carries early-hook tail risk.
  [EDGE DETECTED] Run Diff 0.76. CONSIDER MONEYLINE FOR TOR.

==================================================================
  V6.6 FINAL: TB 2.96 — TOR 3.72
==================================================================

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED FORENSIC REPORT
======================================================================

── 1. SCORE PROJECTION (Calibrated) ────────────────────────────
  TB: 2.96 [1.0 — 6.0] runs (41.6%)
  TOR: 3.72 [1.0 — 6.0] runs (58.4%)
  TOTAL: 6.07 [3.0 — 11.0]
  [CALIBRATION] Systematic SYSTEMATIC_OVER detected. Applied -0.61 run correction.
  BLOWOUT PROB (>13 runs): 6.7%

── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────
  Drew Rasmussen: 5 K's ✅ [ALIGNED]
    K-Prophet: 5 (μ 4.88) | QE: 6 (μ 5.73) | Δ=1
  Kevin Gausman: 6 K's ⚠️ [SPLIT_SIGNAL]
    K-Prophet: 5 (μ 5.34) | QE: 7 (μ 6.62) | Δ=2

── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────
  [NONE DETECTED]

── 4. ACE TRAP SCAN ────────────────────────────────────────────
  [NO ACE TRAPS DETECTED]

── 5. BETTING INTELLIGENCE ─────────────────────────────────────
  [EDGE] Run Diff 0.76. CONSIDER ML TOR (58.4%)
  (Provide market_odds dict for full Kelly/EV analysis)

── 6. TELEMETRY ────────────────────────────────────────────────
  ADI: N/A | PF: 100
  Umpire: Unknown (neutral)
  Calibration: Total SYSTEMATIC_OVER | K NEUTRAL

======================================================================

── DATA RECORDER ───────────────────────────────────────────────
  ✅ predictions_history.csv  — game score prediction appended
  ✅ performance_tracker.csv  — K-prop predictions appended
  ✅ audits/audit_TB_TOR_2026-05-05_2.json  — full audit trail saved
  ✅ intelligence/matchup_TB_TOR_2026-05-05.md  — intel report saved
  📝 Run 'python3 record_results.py' after game to enter actuals

----------------------------------------
## WSH @ MIN
**SP:** Cade Cavalli vs Taj Bradley

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  WSH @ MIN | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x
  [DEBUG] WSH Bullpen: {'A': 3.5, 'B': 5.0, 'C': 6.0, 'AVG': 4.15}
  [DEBUG] MIN Bullpen: {'A': 3.91, 'B': 5.766666666666667, 'C': 6.069000000000001, 'AVG': 4.237631578947369}
  [DEBUG] Env Factor: 1.000 (PF:1.0 T:1.000 W:1.000 H:1.000 Alt:1.000)
  [DEBUG] WSH: Blended ERA 3.91, wRC+ 117.1, Exp IP 5.71
  [DEBUG] MIN: Blended ERA 4.23, wRC+ 91.4, Exp IP 5.04
  [V6.6.1 CALIBRATION] Env factor adjusted: 0.939x (aggressive)
╔══════════════════════════════════════════════════════════════════╗
║        MLB QUANT-ELITE V6.6 | CALIBRATED ENGINE               ║
║        WSH @ MIN | DETERMINISTIC STATE ENGINE         ║
╚══════════════════════════════════════════════════════════════════╝

── 1. STATE ENGINE EXPECTANCY (100,000 SIMS) ───────────────────
  WSH: 5.582 runs  |  MIN: 3.788 runs
  TOTAL: 9.370 runs
  WIN PROBABILITY: WSH 63.4% | MIN 36.6%
  BLOWOUT PROBABILITY (>13 RUNS): 19.7%

── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────
  Cade Cavalli - 6.53 K's - Final Prediction: 6 K's
  Taj Bradley - 4.52 K's - Final Prediction: 4 K's

── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────
  [EDGE DETECTED] Run Diff 1.79 >= 1.4. MASSIVE EDGE: CONSIDER RUNLINE (-1.5) FOR WSH.

==================================================================
  V6.6 FINAL: WSH 5.58 — MIN 3.79
==================================================================

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED FORENSIC REPORT
======================================================================

── 1. SCORE PROJECTION (Calibrated) ────────────────────────────
  WSH: 5.58 [2.0 — 10.0] runs (63.4%)
  MIN: 3.79 [1.0 — 7.0] runs (36.6%)
  TOTAL: 8.76 [4.0 — 15.0]
  [CALIBRATION] Systematic SYSTEMATIC_OVER detected. Applied -0.61 run correction.
  BLOWOUT PROB (>13 runs): 19.7%

── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────
  Cade Cavalli: 5 K's ✅ [ALIGNED]
    K-Prophet: 5 (μ 5.41) | QE: 6 (μ 6.53) | Δ=1
  Taj Bradley: 5 K's ✅ [ALIGNED]
    K-Prophet: 5 (μ 5.25) | QE: 4 (μ 4.52) | Δ=1

── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────
  [NONE DETECTED]

── 4. ACE TRAP SCAN ────────────────────────────────────────────
  [NO ACE TRAPS DETECTED]

── 5. BETTING INTELLIGENCE ─────────────────────────────────────
  [MASSIVE EDGE] Run Diff 1.79. CONSIDER RUNLINE (-1.5) WSH (63.4%)
  (Provide market_odds dict for full Kelly/EV analysis)

── 6. TELEMETRY ────────────────────────────────────────────────
  ADI: N/A | PF: 100
  Umpire: Unknown (neutral)
  Calibration: Total SYSTEMATIC_OVER | K NEUTRAL

======================================================================

── DATA RECORDER ───────────────────────────────────────────────
  ✅ predictions_history.csv  — game score prediction appended
  ✅ performance_tracker.csv  — K-prop predictions appended
  ✅ audits/audit_WSH_MIN_2026-05-05_2.json  — full audit trail saved
  ✅ intelligence/matchup_WSH_MIN_2026-05-05.md  — intel report saved
  📝 Run 'python3 record_results.py' after game to enter actuals

----------------------------------------
## TEX @ NYY
**SP:** Jacob deGrom vs Elmer Rodriguez

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  TEX @ NYY | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x
  [DEBUG] TEX Bullpen: {'A': 3.22, 'B': 4.5, 'C': 5.460000000000001, 'AVG': 4.1010526315789475}
  [DEBUG] NYY Bullpen: {'A': 2.3, 'B': 4.783333333333333, 'C': 5.817, 'AVG': 4.034387755102041}
  [DEBUG] Env Factor: 1.000 (PF:1.0 T:1.000 W:1.000 H:1.000 Alt:1.000)
  [DEBUG] TEX: Blended ERA 3.17, wRC+ 102.2, Exp IP 5.73
  [DEBUG] NYY: Blended ERA 4.53, wRC+ 109.0, Exp IP 5.19
  [V6.6.1 CALIBRATION] Env factor adjusted: 0.939x (aggressive)
╔══════════════════════════════════════════════════════════════════╗
║        MLB QUANT-ELITE V6.6 | CALIBRATED ENGINE               ║
║        TEX @ NYY | DETERMINISTIC STATE ENGINE         ║
╚══════════════════════════════════════════════════════════════════╝

── 1. STATE ENGINE EXPECTANCY (100,000 SIMS) ───────────────────
  TEX: 4.689 runs  |  NYY: 4.165 runs
  TOTAL: 8.854 runs
  WIN PROBABILITY: TEX 53.5% | NYY 46.5%
  BLOWOUT PROBABILITY (>13 RUNS): 16.8%

── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────
  Jacob deGrom - 6.98 K's - Final Prediction: 7 K's
  Eduardo Rodriguez - 2.86 K's - Final Prediction: 3 K's

── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────
  [VOLATILITY WARNING] Jacob deGrom projected for high K's but carries early-hook tail risk.
  [EDGE DETECTED] Run Diff 0.52. CONSIDER MONEYLINE FOR TEX.

==================================================================
  V6.6 FINAL: TEX 4.69 — NYY 4.16
==================================================================

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED FORENSIC REPORT
======================================================================

── 1. SCORE PROJECTION (Calibrated) ────────────────────────────
  TEX: 4.69 [1.0 — 8.0] runs (53.5%)
  NYY: 4.16 [1.0 — 7.0] runs (46.5%)
  TOTAL: 8.24 [4.0 — 14.0]
  [CALIBRATION] Systematic SYSTEMATIC_OVER detected. Applied -0.61 run correction.
  BLOWOUT PROB (>13 runs): 16.8%

── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────
  Jacob deGrom: 6 K's ✅ [ALIGNED]
    K-Prophet: 6 (μ 5.78) | QE: 7 (μ 6.98) | Δ=1
  Eduardo Rodriguez: 3 K's ✅ [ALIGNED]
    K-Prophet: 3 (μ 3.80) | QE: 3 (μ 2.86) | Δ=0

── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────
  [NONE DETECTED]

── 4. ACE TRAP SCAN ────────────────────────────────────────────
  [NO ACE TRAPS DETECTED]

── 5. BETTING INTELLIGENCE ─────────────────────────────────────
  [EDGE] Run Diff 0.52. CONSIDER ML TEX (53.5%)
  (Provide market_odds dict for full Kelly/EV analysis)

── 6. TELEMETRY ────────────────────────────────────────────────
  ADI: N/A | PF: 100
  Umpire: Unknown (neutral)
  Calibration: Total SYSTEMATIC_OVER | K NEUTRAL

======================================================================

── DATA RECORDER ───────────────────────────────────────────────
  ✅ predictions_history.csv  — game score prediction appended
  ✅ performance_tracker.csv  — K-prop predictions appended
  ✅ audits/audit_TEX_NYY_2026-05-05_2.json  — full audit trail saved
  ✅ intelligence/matchup_TEX_NYY_2026-05-05.md  — intel report saved
  📝 Run 'python3 record_results.py' after game to enter actuals

----------------------------------------
## KC @ CLE
**SP:** Stephen Kolek vs Gavin Williams

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  KC @ CLE | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x
  [DEBUG] KC Bullpen: {'A': 3.5, 'B': 5.0, 'C': 6.0, 'AVG': 4.15}
  [DEBUG] CLE Bullpen: {'A': 2.98, 'B': 4.87, 'C': 5.2185, 'AVG': 4.1166265060240965}
  [DEBUG] Env Factor: 1.000 (PF:1.0 T:1.000 W:1.000 H:1.000 Alt:1.000)
  [DEBUG] KC: Blended ERA 4.12, wRC+ 102.8, Exp IP 5.59
  [DEBUG] CLE: Blended ERA 4.23, wRC+ 92.6, Exp IP 5.33
  [V6.6.1 CALIBRATION] Env factor adjusted: 0.939x (aggressive)
╔══════════════════════════════════════════════════════════════════╗
║        MLB QUANT-ELITE V6.6 | CALIBRATED ENGINE               ║
║        KC @ CLE | DETERMINISTIC STATE ENGINE         ║
╚══════════════════════════════════════════════════════════════════╝

── 1. STATE ENGINE EXPECTANCY (100,000 SIMS) ───────────────────
  KC: 4.494 runs  |  CLE: 3.915 runs
  TOTAL: 8.408 runs
  WIN PROBABILITY: KC 54.4% | CLE 45.6%
  BLOWOUT PROBABILITY (>13 RUNS): 14.1%

── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────
  Stephen Kolek - 5.01 K's - Final Prediction: 5 K's
  Gavin Williams - 5.88 K's - Final Prediction: 6 K's

── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────
  [VOLATILITY WARNING] Gavin Williams projected for high K's but carries early-hook tail risk.
  [EDGE DETECTED] Run Diff 0.58. CONSIDER MONEYLINE FOR KC.

==================================================================
  V6.6 FINAL: KC 4.49 — CLE 3.91
==================================================================

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED FORENSIC REPORT
======================================================================

── 1. SCORE PROJECTION (Calibrated) ────────────────────────────
  KC: 4.49 [1.0 — 8.0] runs (54.4%)
  CLE: 3.91 [1.0 — 7.0] runs (45.6%)
  TOTAL: 7.79 [4.0 — 13.0]
  [CALIBRATION] Systematic SYSTEMATIC_OVER detected. Applied -0.61 run correction.
  BLOWOUT PROB (>13 runs): 14.1%

── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────
  Stephen Kolek: 4 K's ✅ [ALIGNED]
    K-Prophet: 4 (μ 4.41) | QE: 5 (μ 5.01) | Δ=1
  Gavin Williams: 5 K's ✅ [ALIGNED]
    K-Prophet: 5 (μ 5.18) | QE: 6 (μ 5.88) | Δ=1

── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────
  [NONE DETECTED]

── 4. ACE TRAP SCAN ────────────────────────────────────────────
  [NO ACE TRAPS DETECTED]

── 5. BETTING INTELLIGENCE ─────────────────────────────────────
  [EDGE] Run Diff 0.58. CONSIDER ML KC (54.4%)
  (Provide market_odds dict for full Kelly/EV analysis)

── 6. TELEMETRY ────────────────────────────────────────────────
  ADI: N/A | PF: 100
  Umpire: Unknown (neutral)
  Calibration: Total SYSTEMATIC_OVER | K NEUTRAL

======================================================================

── DATA RECORDER ───────────────────────────────────────────────
  ✅ predictions_history.csv  — game score prediction appended
  ✅ performance_tracker.csv  — K-prop predictions appended
  ✅ audits/audit_KC_CLE_2026-05-05_2.json  — full audit trail saved
  ✅ intelligence/matchup_KC_CLE_2026-05-05.md  — intel report saved
  📝 Run 'python3 record_results.py' after game to enter actuals

----------------------------------------
## CIN @ CHC
**SP:** Andrew Abbott vs Jameson Taillon

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  CIN @ CHC | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x

----------------------------------------
## MIL @ STL
**SP:** Brandon Sproat vs Andre Pallante

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  MIL @ STL | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x
  [DEBUG] MIL Bullpen: {'A': 2.76, 'B': 4.556666666666666, 'C': 4.8615, 'AVG': 4.091449275362319}
  [DEBUG] STL Bullpen: {'A': 3.09, 'B': 5.736666666666667, 'C': 6.7410000000000005, 'AVG': 4.2292}
  [DEBUG] Env Factor: 1.000 (PF:1.0 T:1.000 W:1.000 H:1.000 Alt:1.000)
  [DEBUG] MIL: Blended ERA 5.00, wRC+ 110.7, Exp IP 4.71
  [DEBUG] STL: Blended ERA 4.28, wRC+ 114.3, Exp IP 5.15
  [V6.6.1 CALIBRATION] Env factor adjusted: 0.939x (aggressive)
╔══════════════════════════════════════════════════════════════════╗
║        MLB QUANT-ELITE V6.6 | CALIBRATED ENGINE               ║
║        MIL @ STL | DETERMINISTIC STATE ENGINE         ║
╚══════════════════════════════════════════════════════════════════╝

── 1. STATE ENGINE EXPECTANCY (100,000 SIMS) ───────────────────
  MIL: 5.187 runs  |  STL: 5.552 runs
  TOTAL: 10.739 runs
  WIN PROBABILITY: MIL 46.0% | STL 54.0%
  BLOWOUT PROBABILITY (>13 RUNS): 28.2%

── 2. PITCHER PROP PROJECTIONS ────────────────────────────────────
  Brandon Sproat - 3.53 K's - Final Prediction: 3 K's
  Andre Pallante - 3.68 K's - Final Prediction: 3 K's

── 3. BETTING INTELLIGENCE FLAGS ──────────────────────────────────
  [WARNING] Run Diff 0.37 < 0.5. TOSS-UP: FADE MONEYLINE.
  [ACTION] Focus on Game Totals or Pitcher Unders.

==================================================================
  V6.6 FINAL: MIL 5.19 — STL 5.55
==================================================================

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED FORENSIC REPORT
======================================================================

── 1. SCORE PROJECTION (Calibrated) ────────────────────────────
  MIL: 5.19 [2.0 — 9.0] runs (46.0%)
  STL: 5.55 [2.0 — 10.0] runs (54.0%)
  TOTAL: 10.13 [5.0 — 17.0]
  [CALIBRATION] Systematic SYSTEMATIC_OVER detected. Applied -0.61 run correction.
  BLOWOUT PROB (>13 runs): 28.2%

── 2. K-PROPHET PRECISION (Reconciled) ─────────────────────────
  Brandon Sproat: 4 K's ✅ [ALIGNED]
    K-Prophet: 4 (μ 4.38) | QE: 3 (μ 3.53) | Δ=1
  Andre Pallante: 4 K's ✅ [ALIGNED]
    K-Prophet: 4 (μ 3.92) | QE: 3 (μ 3.68) | Δ=1

── 3. HR-ALPHA TARGETS (>25% PROBABILITY) ──────────────────────
  [NONE DETECTED]

── 4. ACE TRAP SCAN ────────────────────────────────────────────
  [NO ACE TRAPS DETECTED]

── 5. BETTING INTELLIGENCE ─────────────────────────────────────
  [TOSS-UP] Run Diff 0.37 < 0.5. FADE MONEYLINE. Focus totals/props.
  (Provide market_odds dict for full Kelly/EV analysis)

── 6. TELEMETRY ────────────────────────────────────────────────
  ADI: N/A | PF: 100
  Umpire: Unknown (neutral)
  Calibration: Total SYSTEMATIC_OVER | K NEUTRAL

======================================================================

── DATA RECORDER ───────────────────────────────────────────────
  ✅ predictions_history.csv  — game score prediction appended
  ✅ performance_tracker.csv  — K-prop predictions appended
  ✅ audits/audit_MIL_STL_2026-05-05_2.json  — full audit trail saved
  ✅ intelligence/matchup_MIL_STL_2026-05-05.md  — intel report saved
  📝 Run 'python3 record_results.py' after game to enter actuals

----------------------------------------
## LAD @ HOU
**SP:** Shohei Ohtani vs Peter Lambert

======================================================================
  OMNI-PROPHET V16.0 | CALIBRATED & ANCHORED ENGINE
  LAD @ HOU | 2026-05-05 17:31
======================================================================
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================

── PRE-FLIGHT CHECK ─────────────────────────────────────────────
  STATUS: PASS

  [1/3] Running K-Prophet V11.0 Engine...
  [2/3] Running HR-Alpha Engine...
  [3/3] Running Quant-Elite V6.6 Score Engine...
╔══════════════════════════════════════════════════════════════════╗
║          OMNI-PROPHET V15.0 | CALIBRATION CHECK                ║
╚══════════════════════════════════════════════════════════════════╝

── 1. GAME TOTAL BIAS ANALYSIS (last 10 games) ──────────
  Bias Detected: SYSTEMATIC_OVER
  Mean Error (Actual - Predicted): -4.09 runs
  MAE: 4.09 runs
  Undershot: 0% | Overshot: 100%
  → CALIBRATION MODIFIER: -0.61 runs to total

── 2. K-PROP BIAS ANALYSIS (last 20 props) ───────────────
  Bias Detected: NEUTRAL
  Mean Signed Error: -0.19 K's
  MAE: 2.46 K's
  Bet Record: 5W - 4L (55.6%)
  Total PNL: +0.47 units
  Exact Hit %: 20.0% | Within ±1.5: 30.0%
  Over Bets: 1/2 | Under Bets: 3/6
  → K/9 MODIFIER: 1.000x

── 3. MONEYLINE DIRECTION ACCURACY ──────────────────────────────
  Direction Correct: 7/10 (70.0%)

── 4. PER-PITCHER K INTELLIGENCE (23 pitchers tracked) ──

==================================================================
  [V6.6 CALIBRATION] Total Modifier: -0.61 | K/9 Modifier: 1.000x

----------------------------------------
