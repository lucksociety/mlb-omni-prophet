# MLB Omni Prophet - Dashboard Generation Rules

This document outlines the hardcoded filtering rules, probability thresholds, and search algorithms currently active in `scripts/generate_dashboard.py`. These rules govern what bets qualify for the dashboard each day.

## 1. VIP Best Bets
The algorithm selects the **Top 10** most profitable bets (+EV) across the entire slate that meet the following strict criteria:
* **Win Probability:** Must be **>= 55.0%**
* **Odds:** Must be **-145 or better** (e.g., -144, +110, etc. -146 is explicitly filtered out).

## 2. Top Matchup Bets
For each individual game on the slate, the dashboard lists the **Top 3** +EV bets for that specific matchup, sorted by highest Expected Value.

## 3. Full Game ML / RL (Moneyline / Runline)
Any full game line (Moneyline or Runline) displayed must meet the following baseline:
* **Win Probability:** Must be **>= 48.0%**

## 4. HR Derby (Home Run Props)
Because Home Run props are inherently longshots, they have a unique probability baseline to filter out mathematically terrible bets:
* **Win Probability:** Must be **>= 20.0%**

## 5. MLB Parlay of the Day
The system uses a mathematical combinatorial search to find the mathematically safest parlay possible that pays out at least even money.
* **Payout:** Must be **+100 (Even Money) or better**.
* **Probability:** The combined parlay win probability must be strictly **> 50.0%**.
* **Structure:** No Same-Game Parlays (maximum 1 bet per matchup).
* **Selection:** The engine searches all possible combinations and selects the one with the **highest absolute win probability** that meets the +100 payout threshold.

## 6. MLB Lotto of the Day
The system uses an advanced Branch-and-Bound optimization search with a Pareto frontier filter to find the safest possible high-payout lotto ticket.
* **Payout:** Must be **+500 or better**.
* **Structure:** Must contain **at least 2 legs**.
* **Structure:** No Same-Game Parlays (maximum 1 bet per matchup).
* **Selection:** The engine explores the combination tree and selects the exact combination that reaches +500 with the **highest absolute win probability** mathematically possible.

---
*Note: Because these rules are hardcoded into the Python generation script (`generate_dashboard.py`), they are permanently saved and will automatically apply exactly as written when the dashboard is generated tomorrow.*
