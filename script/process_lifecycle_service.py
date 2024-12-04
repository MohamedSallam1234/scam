# script/process_lifecycle_service.py

import psutil
import time
import json
import logging
from multiprocessing import Pipe

def monitor_processes(pipe_conn, monitor_interval):
    """
    Monitors process creation and termination by periodically scanning the list of running processes.
    """
    previous_pids = set(psutil.pids())
    logging.info("Process Lifecycle Service started.")

    while True:
        try:
            current_pids = set(psutil.pids())
            # Detect new processes
            new_pids = current_pids - previous_pids
            for pid in new_pids:
                # Filter out system processes or processes you don't want to monitor
                try:
                    proc = psutil.Process(pid)
                    # Optionally, you can filter by process name, user, etc.
                    process_name = proc.name()
                    logging.info(f"New process detected: PID {pid}, Name: {process_name}")
                    message = json.dumps({'action': 'start', 'pid': pid})
                    pipe_conn.send(message)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue  # Process terminated or access denied before we could inspect it

            # Detect terminated processes
            terminated_pids = previous_pids - current_pids
            for pid in terminated_pids:
                logging.info(f"Process terminated: PID {pid}")
                message = json.dumps({'action': 'stop', 'pid': pid})
                pipe_conn.send(message)

            previous_pids = current_pids
            time.sleep(monitor_interval)
        except Exception as e:
            logging.error(f"Error in process lifecycle monitoring: {e}")
            time.sleep(monitor_interval)

if __name__ == "__main__":
    import threading

    logging.basicConfig(
        filename='../logs/scam.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    parent_conn, child_conn = Pipe()
    monitor_interval = 1  # Adjust the interval as needed (in seconds)

    monitor_thread = threading.Thread(target=monitor_processes, args=(child_conn, monitor_interval))
    monitor_thread.start()

    # Placeholder: Implement IPC to communicate with process_monitor_service.py
    # For example, you could pass parent_conn to another service or use a shared Queue
