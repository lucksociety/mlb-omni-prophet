#!/usr/bin/env python3
import os
import sys
import datetime

TEMPLATE_PATH = "deep_research_report_template.md"

def create_report(away, home, date=None):
    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    filename = f"matchup_research_{away}_{home}_{date}.md"
    if os.path.exists(filename):
        print(f"Report already exists: {filename}")
        return filename
    
    with open(TEMPLATE_PATH, "r") as f:
        template = f.read()
    
    report = template.replace("[AWAY]", away)
    report = report.replace("[HOME]", home)
    report = report.replace("[DATE]", date)
    
    with open(filename, "w") as f:
        f.write(report)
    
    print(f"Created research report: {filename}")
    return filename

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 research_assistant.py <AWAY> <HOME>")
        sys.exit(1)
    
    create_report(sys.argv[1].upper(), sys.argv[2].upper())
