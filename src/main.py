"""
main.py - Application Entry Point

Collects system metrics at a regular interval
and stores them in PostgreSQL.
"""

import schedule
import time
import logging
from src.collector import collect_metrics
from src.database import insert_metrics
from src.config import COLLECTION_INTERVAL

# ── Logging Setup ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def job():
    """Collect metrics and insert them into the database."""
    try:
        metrics = collect_metrics()
        insert_metrics(metrics)
        logger.info(
            "CPU: %.1f%%  |  RAM: %.1f%%  |  Disk: %.1f%%  |  Net Sent: %s  |  Net Recv: %s",
            metrics["cpu_usage"],
            metrics["ram_usage"],
            metrics["disk_usage"],
            format_bytes(metrics["network_sent"]),
            format_bytes(metrics["network_received"]),
        )
    except Exception as e:
        logger.error("Failed to collect/store metrics: %s", e)


def format_bytes(num_bytes):
    """Convert bytes to a human-readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def main():
    """Start the metrics collection loop."""
    logger.info("=" * 50)
    logger.info("System Monitoring Collector Started")
    logger.info("Collection interval: %d seconds", COLLECTION_INTERVAL)
    logger.info("=" * 50)

    # Run once immediately, then schedule
    job()
    schedule.every(COLLECTION_INTERVAL).seconds.do(job)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Collector stopped by user.")


if __name__ == "__main__":
    main()
