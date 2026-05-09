import csv
import os

class DataLoader:
    def __init__(self, stats_path):
        self.stats_path = stats_path
        self.sections = {}
        self.load_data()

    def load_data(self):
        current_section = None
        headers = []
        if not os.path.exists(self.stats_path):
            print(f"Error: {self.stats_path} not found.")
            return

        with open(self.stats_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or not any(row):
                    continue
                
                first_val = row[0].strip()
                if first_val in ["Batting Advanced", "Batting Stat Cast", "Pitching Advanced", 
                                "Pitching +", "Pitching Statcast", "Batting Splits LHP", "Batting Splits RHP"]:
                    current_section = first_val
                    self.sections[current_section] = []
                    headers = []
                    continue
                
                if current_section:
                    if first_val == '#' and not headers:
                        # Clean up headers - take the first word before any space
                        headers = [h.split()[0].strip() if h.strip() else f"col_{i}" for i, h in enumerate(row)]
                        continue
                    
                    if headers and first_val != '#' and len(row) >= len(headers):
                        row_dict = dict(zip(headers, row[:len(headers)]))
                        self.sections[current_section].append(row_dict)

    def get_section(self, section_name):
        return self.sections.get(section_name, [])

    def fuzzy_find_player(self, name, players):
        if not players or not name or not name.strip():
            return None
        name_l = name.lower()
        parts = name_l.split()
        if not parts: return None
        last_name = parts[-1]
        
        # Try exact match first
        for p in players:
            if p.get('Name', '').lower() == name_l:
                return p
        
        # Try last name match
        for p in players:
            pn = p.get('Name', '').lower()
            if last_name in pn:
                return p
        
        return None

if __name__ == "__main__":
    loader = DataLoader("/Users/danielreiss/Desktop/Antigravity/HR/MLB Stats")
    print(f"Loaded sections: {list(loader.sections.keys())}")
    adv = loader.get_section("Batting Advanced")
    if adv:
        print(f"Sample player: {adv[0]['Name']} - ISO: {adv[0].get('ISO')}")
