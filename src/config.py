"""
config.py - Application Configuration

Loads settings from environment variables (.env file).
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ── Database Configuration ──
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "system_metrics_db")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")

# ── Collection Configuration ──
COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", "5"))
