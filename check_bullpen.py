from quant_elite_v6_2 import parse_csv, get_bullpen_tiers

sections = parse_csv('/Users/danielreiss/Desktop/Antigravity/MLB/MLB Stats')
teams = ['CLE', 'PIT', 'LAA', 'LAD']

print("--- Bullpen Tiers Diagnostic ---")
for team in teams:
    tiers = get_bullpen_tiers(team, "NONE", sections)
    print(f"Team: {team}")
    print(f"  Tier A: {tiers['A']:.2f}")
    print(f"  Tier B: {tiers['B']:.2f}")
    print(f"  Tier C: {tiers['C']:.2f}")
