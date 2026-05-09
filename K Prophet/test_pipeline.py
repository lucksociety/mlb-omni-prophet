from k_pipeline import KProphetMaster

def test_pipeline():
    master = KProphetMaster()

    print("--- TEST 1: The Stable Veteran (High Predictability) ---")
    pitcher_stable = {
        'PitchCounts': [95, 98, 92, 96, 94], # Extremely stable leash
        'ShortLeash': False,
        'InjuryFlag': 0.0,
        'BB_pct': 6.5,
        'Zone_pct': 52.0,
        'SwStr': 12.0,
        'CSW': 28.5,
        'K_pct': 24.5,
        'PitchMix': {'FF': 0.45, 'SL': 0.35, 'CH': 0.20},
        'TTT_Penalty': 0.88 # good at navigating order multiple times
    }
    env_stable = {
        'Weather': {'temp': 65, 'dome': False, 'RainDelayRisk': 0.0},
        'Umpire': {'CS_pct': 17.5, 'Unknown': False}, # generous ump
        'Catcher': {'Framing': 55.0} # good framer
    }
    manager = {'Conservatism': 0.1}
    
    # Mocking lineup with some weaknesses to sliders (0.35)
    lineup_stable = [
        {'O_Swing': 32.0, 'K_Weakness': {'SL': 0.35, 'FF': 0.20, 'CH': 0.15}}
        for _ in range(9)
    ]

    res1 = master.execute_pipeline(pitcher_stable, lineup_stable, env_stable, manager)
    print(f"Status: {res1['status']}")
    if res1['status'] == 'PREDICTED':
        print(f"Exact K Prediction: {res1['exact_k']} (Confidence: {res1['confidence']*100:.2f}%)")
        print(f"Predictability Score: {res1['predictability_score']:.1f}")
        print("Telemetry:", res1['telemetry'])
    else:
        print(f"Reason: {res1['reason']}")


    print("\n--- TEST 2: The Wild Flamethrower on Injury Return (High Volatility) ---")
    pitcher_wild = {
        'PitchCounts': [60, 45, 70], # building up
        'ShortLeash': True,
        'InjuryFlag': 1.0,
        'BB_pct': 14.5, # Walk heavy
        'Zone_pct': 42.0,
        'SwStr': 16.0,
        'CSW': 30.0,
        'PitchMix': {'FF': 0.70, 'CU': 0.30},
    }
    env_wild = {
        'Weather': {'temp': 80, 'RainDelayRisk': 0.5},
        'Umpire': {'Unknown': True}
    }
    
    res2 = master.execute_pipeline(pitcher_wild, [], env_wild, manager)
    print(f"Status: {res2['status']}")
    if res2['status'] == 'REJECTED':
        print(f"Reason: {res2['reason']} (Score: {res2['predictability_score']:.1f})")
    else:
        print("Wait, this should have been rejected!")

if __name__ == "__main__":
    test_pipeline()
