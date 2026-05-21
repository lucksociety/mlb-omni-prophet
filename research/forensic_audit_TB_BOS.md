# Forensic Audit: TBR @ BOS (2026-05-07)
**Status**: COMPLETE | **Result**: LOSS (Total & K-Prop) | **Win**: NRFI & TBR ML

## 1. The "Whiff" of the Night: Jake Bennett K-Prop
- **Model Projection**: 4.05 K's
- **Market Line**: 3.5 (Over +130)
- **Actual Result**: **1 Strikeout** (5.1 IP)
- **Forensic Breakdown**: 
    - Bennett's 112 Stuff+ was completely neutralized by the Rays' contact-first approach. 
    - **Yandy Diaz (13.8% K)** and **Junior Caminero (19.2% K)** combined for 0 strikeouts against him.
    - **V17 Logic Failure**: The engine weighted Bennett’s "swing-and-miss" profile (Fix 4: Ace Floor) too heavily against a lineup that ranks in the top 5% for Z-Contact (Zone Contact).
- **Calibration**: Update `reconcile_k_projections` to penalize Stuff+ scores when facing lineups with >88% Z-Contact averages.

## 2. Total Variance: Under 8.5 → 12 Runs
- **Model Projection**: 7.67 Runs (Ace Duel)
- **Actual Result**: **12 Runs** (TBR 8-4)
- **Forensic Breakdown**:
    - **Missing Piece**: Jesse Scholtens was listed as the Primary but did not pitch (rescheduled for May 8). The Rays likely used a bullpen-day or lower-tier bulk arm, degrading the pitching quality significantly.
    - **Archetype Error**: The V17 Engine classified this as an "Ace Duel" based on Bennett’s 1.80 ERA. However, his **1.40 WHIP** and **2.15 xERA** were screaming "Regression Trap."
- **Calibration**: Tighten the "Ace Duel" classification. A pitcher with a WHIP > 1.25 or xERA > 2.00 should NEVER trigger the Ace-Duel downward modifier.

## 3. The Bright Spots
- **NRFI (-125)**: ✅ HIT. (Clean 1st inning).
- **TBR Moneyline (-102)**: ✅ HIT. (Rays 8-4).
- **Logic Success**: The engine correctly identified the Rays as the superior team despite the "plus money" market price.

## V18 ENGINE FIXES:
1. **Fix 11: Contact Ceiling**. If Lineup Z-Contact > 87%, cap Pitcher K-Expectancy at 85% of raw projection.
2. **Fix 12: WHIP Regression Anchor**. WHIP > 1.30 now overrides ERA-based "Ace" status.
3. **Fix 13: Bulk/Primary Verification**. Automated cross-check of "Next Start" data to prevent using bulk-relievers on their rest days.
