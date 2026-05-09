import os
import sys
from record_results import update_predictions_csv, update_k_tracker, update_audit_json, calc_pnl

def finalize():
    date_str = "2026-05-07"
    away_team = "BAL"
    home_team = "MIA"
    away_score = 3
    home_score = 4
    
    # 1. Update Game Projection (Row 132)
    print(f"Updating predictions_history.csv row 132...")
    update_predictions_csv(132, away_score, home_score)
    
    # 2. Update K Props
    # Max Meyer (Row 316) - Under 5.5 @ +105
    print(f"Updating Meyer K's (Row 316)...")
    result_m, pnl_m = calc_pnl("Under 5.5", "105", 5)
    update_k_tracker(316, 5, "Under 5.5", "105", result_m, pnl_m)
    
    # Cade Povich (Row 315) - Under 4.5 @ -105
    print(f"Updating Povich K's (Row 315)...")
    result_p, pnl_p = calc_pnl("Under 4.5", "-105", 1)
    update_k_tracker(315, 1, "Under 4.5", "-105", result_p, pnl_p)
    
    # 3. Update Audit JSON
    print(f"Updating audit JSON...")
    update_audit_json(away_team, home_team, date_str, away_score, home_score, 
                      away_sp_k=1, home_sp_k=5)
    
    print("\n✅ Finalization complete for BAL @ MIA (2026-05-07)")

if __name__ == "__main__":
    finalize()
