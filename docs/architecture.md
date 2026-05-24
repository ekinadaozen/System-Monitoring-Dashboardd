# 🏗️ Architecture

## Overview

The System Monitoring & Analytics Dashboard follows a simple **ETL (Extract, Transform, Load)** pattern to collect, store, and visualize system metrics from the local machine.

---

## Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   EXTRACT   │────▶│  TRANSFORM  │────▶│    LOAD      │
│   psutil    │     │   Python    │     │  PostgreSQL  │
│             │     │   (format)  │     │              │
└─────────────┘     └─────────────┘     └──────┬───────┘
                                               │
                              ┌────────────────┼────────────────┐
                              ▼                                 ▼
                       ┌─────────────┐                  ┌─────────────┐
                       │   Grafana    │                  │  Power BI    │
                       │  (live viz)  │                  │  (reports)   │
                       └─────────────┘                  └─────────────┘
```

---

## Component Responsibilities

### 1. Collector (`src/collector.py`)

- **Purpose**: Extract system metrics using `psutil`
- **Metrics collected**:
  - CPU usage percentage
  - RAM usage percentage
  - Disk usage percentage
  - Network bytes sent (cumulative)
  - Network bytes received (cumulative)
- **Output**: Python dictionary with all metrics + timestamp

### 2. Database Module (`src/database.py`)

- **Purpose**: Handle PostgreSQL connection and data insertion
- **Responsibilities**:
  - Create database connections
  - Insert metric records using parameterized queries
  - Manage connection lifecycle (open, commit, close)

### 3. Configuration (`src/config.py`)

- **Purpose**: Centralize configuration management
- **Source**: Environment variables loaded from `.env` file
- **Settings**: Database credentials, host, port, collection interval

### 4. Main Application (`src/main.py`)

- **Purpose**: Orchestrate the collection loop
- **Behavior**:
  1. Initialize logging
  2. Run an initial collection immediately
  3. Schedule repeated collection every N seconds
  4. Loop until interrupted (Ctrl+C)

### 5. PostgreSQL Database

- **Purpose**: Persistent storage for all metrics
- **Table**: `system_metrics` — stores raw metric readings
- **Views**: Pre-built aggregations for Power BI:
  - `hourly_metrics` — hourly averages
  - `daily_summary` — daily summaries with peak values
  - `latest_metrics` — most recent reading

### 6. Grafana

- **Purpose**: Real-time visualization
- **Panels**:
  - CPU usage over time (time series)
  - RAM usage over time (time series)
  - Disk usage (gauge with color thresholds)
  - Current CPU (gauge)
  - Network activity (time series with sent/received)
- **Refresh rate**: Every 5 seconds

---

## Technology Choices

| Decision               | Choice        | Reasoning                                     |
| ---------------------- | ------------- | --------------------------------------------- |
| Metrics library        | psutil        | Industry standard, cross-platform              |
| Database               | PostgreSQL    | Robust, free, great Grafana/Power BI support   |
| Scheduling             | schedule      | Simple, beginner-friendly, no overhead          |
| Visualization          | Grafana       | Purpose-built for time series dashboards        |
| BI Reporting           | Power BI      | Industry standard for business analytics        |
| Containerization       | Docker Compose| Simple multi-service orchestration              |

---

## Network Diagram

```
Port Mapping:
─────────────
  Host:5432  ──▶  PostgreSQL Container
  Host:3000  ──▶  Grafana Container

Data Flow:
──────────
  Python App (host) ──INSERT──▶ PostgreSQL ◀──SELECT── Grafana
                                    ▲
                                    │
                               Power BI (host)
```

---

## Design Decisions

1. **Python runs on host, not in Docker** — Allows `psutil` to read actual host system metrics instead of container metrics.
2. **Cumulative network counters** — Stored as-is (cumulative since boot) rather than deltas, allowing both approaches in downstream queries.
3. **SQL views for Power BI** — Pre-aggregated views reduce query complexity in Power BI and ensure consistent reporting logic.
4. **Grafana provisioning** — Datasource and dashboard are auto-configured via YAML/JSON files, enabling reproducible setup.
