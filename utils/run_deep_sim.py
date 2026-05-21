#!/usr/bin/env python3
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

import datetime

def check_report_status(away, home, date=None):
    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    filename = f"matchup_research_{away}_{home}_{date}.md"
    if not os.path.exists(filename):
        print(f"❌ ERROR: No research report found for {away} @ {home} on {date}.")
        print(f"Run 'python3 research_assistant.py {away} {home}' first.")
        return False
    
    with open(filename, "r") as f:
        content = f.read()
    
    if "**Status**: COMPLETE" not in content:
        print(f"❌ ERROR: Research report for {away} @ {home} is NOT complete.")
        print(f"Please complete all steps in {filename} and set status to COMPLETE.")
        return False
    
    if "**Verdict**: GO" not in content:
        print(f"❌ ERROR: Research report verdict is not GO.")
        return False
    
    print(f"✅ Research verified for {away} @ {home}. Proceeding to simulation...")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 run_deep_sim.py <AWAY> <HOME>")
        sys.exit(1)
    
    away = sys.argv[1].upper()
    home = sys.argv[2].upper()
    
    if check_report_status(away, home):
        # In a real scenario, this would import and run the simulation
        # For now, it just signals that it's okay to proceed.
        print("\n🚀 PROJECTION ENGINE READY.")
        print(f"Please ensure sim_{away.lower()}_{home.lower()}_v6.py is updated with the research data.")
    else:
        sys.exit(1)