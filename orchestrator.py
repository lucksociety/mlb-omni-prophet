import os
import json
import subprocess
import time
from datetime import datetime
import sys

CONFIG_FILE = "schedule_config.json"
LOG_DIR = "logs"

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open(os.path.join(LOG_DIR, "orchestrator.log"), "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def run_task(task):
    script_path = task.get("script")
    name = task.get("name", script_path)
    args = task.get("args", [])
    
    if not os.path.exists(script_path):
        log_message(f"ERROR: Script not found: {script_path}")
        return

    log_message(f"STARTING TASK: {name}")
    
    log_file_path = os.path.join(LOG_DIR, f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    try:
        with open(log_file_path, "w") as log_file:
            process = subprocess.Popen(
                [sys.executable, script_path] + args,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True
            )
            # We can wait or run in background. For orchestrator, we might wait to prevent overlaps if desired.
            # Here we wait for simplicity.
            process.wait()
            
        if process.returncode == 0:
            log_message(f"SUCCESS: {name} completed.")
        else:
            log_message(f"FAILURE: {name} exited with code {process.returncode}. Check {log_file_path}")
            
    except Exception as e:
        log_message(f"EXCEPTION: Failed to run {name}: {str(e)}")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return []
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        log_message(f"ERROR: Failed to load config: {str(e)}")
        return []

def main():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        
    log_message("Orchestrator started.")
    
    # Track last run times for daily/interval tasks
    last_run = {}

    while True:
        tasks = load_config()
        now = datetime.now()
        
        for task in tasks:
            task_id = task.get("name", task.get("script"))
            schedule_type = task.get("type") # "daily", "interval"
            
            should_run = False
            
            if schedule_type == "daily":
                target_time = task.get("time") # "HH:MM"
                if now.strftime("%H:%M") == target_time:
                    # Check if already run today
                    if last_run.get(task_id, "") != now.strftime("%Y-%m-%d"):
                        should_run = True
                        last_run[task_id] = now.strftime("%Y-%m-%d")
            
            elif schedule_type == "interval":
                minutes = task.get("minutes", 60)
                last_time = last_run.get(task_id, 0)
                if time.time() - last_time > (minutes * 60):
                    should_run = True
                    last_run[task_id] = time.time()
            
            if should_run:
                run_task(task)
        
        # Sleep for a bit to avoid high CPU
        time.sleep(30)

if __name__ == "__main__":
    main()
