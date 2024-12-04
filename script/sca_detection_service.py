# script/sca_detection_service.py

import json
import logging
from multiprocessing import Pipe
import threading
from utils import inject_noise

def detect_attacks(pipe_conn, thresholds, noise_duration):
    process_data = {}

    while True:
        try:
            if pipe_conn.poll():
                data_json = pipe_conn.recv()
                data = json.loads(data_json)
                pid = data['pid']

                # Update process data
                if pid not in process_data:
                    process_data[pid] = {}
                process_data[pid]['previous'] = process_data[pid].get('current', {})
                process_data[pid]['current'] = data

                # Calculate differences for certain metrics
                if 'previous' in process_data[pid]:
                    prev = process_data[pid]['previous']
                    curr = process_data[pid]['current']

                    io_read_diff = curr['io_read_bytes'] - prev.get('io_read_bytes', 0)
                    ctx_switches_diff = (
                        curr['ctx_switch_voluntary'] - prev.get('ctx_switch_voluntary', 0) +
                        curr['ctx_switch_involuntary'] - prev.get('ctx_switch_involuntary', 0)
                    )

                    # Detection logic
                    if (
                        curr['cpu_usage'] > thresholds['cpu_usage_threshold'] or
                        curr['memory_rss'] > thresholds['memory_usage_threshold'] or
                        io_read_diff > thresholds['io_read_threshold'] or
                        ctx_switches_diff > thresholds['context_switches_threshold']
                    ):
                        logging.warning(f"Potential side-channel attack detected! PID {pid}. Initiating mitigation.")
                        inject_noise(noise_duration)
                    else:
                        logging.info(f"PID {pid} operating normally.")

        except Exception as e:
            logging.error(f"Error during attack detection: {e}")

if __name__ == "__main__":
    import threading

    logging.basicConfig(
        filename='../logs/scam.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    parent_conn, child_conn = Pipe()

    # Load thresholds from config
    thresholds = {
        'cpu_usage_threshold': 80.0,         # %
        'memory_usage_threshold': 100_000_000,  # Bytes
        'io_read_threshold': 10_000_000,     # Bytes per interval
        'context_switches_threshold': 1000    # Switches per interval
    }
    noise_duration = 5  # Seconds

    detection_thread = threading.Thread(target=detect_attacks, args=(parent_conn, thresholds, noise_duration))
    detection_thread.start()

    # Placeholder: Implement IPC to receive data from process_monitor_service.py
