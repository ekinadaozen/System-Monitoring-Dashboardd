"""
collector.py - System Metrics Collector

Uses psutil to gather real-time system metrics
from the local machine.
"""

import os
import psutil
from datetime import datetime


def collect_metrics():
    """
    Collect current system metrics.

    Returns:
        dict: A dictionary containing:
            - timestamp: Current UTC time
            - cpu_usage: CPU usage percentage (0-100)
            - ram_usage: RAM usage percentage (0-100)
            - disk_usage: Disk usage percentage (0-100)
            - network_sent: Total bytes sent since boot
            - network_received: Total bytes received since boot
    """
    # CPU usage averaged over a 1-second interval
    cpu = psutil.cpu_percent(interval=1)

    # RAM usage
    memory = psutil.virtual_memory()
    ram = memory.percent

    # Disk usage (root partition — works on both Windows and Linux)
    disk_path = "C:\\" if os.name == "nt" else "/"
    disk = psutil.disk_usage(disk_path).percent

    # Network I/O counters (cumulative since boot)
    net = psutil.net_io_counters()
    net_sent = net.bytes_sent
    net_recv = net.bytes_recv

    metrics = {
        "timestamp": datetime.utcnow(),
        "cpu_usage": cpu,
        "ram_usage": ram,
        "disk_usage": disk,
        "network_sent": net_sent,
        "network_received": net_recv,
    }

    return metrics
