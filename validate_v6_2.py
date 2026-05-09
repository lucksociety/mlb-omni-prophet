import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quant_elite_v6_2 import run_v6_2_protocol

# SEA @ STL re-test
sea_lineup = [('JP Crawford', 'L'), ('Julio Rodriguez', 'R'), ('Cal Raleigh', 'S'), ('Mitch Garver', 'R'), ('Ty France', 'R'), ('Jorge Polanco', 'S'), ('Mitch Haniger', 'R'), ('Dominic Canzone', 'L'), ('Josh Rojas', 'L')]
stl_lineup = [('Brendan Donovan', 'L'), ('Paul Goldschmidt', 'R'), ('Nolan Arenado', 'R'), ('Willson Contreras', 'R'), ('Lars Nootbaar', 'L'), ('Jordan Walker', 'R'), ('Nolan Gorman', 'L'), ('Masyn Winn', 'R'), ('Victor Scott', 'L')]

print("RE-TESTING SEA @ STL (Actual 20 Runs):")
run_v6_2_protocol('SEA', 'STL', 'Bryan Woo', 'Matthew Liberatore', 'R', 'L',
                  4.59, 2.82, sea_lineup, stl_lineup, 101, False, 75, 5, 90, 50, 465, 0.0)

print("\n" + "="*80 + "\n")

# CHC @ LAD re-test
chc_lineup = [('Nico Hoerner', 'R'), ('M. Busch', 'L'), ('Alex Bregman', 'R'), ('Ian Happ', 'S'), ('Seiya Suzuki', 'R'), ('M. Ballesteros', 'L'), ('Carson Kelly', 'R'), ('P. Crow-Armstrong', 'L'), ('D. Swanson', 'R')]
lad_lineup = [('S. Ohtani', 'L'), ('F. Freeman', 'L'), ('Will Smith', 'R'), ('Kyle Tucker', 'L'), ('Max Muncy', 'L'), ('T. Hernandez', 'R'), ('Andy Pages', 'R'), ('Hyeseong Kim', 'L'), ('A. Freeland', 'S')]

print("RE-TESTING CHC @ LAD (Actual 16 Runs):")
run_v6_2_protocol('CHC', 'LAD', 'Colin Rea', 'Roki Sasaki', 'R', 'R',
                  3.00, 6.11, chc_lineup, lad_lineup, 102, False, 65, 6, 180, 60, 267, 0.1)
