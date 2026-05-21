# MLB OMNI-PROPHET V20 — ABSOLUTE BEST PREDICTION PROMPT

> **Use this prompt when requesting a high-fidelity, forensic game audit.**

---

```
ENGAGE OMNI-PROPHET V20: Give me your absolute best prediction possible for this game.

[Lineup Screenshot Attached]

PHASE 1: Extract Lineups & Verification
1. Extract Teams, Starting Pitchers, and exact 9-man batting orders.
2. Verify all 2026 Stuff+, K%, and wOBA data in the local database.
3. If data is missing/stale (>2 days), STOP and request stat overrides for:
   - Pitchers: Name | K% | BB% | ERA | xFIP | HR/FB% | Starts | IP | Stuff+
   - Batters: Name | K% | wOBA

PHASE 2: Engine Execution (V20 Unified Singularity)
1. Run all engines (K-Prophet V2.0, HR-Alpha V6.0, YRFI V2.0, Quant-Elite V6.6).
2. Execute 100,000 Monte Carlo iterations.

PHASE 3: Mandatory "Absolute" Output Format
Follow the MLB_ABSOLUTE_BEST_PREDICTION_LAW.md precisely:
- First Inning Prediction + Probability
- First 5 Inning Score + Win/Tie Probabilities
- Strikeout Projections (Both SPs) + O/U Probabilities
- Final Score Predictions + Win Probabilities + Confidence Bands
- Home Run Tracker (>25% Probability Notes)

MANDATORY: All probabilities MUST come from Monte Carlo frequency counts.
```
