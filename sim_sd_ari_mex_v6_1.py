import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_1 import run_v6_1_protocol

# SD Expected Lineup
SD_LINEUP = [
    ('R. Laureano', 'R'), 
    ('F. Tatis', 'R'), 
    ('J. Merrill', 'L'), 
    ('M. Machado', 'R'), 
    ('X. Bogaerts', 'R'), 
    ('Gavin Sheets', 'L'), 
    ('M. Andujar', 'R'), 
    ('F. Fermin', 'R'), 
    ('J. Cronenworth', 'L')
]

# ARI Expected Lineup
ARI_LINEUP = [
    ('G. Perdomo', 'S'), 
    ('Ketel Marte', 'S'), 
    ('C. Carroll', 'L'), 
    ('L. Gurriel', 'R'), 
    ('A. Del Castillo', 'L'), 
    ('J. Fernandez', 'R'), 
    ('N. Arenado', 'R'), 
    ('I. Vargas', 'S'), 
    ('Alek Thomas', 'L')
]

if __name__ == '__main__':
    run_v6_1_protocol(
        away_team='SDP',
        home_team='ARI',
        away_sp_name='German Marquez',
        home_sp_name='Zac Gallen',
        away_sp_hand='R',
        home_sp_hand='R',
        away_era=3.86,
        home_era=3.51,
        away_lineup=SD_LINEUP,
        home_lineup=ARI_LINEUP,
        park_factor=130, # Mexico City Series (Harp Helu Stadium)
        is_dome=False,
        temp_f=86,
        wind_mph=5,
        wind_ang=90, # Neutral wind
        humidity=40,
        altitude=7350, # Mexico City
        rain_intensity=0.0
    )
