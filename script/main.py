# main.py
import sys
import os
import threading
from multiprocessing import Process, Pipe
import logging
# Add the scripts directory to sys.path
script_dir = os.path.join(os.path.dirname(__file__), 'script')
sys.path.append(script_dir)

# Import your modules
import process_lifecycle_service
import process_monitor_service
import sca_detection_service
import utils
def main():
    # Set up logging
    logging.basicConfig(
        filename='../logs/scam.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Create pipes for IPC
    plc_parent_conn, plc_child_conn = Pipe()
    pm_parent_conn, pm_child_conn = Pipe()
    sd_parent_conn, sd_child_conn = Pipe()

    # Load thresholds from config (you may need to parse your config.ini)
    thresholds = {
        'cpu_usage_threshold': 80.0,         # %
        'memory_usage_threshold': 100_000_000,  # Bytes
        'io_read_threshold': 10_000_000,     # Bytes per interval
        'context_switches_threshold': 1000    # Switches per interval
    }
    noise_duration = 5  # Seconds

    # Start services as separate processes
    plc_process = Process(target=process_lifecycle_service.monitor_processes, args=(plc_child_conn, 1))
    pm_process = Process(target=process_monitor_service.monitor_processes, args=(pm_child_conn, 0.1))
    sd_process = Process(target=sca_detection_service.detect_attacks, args=(sd_child_conn, thresholds, noise_duration))

    plc_process.start()
    pm_process.start()
    sd_process.start()

    # Relay messages between services
    def relay_messages():
        while True:
            # From PLC to PM
            if plc_parent_conn.poll():
                msg = plc_parent_conn.recv()
                pm_parent_conn.send(msg)
            # From PM to SD
            if pm_parent_conn.poll():
                data = pm_parent_conn.recv()
                sd_parent_conn.send(data)

    relay_thread = threading.Thread(target=relay_messages)
    relay_thread.start()

    # Wait for processes to finish (optional, or implement graceful shutdown)
    plc_process.join()
    pm_process.join()
    sd_process.join()

if __name__ == "__main__":
    main()
