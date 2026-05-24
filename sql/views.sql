-- ============================================
-- Power BI Ready Views
-- ============================================
-- These views prepare clean datasets suitable
-- for importing into Power BI or any BI tool.

-- View: Hourly averages for trend analysis
CREATE OR REPLACE VIEW hourly_metrics AS
SELECT
    DATE_TRUNC('hour', timestamp)   AS hour,
    ROUND(AVG(cpu_usage)::numeric, 2)   AS avg_cpu,
    ROUND(AVG(ram_usage)::numeric, 2)   AS avg_ram,
    ROUND(AVG(disk_usage)::numeric, 2)  AS avg_disk,
    MAX(network_sent)               AS max_network_sent,
    MAX(network_received)           AS max_network_received,
    COUNT(*)                        AS sample_count
FROM system_metrics
GROUP BY DATE_TRUNC('hour', timestamp)
ORDER BY hour DESC;

-- View: Daily summary for executive reporting
CREATE OR REPLACE VIEW daily_summary AS
SELECT
    DATE(timestamp)                     AS date,
    ROUND(AVG(cpu_usage)::numeric, 2)   AS avg_cpu,
    ROUND(MAX(cpu_usage)::numeric, 2)   AS peak_cpu,
    ROUND(AVG(ram_usage)::numeric, 2)   AS avg_ram,
    ROUND(MAX(ram_usage)::numeric, 2)   AS peak_ram,
    ROUND(AVG(disk_usage)::numeric, 2)  AS avg_disk,
    COUNT(*)                            AS total_samples
FROM system_metrics
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- View: Latest snapshot (most recent reading)
CREATE OR REPLACE VIEW latest_metrics AS
SELECT *
FROM system_metrics
ORDER BY timestamp DESC
LIMIT 1;
