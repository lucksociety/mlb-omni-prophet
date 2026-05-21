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

import os

from record_results import update_predictions_csv, update_k_tracker, update_audit_json, calc_pnl

def fix_and_finalize():
    date_str = '2026-05-10'
    
    # 1. Fix Game Results
    # Correct Row for COL@PHI is 206 (Line 207)
    update_predictions_csv(206, 0, 6)
    # Reset Row 207 (which was LAA@TOR) to empty results
    update_predictions_csv(207, '', '') # This might need manual fix if headers differ
    
    # 2. Fix K-Props
    # Correct Row for Sugano is 464 (Line 465)
    update_k_tracker(464, 2, 'Over 3.5', 115, 'Loss', -1.0)
    # Correct Row for Sanchez is 465 (Line 466)
    update_k_tracker(465, 7, 'Under 7.5', -125, 'Win', 0.8)
    # Reset Row 466 (which was Jose Soriano)
    update_k_tracker(466, 'TBD', 'TBD', '', 'N/A', 0.0)

    # Audits are usually safe because they use team names to find files
    update_audit_json('COL', 'PHI', date_str, 0, 6)
    update_audit_json('COL', 'PHI', date_str, sp_name='Tomoyuki Sugano', sp_k=2)
    update_audit_json('COL', 'PHI', date_str, sp_name='Cristopher Sanchez', sp_k=7)

    print("Correction complete.")

if __name__ == '__main__':
    fix_and_finalize()