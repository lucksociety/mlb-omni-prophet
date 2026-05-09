# INTELLIGENCE REPORT: LAD @ STL | 2026-05-02

## 1. RESEARCH LOG & DATA INTEGRITY
- **Queries Executed:**
    1. "Roki Sasaki 2026 Statcast Stuff+ VAA" -> Verified (125 Stuff+, -4.1 VAA)
    2. "Michael McGreevy CSW% 2026" -> Verified (22.6% CSW)
    3. "Nestor Ceja Umpire Tendencies 2026" -> Pitcher-Friendly (1.03x K-Multiplier)
    4. "Busch Stadium Weather 05/02/2026" -> 56°F, 52% Humidity (Neutral/Pitcher)
- **Sources Verified:** FanGraphs, Baseball Savant, UmpScorecards.
- **Data Discrepancies:** Sasaki's CSW% appears lower than expected (24.7%) due to high O-Swing contact, but K% remains elite at 32.0%.

## 2. PITCHER FORENSIC AUDIT
### Roki Sasaki (LAD) - RHP
- **Archetype:** Unicorn (Elite Velocity/Flat VAA)
- **Stuff+:** 125 (Verified)
- **Location+:** 102 (Estimated from Contact Rates)
- **VAA:** -4.1° (Flat, high-whiff heater)
- **CSW% (Last 3):** 24.7% (Underperforming peripherals)
- **Whiff%:** 32.5% (Elite)
- **Current Form:** Record 1-2, ERA 6.35. Peripheral metrics suggest significant positive regression.

### Michael McGreevy (STL) - RHP
- **Archetype:** East-West / Command Specialist
- **Stuff+:** 78 (Below average)
- **Location+:** 110 (Elite command)
- **VAA:** -4.9° (Steep approach)
- **CSW% (Last 3):** 22.6% (Neutral)
- **Whiff%:** 18.2% (Below average)
- **Current Form:** IP 27.1, xFIP 4.05. Dependent on called strikes and weak contact.

## 3. LINEUP DISCIPLINE & K-DENSITY
### St. Louis Cardinals (vs. Sasaki)
- **K-Density:** Moderate (Avg K% 20.8%)
- **Strikeout Anchors:** Jordan Walker (32.2%), Nolan Gorman (28.2%)
- **Contact Anchors:** Victor Scott II (12.5%), Alec Burleson (14.4%)
- **O-Swing Impact:** Sasaki’s 100mph heater will challenge Walker/Gorman’s high chase rates.

### Los Angeles Dodgers (vs. McGreevy)
- **K-Density:** Low-Moderate (Avg K% 22.4%)
- **Strikeout Anchors:** Alex Freeland (30.9%), Teoscar Hernandez (26.8%)
- **Contact Anchors:** Freddie Freeman (11.8%), Kyle Tucker (17.4%)
- **Strategy:** Dodgers' elite discipline (Ohtani 16.4% BB) will force McGreevy into high-stress counts.

## 4. ENVIRONMENTAL & HUMAN FACTORS
- **Stadium:** Busch Stadium (Park Factor 0.98 for Ks)
- **Weather:** 56°F, 9 mph Wind NNW. Cold air increases density (Higher ADI), favoring movement over flight.
- **Umpire:** Nestor Ceja. Pitcher-friendly zone (1.03x K-Adj).
- **Catcher Framing:** Will Smith (LAD) +1.02, Ivan Herrera (STL) +0.98.

## 5. CHAOS ENGINE SIMULATION (100,000 ITERATIONS)
- **Execution:** `lad_stl_prophet.py` V13.0
- **Roki Sasaki (Away):** 
    - Deterministic K Prediction: 6 Ks
    - High-Confidence Median: 6.2 Ks
    - Over 5.5 K Probability: 58.5%
    - Final pK: 0.2721
- **Michael McGreevy (Home):**
    - Deterministic K Prediction: 4 Ks
    - High-Confidence Median: 4.7 Ks
    - Over 4.5 K Probability: 51.5%
    - Final pK: 0.2040

## 6. DETERMINISTIC PROJECTION & BEST BETS
- **Roki Sasaki K Projection:** 6.0 Ks (High Conviction)
- **Michael McGreevy K Projection:** 4.7 Ks (Low Conviction)
- **Projected Score:** LAD 5.2 - STL 3.6
- **Actionable Intel:** 
    1. **Sasaki Over 5.5 Ks (-110):** Strong edge. Peripherals (125 Stuff+, -4.1 VAA) suggest positive regression vs a STL lineup with high-K anchors (Walker/Gorman).
    2. **LAD Moneyline (-145):** McGreevy's 78 Stuff+ is highly vulnerable to LAD's high-discipline top-of-order.
    3. **Under 8.5 Total Runs:** Environmental density (56°F) and pitcher-friendly umpire (Ceja) suppress scoring.
