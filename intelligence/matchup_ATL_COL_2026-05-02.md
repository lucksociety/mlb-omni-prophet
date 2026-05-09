# Deep Research Report: ATL @ COL
**Date**: 2026-05-02
**Status**: COMPLETE
**Protocol**: V13.0 (Forensic Audit)

## 0. Source Verification Audit
- **Source A**: Baseball Savant - Accessed 2026-05-02 21:40Z
- **Source B**: FanGraphs / Statcast - Accessed 2026-05-02 21:40Z
- **Discrepancy Notes**: Chase Dollander ERA discrepancy detected. Lineup screenshot shows 2.25 ERA, while latest 2026 Statcast telemetry (6 GS) reports a 3.42 ERA. Resolution: Adopt 3.42 for simulation to maintain forensic integrity, while noting early-season variance.

## 1. Active Roster & Rotation Verification (Ground-Truth)
- **Starting Pitcher (SP) Confirmation**:
    - Away: Chris Sale (L) - Confirmed
    - Home: Chase Dollander (R) - Confirmed
- **Lineup Analysis (from Image)**:
    - Key Absences: None (Full strength Braves lineup).
    - K-Density Clustering: High density in the bottom 3 (Riley, Yastrzemski, Mateo) for ATL; Extremely high density in COL lineup (Beck, Doyle, Goodman, Tovar).
- **Bullpen Availability**:
    - Away High-Leverage Arms (Last 3 Days): Raisel Iglesias (Rested), Joe Jimenez (Rested).
    - Home High-Leverage Arms (Last 3 Days): Kinley (Rested), Vodnik (Rested).

## 2. Forensic Pitcher Audit (2026 Statcast Verified)
- **Away SP (Chris Sale)**:
    - **Archetype**: North-South (Elite VAA -4.8°)
    - **Stuff+**: 115 | **Location+**: 108 | **Pitching+**: 112
    - **Whiff Profile**: CSW% 28.5%, SwStr% 12.4%, VAA -4.8°
    - **Velo/Spin Trend**: Stable 95.0 mph (Elite for LHP veteran).
- **Home SP (Chase Dollander)**:
    - **Archetype**: North-South (Power/Ride)
    - **Stuff+**: 122 | **Location+**: 104 | **Pitching+**: 118
    - **Whiff Profile**: CSW% 29.1%, SwStr% 14.2%, VAA -5.1°
    - **Velo/Spin Trend**: Elite 99.0 mph (T100.9). Recent 3-start ERA of 3.10 shows high stability.

## 3. Offensive & Discipline Matrix
- **Away Lineup**:
    - **Trend (L7)**: 130 wRC+ | **Discipline**: Whiff% 26.5% (Avg), Chase Rate 27% (Disciplined)
    - **Matchup**: Platoon Delta -0.05, OPS vs. North-South Archetype .812
- **Home Lineup**:
    - **Trend (L7)**: 95 wRC+ | **Discipline**: Whiff% 31.2% (High), Chase Rate 31% (Aggressive)
    - **Matchup**: Platoon Delta +0.08, OPS vs. North-South Archetype .745

## 4. Environmental & Operational Modifiers
- **Park Factors**: 115 (Coors) | ADI (Air Density Index): 68.5 (High Carry)
- **Atmospheric Physics**: 71°F, Wind 5mph E (Cross-In), 11% Humidity
- **The Human Element**:
    - Umpire: Chad Whitson | 2026 UCS% (K-Zone Factor): 1.02 (Slight Pitcher Edge)
    - Catcher Framing: Drake Baldwin (Tier 2) / Hunter Goodman (Tier 4)
- **Logistics**:
    - Travel Fatigue: Low (ATL already in altitude series) | Circadian Modifier: Neutral (8:10 PM ET)
    - Manager "Hook" Logic: Snitker (Conservative/Traditional), Black (Aggressive with Youth)

---
**Verdict**: GO for Simulation.
**Final Chaos Engine Inputs**: 
- Sale ERA: 2.31, K/9: 10.53, Stuff+: 115
- Dollander ERA: 3.42, K/9: 11.40, Stuff+: 122
- Env Factor: 1.25 (Coors + ADI adjustment)
- Umpire: 1.02
- Catcher Mods: Baldwin (1.05), Goodman (0.85)
