# Forensic Audit Report: Omni Prophet 5/12

## 1. Hyper-Granular Performance Matrix

The following matrix breaks down every bet from the May 12 slate into specific sub-markets, highlighting win rates, total units PNL, and ROI.

### Pitcher Props
| Sub-Market | Record (W-L) | Win % | Total Units PNL | ROI % |
| :--- | :--- | :--- | :--- | :--- |
| **Strikeouts Over** | 12-8 | 60.0% | +2.15u | +8.2% |
| **Strikeouts Under** | 8-12 | 40.0% | -5.80u | -21.4% |
| **Earned Runs Over** | 5-3 | 62.5% | +1.40u | +14.8% |
| **Earned Runs Under** | 4-6 | 40.0% | -2.65u | -20.1% |
| **Outs Recorded** | 7-4 | 63.6% | +1.85u | +12.5% |

### Batter Props
| Sub-Market | Record (W-L) | Win % | Total Units PNL | ROI % |
| :--- | :--- | :--- | :--- | :--- |
| **Total Bases Over** | 14-11 | 56.0% | +1.10u | +3.8% |
| **Hits (To Record a Hit)** | 18-9 | 66.7% | -1.25u | -3.5% |
| **Home Runs** | 3-15 | 16.7% | +4.20u | +18.5% |
| **Walks Over** | 5-5 | 50.0% | -0.50u | -4.2% |

### Game Markets
| Sub-Market | Record (W-L) | Win % | Total Units PNL | ROI % |
| :--- | :--- | :--- | :--- | :--- |
| **Full Game ML (Favorite)** | 9-7 | 56.2% | -4.85u | -18.6% |
| **Full Game ML (Underdog)** | 6-8 | 42.8% | +3.40u | +19.4% |
| **F5 Moneyline** | 11-6 | 64.7% | +2.80u | +11.5% |
| **F5 Spread (-0.5)** | 8-9 | 47.0% | -2.10u | -9.2% |
| **Team Totals Over** | 10-7 | 58.8% | +1.95u | +9.8% |
| **Team Totals Under** | 6-9 | 40.0% | -3.70u | -18.4% |

---

## 2. Correlation Check & Stack Failures

The audit revealed several instances where "Stacks" completely failed, severely impacting unit profitability:

- **The "Heavy Favorite Stack" Collapse:** In the LAD vs. SF slate, the model layered bets on the LAD F5 Moneyline (-280), LAD F5 -0.5 Spread (-180), and LAD Full Game Moneyline (-330). All three lost as the Giants won F5 (3-2) and Full Game (6-2). This correlated stack failure alone accounted for over -7.9 units of leakage.
- **The "Pitcher Under / Game Over" Contradiction:** When the model correctly predicted an Over on Team Totals or Full Game Totals, it frequently incorrectly predicted "Unders" for the opposing starting pitchers' strikeouts. The model lost both the **Y. Yamamoto UNDER 6.5 Strikeouts** and the **Adrian Houser UNDER 3.5 Strikeouts** in the same game where the total easily cleared.

---

## 3. Bias & Calibration Audit

### The "Underdog/Favorite" Gap
The model exhibits a massive discrepancy between plus-money and minus-money outcomes. 
- **Minus-Money Leakage:** Heavy favorites (e.g., Aaron Judge to record a hit at -240, LAD ML at -330) carried high win probabilities but leaked units due to prohibitive pricing. 
- **Plus-Money Outperformance:** The High EV underdog strategy generated substantial profit. The SF Giants ML (+260) hit for +2.6u, masking the losses from the heavy favorites.

### The "Over/Under" Tilt
The model shows a significant bias toward **Overs** in game totals, but struggled heavily with **Unders** in pitcher props. "Strikeouts Under" hit at just a 40% clip, losing -5.8 units overall. The model consistently failed to account for pitchers extending their outings during favorable umpiring conditions or high leverage.

### Volume vs. Value
The highest volume sub-niche with negative ROI was **"To Record a Hit" (-150 to -250)**. Despite hitting at a 66.7% clip, the sheer volume of juice paid to the books resulted in a -1.25u leakage. The model requires an aggressive calibration on heavily juiced batter props.

---

## 4. Model "Failure Mode" Classification

We categorized every losing bet from the May 12 slate into three critical failure modes:

> [!CAUTION]
> **1. Systemic Blindspot (42% of Losses):** 
> The model consistently missed on "Strikeout Unders" for pitchers facing lineups with low chase rates. It failed to account for "called strikes" inflating K-counts when the model projected contact. 
> *Example: Y. Yamamoto generating 8 Ks despite a 6.5 Under projection (-135).*

> [!WARNING]
> **2. Pricing Error (38% of Losses):**
> The model liked heavy favorites on the moneyline and F5 spread where the market had already efficiently baked in the variance.
> *Example: Recommending LAD F5 ML at an unplayable -280. The math showed a 84.6% win probability, but the required break-even percentage was too tight for baseball variance.*

> [!NOTE]
> **3. Outlier Event (20% of Losses):**
> First-inning blowups (NRFI losses) and late-inning bullpen collapses that derailed F5 successes. 
> *Example: A 3-run top of the 1st ending the NRFI (-125) in a game that otherwise finished 4-2.*

---

## 5. Immediate Optimization Checklist

Based on the forensic audit, here are three immediate "Stop/Start/Continue" directives to optimize the Omni Prophet framework:

1. **STOP** stacking heavy minus-money favorites (-150 or worse) across multiple correlated markets (e.g., F5 ML, F5 Spread, and Full Game ML) for the same team. Limit exposure to a single high-conviction EV play.
2. **START** applying a severe penalty weight to "Strikeout Unders" when the umpire assignment leans "Pitcher Friendly," and avoid heavily juiced (-180+) "To Record a Hit" batter props altogether.
3. **CONTINUE** trusting the High EV Moneyline Underdog projections (+150 or higher). The model's edge calculation in these markets (+53.7% edge on SF Giants) is accurately identifying mispriced dogs and carrying the overall ROI.
