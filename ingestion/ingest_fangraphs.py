import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)
import csv
import os

def ingest_csv(input_filename, section_name):
    if not os.path.exists(input_filename):
        print(f"File not found: {input_filename}. Skipping {section_name} update.")
        return

    print(f"Reading {input_filename}...")
    with open(input_filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        data = list(reader)
        
    if not data:
        print(f"No data found in {input_filename}.")
        return

    headers = data[0]
    
    # Ensure the first column has '#' to match the internal parsing structure of your scripts
    if headers[0] != '#':
        headers.insert(0, '#')
        for i in range(1, len(data)):
            data[i].insert(0, str(i))

    with open('/Users/danielreiss/Desktop/Antigravity/MLB/data/MLB Stats', 'a', encoding='utf-8') as f:
        f.write(f'\n{section_name},,,,,,,,,,,,,,,,,,,,,\n')
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data[1:]:
            writer.writerow(row)
            
    print(f"SUCCESS: {section_name} appended to MLB Stats.")
    print(f"You can now safely delete {input_filename} to keep your folder clean.")

def main():
    print("Starting FanGraphs CSV Ingestion...")
    # These are the default filenames FanGraphs exports. 
    # Just drop them in this folder and run the script.
    ingest_csv('fangraphs_batters.csv', 'Batting Advanced')
    ingest_csv('fangraphs_pitchers.csv', 'Pitching Advanced')
    print("Update complete!")

if __name__ == '__main__':
    main()