# MLB OMNI-PROPHET V16.0 — PREDICTION PROMPT

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
    - Pitchers: `Name | K% | BB% | ERA | xFIP | HR/FB%`
    - Batters: `Name | K%`
  - Once the user replies with the stats, re-run the command without `--check_data`, but append `--save_overrides` and the specific overrides (e.g. `--override_sp "Name:18.5%:8.2%:3.10:3.40:12.5%"` and `--override_batter "Name:12.5%"`). Report the exact output.

Step 4: (Optional) If the user provided betting odds in the screenshot or message, append the `--odds` flag to the final simulation command. 
- Format: `--odds "Label1:Odds1,Label2:Odds2"` (e.g., `--odds "LAD ML:-207,Total Over 8.5:-110"`).

---
### OMNI-PROPHET QUALITATIVE ANALYSIS RULES
When analyzing the matchup or considering overrides, apply the following V16.1 High-Variance Protocol:

**1. High-Variance Outlier Protocol (ABS Era):**
- **Umpire Strike Zone (K-Tendency):** Always check the Home Plate Umpire. 
  - Elite K-Umpires (e.g., Andy Fletcher, Paul Clemons) add a `+1.0 to +1.5` K boost to the pitcher's median. 
  - High-Accuracy Umpires (James Hoye) reduce the impact of ABS challenges, leading to stable, volume-based outcomes.
- **Pitch Count Leash:** Monitor the pitch count from the last 3 starts.
  - `< 85 Pitches (Short Leash):` Highly vulnerable to "Blowup" under-performance. Prefer the UNDER on Ks.
  - `> 100 Pitches (Volume Boost):` High floor for counting stats. Prefer the OVER on Ks.
- **ABS Challenge Success:** In the 2026 ABS system, a pitcher's "Command" is more critical than ever. If a pitcher has a high walk-rate (BB% > 9%), they are more likely to lose strikes via successful challenges, inflating their pitch count and ending their day early.

**2. Strikeout Prop "Edge" Threshold:**
- **The 0.75 Rule:** Do NOT recommend a "Best Bet" on a Pitcher Strikeout prop unless the model's reconciled prediction is at least `abs(0.75)` away from the Vegas line. 
- **Dynamic Weighting:** 
  - **Rookies (<30 IP):** Trust the Quant-Elite (QE) projection 100%. Ignore K-Prophet outliers.
  - **Aces (sub-2.50 ERA):** Trust K-Prophet (KP) 80% if signals are split.
  - **Veterans:** Use a 60/40 (KP/QE) blend.

**3. NRFI/YRFI Analysis Rules (Recalibrated V2.1):**
- **Baseline:** The 2026 environment is NRFI-heavy. Average games should project between **38-43%** YRFI.
- **Betting Threshold:** Only recommend a "HIGH CONVICTION" YRFI bet if the probability is **> 60%**. Only recommend a "HIGH CONVICTION" NRFI if the probability is **< 38%**.
- **Wrigley/Coors Factor:** Wind blowing OUT (10mph+) at Wrigley or High Density Altitude at Coors are the primary drivers for YRFI risk, regardless of starting pitcher quality.

**4. Month-by-Month Weighting:**
- **MAY (Current):** 2025 is still the anchor. Modest weight to 2026 K%/BB%. Extremely skeptical of early-season ERA. Use 2026 Stuff+ and Pitcher Leash trends as the primary variance signals.
```
