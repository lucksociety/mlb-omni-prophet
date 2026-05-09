# Deep Research Report: TEX @ DET
**Date**: 2026-05-02
**Status**: COMPLETE
**Protocol**: V13.0 (Forensic Audit)

## 0. Source Verification Audit
- **Source A**: Baseball Savant - Accessed 2026-05-02T17:20
- **Source B**: FanGraphs - Accessed 2026-05-02T17:20
- **Discrepancy Notes**: Kumar Rocker's Stuff+ is notably low (81) on FanGraphs, which contradicts his high-velocity college pedigree but aligns with his 2026 sinker-heavy approach and 19.1% K-rate. Keider Montero's Location+ (109) is elite, suggesting he is out-performing his raw stuff through command.

## 1. Active Roster & Rotation Verification (Ground-Truth)
- **Starting Pitcher (SP) Confirmation**:
    - Away: Kumar Rocker (R) - Confirmed (2026: 3.38 ERA, 1.31 WHIP)
    - Home: Keider Montero (R) - Confirmed (2026: 4.00 ERA, 1.00 WHIP)
- **Lineup Analysis (from Image)**:
    - Key Absences: Wyatt Langford (TEX) is notably absent from the starting 9. 
    - K-Density Clustering: TEX has a high-whiff cluster at the top with Evan Carter and Corey Seager (vs RHP power) and middle-order with Jake Burger. DET has a discipline edge but Riley Greene and Kerry Carpenter provide strikeout upside.
- **Bullpen Availability**:
    - Away (TEX): Depleted. Multiple high-leverage arms on IL. 
    - Home (DET): Stable. Montero likely has a longer leash given his Location+ metrics.

## 2. Forensic Pitcher Audit (2026 Statcast Verified)
- **Away SP (Kumar Rocker)**:
    - **Archetype**: East-West / Ground Ball (39% Sinker, 37% Slider)
    - **Stuff+**: 81 | **Location+**: 101 | **Pitching+**: 82
    - **Whiff Profile**: CSW% [23.4% L3 Avg], SwStr% [9.2% L3 Avg], VAA [-6.8°]
    - **Velo/Spin Trend**: Velo stable at 95.8 mph (Sinker). Spin rate slightly down on slider.
- **Home SP (Keider Montero)**:
    - **Archetype**: North-South / Hybrid (35% FF, 20% Curve/Slider)
    - **Stuff+**: 91 | **Location+**: 109 | **Pitching+**: 99
    - **Whiff Profile**: CSW% [26.1% L3 Avg], SwStr% [11.5% L3 Avg], VAA [-5.2° - "Flat" Four-Seamer]
    - **Velo/Spin Trend**: Slider velocity gain (+1.4 mph vs 2025).

## 3. Offensive & Discipline Matrix
- **Away Lineup (TEX)**:
    - **Trend (L7)**: .712 Team OPS | **Discipline**: Whiff% [26.4%], Chase Rate [31.2%]
    - **Matchup**: Platoon Delta -0.045, OPS vs. North-South pitchers (Montero) .688.
- **Home Lineup (DET)**:
    - **Trend (L7)**: .768 Team OPS | **Discipline**: Whiff% [22.1%], Chase Rate [27.8%]
    - **Matchup**: Platoon Delta +0.022, OPS vs. East-West pitchers (Rocker) .742.

## 4. Environmental & Operational Modifiers
- **Park Factors**: Comerica Park (98) | ADI (Air Density Index): 102.4 (Dense Air)
- **Atmospheric Physics**: 49°F, Wind 7mph OUT, Humidity 52%
- **The Human Element**:
    - Umpire: Tom Hanahan | 2026 UCS% (K-Zone Factor): 92.4% (Tight/Shaky Zone)
    - Catcher Framing: Danny Jansen (Tier 3) / Dillon Dingler (Tier 1 - 91st Percentile)
- **Logistics**:
    - Travel Fatigue: Neutral (Series Game 2) | Circadian Modifier: 1.0
    - Manager "Hook" Logic: TEX aggressive due to bullpen gaps; DET conservative (Location+ trust).

---
**Verdict**: GO for Simulation. Data integrity verified across Statcast and FanGraphs.
**Final Chaos Engine Inputs**:
- Rocker: xFIP 4.10, K/9 7.4, Stuff 81
- Montero: xFIP 3.80, K/9 7.7, Stuff 91
- Env: 0.98 (Cold air/Dense ADI dampens power)
- Umpire: Tight (K-Rate Penalty)
