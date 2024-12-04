# scripts/__init__.py

# Import modules to simplify imports elsewhere
from .process_lifecycle_service import monitor_processes
from .process_monitor_service import monitor_processes
from .sca_detection_service import detect_attacks
from .utils import inject_noise
