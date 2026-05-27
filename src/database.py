"""
database.py - PostgreSQL Database Operations

Handles connection and data insertion for system metrics.
"""

import psycopg2
try:
    from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
except ModuleNotFoundError:
    from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    """
    Create and return a new database connection.

    Returns:
        psycopg2.connection: A PostgreSQL database connection.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    return conn


def insert_metrics(metrics):
    """
    Insert a single metrics record into the database.

    Args:
        metrics (dict): Dictionary with keys:
            timestamp, cpu_usage, ram_usage, disk_usage,
            network_sent, network_received
    """
    query = """
        INSERT INTO system_metrics
            (timestamp, cpu_usage, ram_usage, disk_usage, network_sent, network_received)
        VALUES
            (%(timestamp)s, %(cpu_usage)s, %(ram_usage)s, %(disk_usage)s,
             %(network_sent)s, %(network_received)s);
    """

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, metrics)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
