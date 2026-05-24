-- ============================================
-- System Metrics Database Initialization
-- ============================================

-- Create the main metrics table
CREATE TABLE IF NOT EXISTS system_metrics (
    id              SERIAL PRIMARY KEY,
    timestamp       TIMESTAMP NOT NULL DEFAULT NOW(),
    cpu_usage       REAL NOT NULL,       -- CPU usage percentage (0-100)
    ram_usage       REAL NOT NULL,       -- RAM usage percentage (0-100)
    disk_usage      REAL NOT NULL,       -- Disk usage percentage (0-100)
    network_sent    BIGINT NOT NULL,     -- Cumulative bytes sent
    network_received BIGINT NOT NULL     -- Cumulative bytes received
);

-- Index on timestamp for faster time-based queries
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp
    ON system_metrics (timestamp DESC);
