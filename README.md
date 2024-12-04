#  SCAM Project

## Overview
The **Side-Channel Attack Monitoring (SCAM)** project is designed to detect and mitigate Spectre-like side-channel attacks in real-time. It leverages accessible software-based metrics and threshold-based analysis to identify suspicious activity in virtualized environments such as **Windows Subsystem for Linux (WSL2)**, where hardware-level performance counters are unavailable.

SCAM is a simplified yet effective approach to mitigating threats using noise injection techniques to disrupt potential attackers. This tool can be integrated into cloud environments to enhance security, making it ideal for virtualized systems and environments without access to specialized hardware.

## Features
- **Real-time Process Monitoring**: Monitor active processes to collect software-based performance metrics.
- **Threshold-Based Anomaly Detection**: Utilize thresholds based on baseline metrics to detect abnormal activities indicative of side-channel attacks.
- **Noise Injection Mechanism**: Disrupt the precision of potential side-channel attacks by generating noise in CPU processes.
- **Designed for WSL2 Environment**: Suitable for environments where access to hardware-level monitoring is restricted.

## Project Structure
The project is organized as follows:

```
SCAM/
│
├── main.py
│   - The main entry point of the SCAM system that integrates all components.
│
├── services/
│   ├── process_lifecycle_service.py
│   │   - Tracks the lifecycle of processes (creation and termination).
│   │
│   ├── process_monitor_service.py
│   │   - Monitors performance metrics of processes.
│   │
│   ├── sca_detection_service.py
│   │   - Detects potential side-channel attacks based on the collected metrics.
│   │
│   └── noise_injection.py
│       - Injects noise into system processes to mitigate ongoing attacks.
│
├── utils/
│   └── logger.py
│       - Utility functions for logging.
│
├── logs/
│   └── scam.log
│       - Logs file containing records of process monitoring, detection, and mitigation activities.
│
├── requirements.txt
│   - Dependencies required to run the SCAM project.
│
└── README.md
    - This documentation file.
```

## Prerequisites
- **Python 3.8** or higher
- **psutil library**: A Python cross-platform library for process and system monitoring.
- **pip**: Python package manager.

To install the required dependencies, run:
```sh
pip install -r requirements.txt
```

## Installation
### Clone the Repository
```sh
git clone https://github.com/yourusername/scam.git
cd scam
```

### Set Up Virtual Environment (Optional but Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## How to Run the Project
### Run the Main SCAM System
```sh
python main.py
```
The `main.py` script integrates all components and initiates the monitoring, detection, and mitigation processes.

## Components
1. **process_lifecycle_service.py**
   - Tracks the creation and termination of system processes to ensure that all new processes are included in the monitoring system.

2. **process_monitor_service.py**
   - Collects performance metrics such as **CPU usage**, **memory usage**, and **I/O activity** from running processes using the `psutil` library.

3. **sca_detection_service.py**
   - Analyzes the collected metrics against predefined thresholds to detect anomalies that may indicate side-channel attacks.

4. **noise_injection.py**
   - Implements a noise injection mechanism to obfuscate the information being gathered by an attacker by creating random computational tasks.

## Logging
The SCAM system uses a centralized logging mechanism to keep track of key events:
- **New Process Detection**
- **Anomalous Behavior Detected**
- **Mitigation Action Triggered**

Logs are saved in the `logs/scam.log` file. You can monitor this file to observe the operation of the SCAM system and any detected anomalies.

## Testing
- **Process Detection Testing**: Start new processes (e.g., `python script.py`) and verify that they are detected by the SCAM system.
- **Attack Simulation**: Run a CPU-intensive or memory-intensive script to simulate an attack and observe if SCAM detects abnormal behavior and triggers mitigation.
- **Noise Injection Verification**: Ensure that the noise injection mechanism runs upon attack detection without impacting system stability.

## Configuration
- **Thresholds for Detection**: The thresholds for CPU, memory, and I/O are configured within `sca_detection_service.py`. You can tune these thresholds based on the system's baseline performance.

## Future Enhancements
- **Machine Learning-Based Detection**: Replace the threshold-based approach with an ML-based model for more accurate detection.
- **Integration with Cloud Platforms**: Extend SCAM's applicability to cloud environments, such as **OpenStack** integration.
- **Cross-VM Detection**: Implement cross-VM detection mechanisms to identify attacks occurring across virtual machines in shared environments.

## Conclusion
The **Simplified SCAM** project provides an accessible way to detect and mitigate side-channel attacks in constrained environments such as WSL2. By focusing on easily accessible metrics and utilizing noise injection, SCAM offers a practical solution for systems that lack specialized hardware monitoring capabilities.

Feel free to contribute, test, or suggest improvements!

## License
This project is licensed under the **MIT License**.

## Contact
For questions or contributions, please contact:

- **Author**: Mohamed Ibrahim
- **Email**: muhammed.ibraim.sallam@gmail.com
