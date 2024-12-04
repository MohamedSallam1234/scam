# script/utils.py

import threading
import time
import logging
import numpy as np

def inject_noise(duration):
    logging.info("Mitigation action performed: Injecting noise.")
    cpu_thread = threading.Thread(target=generate_cpu_noise, args=(duration,))
    memory_thread = threading.Thread(target=generate_memory_noise, args=(duration,))
    cpu_thread.start()
    memory_thread.start()

def generate_cpu_noise(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        x = 0
        for i in range(100000):
            x += i * i

def generate_memory_noise(duration):
    end_time = time.time() + duration
    data = np.random.rand(1000000)
    while time.time() < end_time:
        data *= np.random.rand(1000000)
