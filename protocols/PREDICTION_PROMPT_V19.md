# MLB OMNI-PROPHET V19.1 — PREDICTION PROMPT

> **Copy everything inside the code block below and paste it into a new conversation along with the lineup screenshot.**

---

```
Analyze the attached lineup screenshot.

Step 1: Extract the away/home teams, starting pitchers, and the exact 9-man batting orders.
Step 2: Run this exact command to check the local database:

`py "c:\Users\dreis\OneDrive\Desktop\Antigravity\MLB\auto_sim_v16.py" --away "[AWAY]" --home "[HOME]" --away_sp "[AWAY_SP]" --home_sp "[HOME_SP]" --away_sp_hand "[AWAY_SP_HAND]" --home_sp_hand "[HOME_SP_HAND]" --away_lineup "[...]" --home_lineup "[...]" --check_data`

Step 3: Analyze the JSON output.
- If status is "OK": Re-run the command without `--check_data`. Report the exact output.
- If status is "STALE_OR_MISSING": Do NOT search the web for stats. Instead, IMMEDIATELY STOP and ask the user to provide the missing 2026/2025/Career stats for the players listed.
  - Ask the user to provide the data in the following format so you can easily copy it:
    - Pitchers: `Name | K% | BB% | ERA | xFIP | HR/FB% | Starts | IP | Stuff+`
    - Batters: `Name | K% | wOBA`
  - Once the user replies with the stats, re-run the command without `--check_data`, but append `--save_overrides` and the specific overrides. Report the exact output.
  - **MANDATORY**: All stat overrides provided by the user MUST be persisted into `MLB Stats` via `--save_overrides`. Do NOT discard user-provided data.

Step 4: (Optional) If the user provided betting odds in the screenshot or message, append the `--odds` flag to the final simulation command. 
- Format: `--odds "Label1:Odds1,Label2:Odds2"` (e.g., `--odds "LAD ML:-207,Total Over 8.5:-110"`).

Step 5: POST-GAME RESULTS RECORDING (MANDATORY — ZERO-LOSS POLICY)
- If the user provides ANY game data — final scores, player stats, box scores, K totals — YOU MUST NOT SIMPLY ACKNOWLEDGE IT.
- You MUST immediately execute this command (filling in the actual values):
  ```
  py "c:\Users\dreis\OneDrive\Desktop\Antigravity\MLB\record_game.py" --away "[AWAY]" --home "[HOME]" --away_score [SCORE] --home_score [SCORE] --away_sp "[NAME]" --home_sp "[NAME]" --away_sp_k [K] --home_sp_k [K] --date [YYYY-MM-DD]
  ```
- If the user provides a full box score, save it to `scratch/raw_box_scores.txt` and add `--box_score "scratch/raw_box_scores.txt"` to the command.
- **CRITICAL**: Relying on chat memory for data retention is strictly forbidden. Every single stat that comes through MUST be recorded.
- **NEVER close or end a conversation** without first confirming all data has been written to disk.

---
### OMNI-PROPHET V19.1 QUALITATIVE ANALYSIS RULES
When analyzing the matchup or considering overrides, apply the following V19.1 Post-Audit Protocol:

**1. Starter Maturity Factor (SMF) Regression:**
- **Rookies (< 5 Starts or < 30 IP):** The engine automatically regresses these pitchers. 
  - If a rookie has a 0.00 ERA, assume a regression toward the team's Bullpen ERA (~4.20). 
  - Be extremely conservative with "Runline" bets on teams starting unproven rookies.
  - **K Props for Rookies:** Trust QE 100%. Do NOT bet K props on pitchers with < 3 starts.

**2. Lineup "Chain Reaction" Clusters:**
- **Power Chains:** Look for sequences of 3+ batters with **wOBA > .350**. 
  - These clusters generate "Blowout Momentum" that standard averages miss. 
  - If a cluster exists, the model's Score Ceiling (p85) is the primary target for Over bets.

**3. K-Prop "Precision Mode" (V19.1 Overhaul):**
- **Distribution-Based Evaluation (NEW):** The model now outputs `k_line_probs` — the probability of hitting each K line (Over 3.5, 4.5, 5.5, 6.5, 7.5).
  - Only recommend a K bet if the **blended probability exceeds 55%** for the side you're betting.
  - Do NOT bet based on median alone. A pitcher with median 6 but 48% chance of hitting Over 5.5 is a PASS.
- **Edge Threshold (Tightened):**
  - **Veterans:** Only bet if the model's K projection is at least **1.0 K** away from the Vegas line.
  - **Proven Aces (ERA < 2.50 AND IP > 50 AND Stuff+ > 105):** Use 0.75 K edge threshold.
  - **Rookies (< 30 IP):** Do NOT bet K props. Period.
- **Double-Counting Fix:** Never recommend two separate bets on the same pitcher's K-prop (e.g., both Over 5.5 and 7+ Ks). Pick the one with the highest Kelly Criterion.
- **Game Flow Awareness (NEW):** The model now adjusts K projections based on projected blowout risk.
  - If the pitcher has a high ERA (projected to allow > 4.5 runs), K projection is dampened by 12%.
  - If the pitcher has a low ERA (projected < 2.5 runs allowed), K projection is boosted by 8%.

**4. Ace Override Rules (Tightened):**
- **Old Rule:** Any pitcher with ERA < 2.50 got a K floor of 6. This caused false positives.
- **New Rule:** Ace override ONLY triggers if ALL THREE conditions are met:
  - ERA < 2.50
  - IP >= 50 (proven track record)
  - Stuff+ > 105 (confirmed elite arsenal)

**5. Month-by-Month Weighting (MAY):**
- 2025 remains the anchor. Use 2026 Stuff+ and Pitcher Leash trends as the primary variance signals. Be skeptical of 2026 ERAs until June.

**6. Statistical Overdispersion & Distribution Health (NEW):**
- **WRITTEN IN STONE**: All simulations MUST adhere to the `CALIBRATION_BIBLE.md` guardrails.
- **Tail Preservation**: The model must never produce an Under/Over probability > 85% for outcomes within ±1.5 K's of the mean.
- **Verification**: Ensure `auto_sim_v16.py` outputs the "V20.1 CALIBRATION" health check on startup.
```
