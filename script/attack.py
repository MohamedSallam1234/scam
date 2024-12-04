# scripts/attack.py

import numpy as np
import time
import threading

def memory_intensive_task():
    # Create a large array (e.g., 100 million elements)
    size = 100_000_000
    data = np.arange(size)

    # Access elements in a pattern that causes cache misses
    # For example, access elements with large strides
    stride = 1024  # Adjust stride to control cache behavior
    sum = 0
    for i in range(0, size, stride):
        sum += data[i]

    print(f"Sum: {sum}")

def cpu_intensive_task():
    # Perform a CPU-bound computation
    total = 0
    for i in range(1, 10_000_000):
        total += i ** 0.5

    print(f"Total: {total}")

def branch_misprediction_task():
    # Simulate branch mispredictions
    import random
    count = 0
    for _ in range(1_000_000):
        x = random.randint(0, 100)
        if x < 50:
            count += 1
        else:
            count -= 1

    print(f"Count: {count}")

def run_attack():
    # Run tasks in parallel to increase resource usage
    threads = []
    tasks = [memory_intensive_task, cpu_intensive_task, branch_misprediction_task]
    for task in tasks:
        thread = threading.Thread(target=task)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    while True:
        run_attack()
        # Sleep briefly before repeating
        time.sleep(1)
