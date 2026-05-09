from quant_elite_v6_5 import parse_csv, get_pitcher_stats, ARCHETYPES

sections = parse_csv('MLB Stats')
burke = get_pitcher_stats('Sean Burke', 'CHW', sections)
king = get_pitcher_stats('Michael King', 'SDP', sections)

print("Sean Burke Stats:", burke)
print("Michael King Stats:", king)
print("Sean Burke Archetype:", ARCHETYPES.get('Sean Burke', 'Not Found'))
print("Michael King Archetype:", ARCHETYPES.get('Michael King', 'Not Found'))
