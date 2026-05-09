
import sys
import os

# Add the directory to path
sys.path.append('/Users/danielreiss/Desktop/Antigravity/MLB')

from record_results import update_predictions_csv, update_k_tracker, update_audit_json

def finalize_results():
    date_str = '2026-05-04'
    away_team = 'LAD'
    home_team = 'HOU'
    away_score = 8
    home_score = 3
    yamamoto_k = 8
    weiss_k = 5
    
    print("--- RECORDING FINAL RESULTS ---")
    
    # Update predictions_history.csv (Rows 34-40)
    for row in range(34, 41):
        success = update_predictions_csv(row, away_score, home_score)
        if success:
            print(f"  ✅ Updated predictions_history.csv row {row}")
            
    # Update K Prophet/performance_tracker.csv (Rows 131, 132)
    # We should also update the others if we want clean history, but 131/132 are the ones from the final sim.
    update_k_tracker(131, yamamoto_k)
    print(f"  ✅ Updated K-tracker row 131 (Yamamoto: {yamamoto_k})")
    update_k_tracker(132, weiss_k)
    print(f"  ✅ Updated K-tracker row 132 (Weiss: {weiss_k})")
    
    # Update audit JSON files
    update_audit_json(away_team, home_team, date_str, away_score, home_score,
                      away_sp_k=yamamoto_k, home_sp_k=weiss_k)
    
    print("\n--- RESULTS RECORDED SUCCESSFULLY ---")

if __name__ == "__main__":
    finalize_results()
