# ⚠️ DEPRECATED — Use PREDICTION_PROMPT_V19.md instead
# MLB OMNI-PROPHET V19.0 — PREDICTION PROMPT

> **Copy everything inside the code block below and paste it into a new conversation along with the lineup screenshot.**

---

```
Analyze the attached lineup screenshot.

Step 1: Extract the away/home teams, starting pitchers, and the exact 9-man batting orders.
Step 2: Run this exact bash command to check the local database:

`python3 /Users/danielreiss/Desktop/Antigravity/MLB/auto_sim_v16.py --away "[AWAY]" --home "[HOME]" --away_sp "[AWAY_SP]" --home_sp "[HOME_SP]" --away_sp_hand "[AWAY_SP_HAND]" --home_sp_hand "[HOME_SP_HAND]" --away_lineup "[...]" --home_lineup "[...]" --check_data`

Step 3: Analyze the JSON output.
- If status is "OK": Re-run the command without `--check_data`. Report the exact output.
- If status is "STALE_OR_MISSING": Do NOT search the web for stats. Instead, IMMEDIATELY STOP and ask the user to provide the missing 2026/2025/Career stats for the players listed.
  - Ask the user to provide the data in the following format so you can easily copy it:
    - Pitchers: `Name | K% | BB% | ERA | xFIP | HR/FB% | Starts | IP`
    - Batters: `Name | K% | wOBA`
  - Once the user replies with the stats, re-run the command without `--check_data`, but append `--save_overrides` and the specific overrides (e.g. `--override_sp "Name:18.5%:8.2%:3.10:3.40:12.5%:2:10.1"` and `--override_batter "Name:12.5%:0.380"`). Report the exact output.

Step 4: (Optional) If the user provided betting odds in the screenshot or message, append the `--odds` flag to the final simulation command. 
- Format: `--odds "Label1:Odds1,Label2:Odds2"` (e.g., `--odds "LAD ML:-207,Total Over 8.5:-110"`).

---
### OMNI-PROPHET V19.0 QUALITATIVE ANALYSIS RULES
When analyzing the matchup or considering overrides, apply the following V19.0 Post-Audit Protocol:

**1. Starter Maturity Factor (SMF) Regression:**
- **Rookies (< 5 Starts or < 30 IP):** The engine now automatically regresses these pitchers. 
  - If a rookie has a 0.00 ERA, assume a regression toward the team's Bullpen ERA (e.g., ~4.20). 
  - Be extremely conservative with "Runline" bets on teams starting unproven rookies.

**2. Lineup "Chain Reaction" Clusters:**
- **Power Chains:** Look for sequences of 3+ batters with **wOBA > .350**. 
  - These clusters generate "Blowout Momentum" that standard averages miss. 
  - If a cluster exists, the model's Score Ceiling (p85) is the primary target for Over bets.

**3. Ace Volatility & Stuff+ Buffer:**
- **High Stuff+ (> 115):** These pitchers (e.g., Strider, Bibee) have high ceiling/floor variance. 
  - Expect wider Confidence Intervals (CI). 
  - Do NOT bet heavily on the Under for these pitchers even if their recent ERA is high; their "Stuff" allows for sudden dominance.

**4. K-Prop "Edge" Threshold (The 0.75 Rule):**
- Do NOT recommend a Strikeout bet unless the model's reconciled prediction is at least `abs(0.75)` away from the Vegas line. 
- **Double-Counting Fix:** Never recommend two separate bets on the same pitcher's K-prop (e.g., both Over 5.5 and 7+ Ks). Pick the one with the highest Kelly Criterion.

**5. Month-by-Month Weighting (MAY):**
- 2025 remains the anchor. Use 2026 Stuff+ and Pitcher Leash trends as the primary variance signals. Be skeptical of 2026 ERAs until June.
```
