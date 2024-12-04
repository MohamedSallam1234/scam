# script/process_monitor_service.py

import time
import json
import logging
import psutil
from multiprocessing import Pipe

def monitor_processes(pipe_conn, monitor_interval):
    monitored_pids = set()
    process_metrics = {}

    while True:
        try:
            # Receive new PIDs to monitor or stop monitoring
            if pipe_conn.poll():
                message = json.loads(pipe_conn.recv())
                action = message.get('action')
                pid = int(message.get('pid'))
                if action == 'start':
                    monitored_pids.add(pid)
                    process_metrics[pid] = {'process': psutil.Process(pid)}
                    logging.info(f"Started monitoring PID {pid}")
                elif action == 'stop' and pid in monitored_pids:
                    monitored_pids.remove(pid)
                    process_metrics.pop(pid, None)
                    logging.info(f"Stopped monitoring PID {pid}")

            # Collect metrics for each monitored process
            for pid in list(monitored_pids):
                try:
                    proc = process_metrics[pid]['process']
                    cpu_usage = proc.cpu_percent(interval=None)
                    memory_info = proc.memory_info()
                    io_counters = proc.io_counters()
                    ctx_switches = proc.num_ctx_switches()

                    data = {
                        'timestamp': time.time(),
                        'pid': pid,
                        'cpu_usage': cpu_usage,
                        'memory_rss': memory_info.rss,
                        'io_read_bytes': io_counters.read_bytes,
                        'io_write_bytes': io_counters.write_bytes,
                        'ctx_switch_voluntary': ctx_switches.voluntary,
                        'ctx_switch_involuntary': ctx_switches.involuntary
                    }

                    # Send data to detection service
                    pipe_conn.send(json.dumps(data))

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    monitored_pids.remove(pid)
                    process_metrics.pop(pid, None)
                    logging.info(f"Process PID {pid} terminated or access denied")

            time.sleep(monitor_interval)
        except Exception as e:
            logging.error(f"Error in process monitoring: {e}")
            time.sleep(monitor_interval)

if __name__ == "__main__":
    import threading

    logging.basicConfig(
        filename='../logs/scam.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    parent_conn, child_conn = Pipe()
    monitor_interval = 0.1  # 100 milliseconds

    monitor_thread = threading.Thread(target=monitor_processes, args=(child_conn, monitor_interval))
    monitor_thread.start()

    # Placeholder: Implement IPC to receive PIDs from process_lifecycle_service.py
