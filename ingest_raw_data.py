import os

def ingest_tsv(input_filename, section_name):
    if not os.path.exists(input_filename):
        print(f"File not found: {input_filename}. Skipping {section_name} update.")
        return

    print(f"Reading {input_filename}...")
    lines = []
    with open(input_filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = [p.strip() for p in line.split('\t')]
            # If the row has enough columns, consider it valid
            if len(parts) > 5 and any(parts):
                lines.append(','.join(parts))
                
    if not lines:
        print(f"No data found in {input_filename}.")
        return

    # Ensure the first header starts with '#' so parse_multi_csv recognizes it
    if not lines[0].startswith('#'):
        lines[0] = '#' + lines[0]

    with open('/Users/danielreiss/Desktop/Antigravity/MLB/MLB Stats', 'a', encoding='utf-8') as f:
        f.write(f'\n{section_name},,,,,,,,,,,,,,,,,,,,,\n')
        for line in lines:
            f.write(line + '\n')
            
    print(f"SUCCESS: {section_name} appended to MLB Stats.")
    print(f"You can now safely delete {input_filename} to keep your folder clean.")

def main():
    print("Starting Raw Text Ingestion...")
    import datetime
    with open('/Users/danielreiss/Desktop/Antigravity/MLB/MLB Stats', 'a', encoding='utf-8') as f:
        f.write(f'\n# LAST_UPDATED: {datetime.date.today().isoformat()}\n')
    
    # These are the default filenames you should use when pasting your tables
    ingest_tsv('raw_batters.txt', 'Batting Advanced')
    ingest_tsv('raw_pitchers.txt', 'Pitching Advanced')
    print("Update complete!")

if __name__ == '__main__':
    main()
