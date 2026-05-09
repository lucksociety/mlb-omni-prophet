from quant_elite_v6_2 import run_v6_2_protocol

# RE-TESTING ATH @ TEX (Athletics @ Rangers)
# Actual Result: Athletics won 8-1

ATH_LINEUP = [
    ('Nick Kurtz', 'L'), ('Shea Langeliers', 'R'), ('Carlos Cortes', 'L'),
    ('Tyler Soderstrom', 'L'), ('Jacob Wilson', 'R'), ('Jeff McNeil', 'L'),
    ('Max Muncy', 'R'), ('Lawrence Butler', 'L'), ('Zack Gelof', 'R')
]

TEX_LINEUP = [
    ('Brandon Nimmo', 'L'), ('Joc Pederson', 'L'), ('Corey Seager', 'L'),
    ('Jake Burger', 'R'), ('Josh Jung', 'R'), ('Evan Carter', 'L'),
    ('Kyle Higashioka', 'R'), ('Josh Smith', 'L'), ('Alejandro Osuna', 'L')
]

if __name__ == '__main__':
    run_v6_2_protocol(
        away_team='ATH', home_team='TEX',
        away_sp_name='Luis Severino', home_sp_name='Nathan Eovaldi',
        away_sp_hand='R', home_sp_hand='R',
        away_era=6.20, home_era=5.06,
        away_lineup=ATH_LINEUP, home_lineup=TEX_LINEUP,
        park_factor=98, is_dome=True, temp_f=72, wind_mph=0, wind_ang=0, 
        humidity=45, altitude=600, rain_intensity=0,
        away_fatigue=0.1, home_fatigue=0.6, # Assume Rangers BP was gassed
        underdog_trap=True
    )
