#  System Monitoring & Analytics Dashboard

A real-time system monitoring application that collects local machine metrics (CPU, RAM, Disk, Network) and stores them in PostgreSQL for visualization in Grafana and analysis in Power BI.

Built as a portfolio project demonstrating **Python**, **SQL**, **data collection**, **ETL workflows**, **dashboarding**, and **containerized infrastructure**.

---

##  Technologies Used

| Category       | Technology                          |
| -------------- | ----------------------------------- |
| Language        | Python 3.11                        |
| Database        | PostgreSQL 15                      |
| Visualization   | Grafana 10.3                       |
| BI Reporting    | Power BI (via SQL views)           |
| Containerization| Docker & Docker Compose            |
| Libraries       | psutil, psycopg2, pandas, schedule |

---

##  Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Local Machine                            │
│                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌────────────┐   │
│   │   Python     │───▶│  PostgreSQL   │◀───│  Grafana   │   │
│   │   Collector  │     │  (Docker)    │     │  (Docker)  │   │
│   │   (psutil)   │     │              │     │  :3000     │   │
│   └──────────────┘     └──────────────┘     └────────────┘   │
│         │                     │                              │
│         │ Collects            │ SQL Views                    │
│         │ every 5s            ▼                              │
│         ▼              ┌──────────────┐                      │
│   CPU, RAM, Disk       │  Power BI    │                      │
│   Network stats        │  (Optional)  │                      │
│                        └──────────────┘                      │
└──────────────────────────────────────────────────────────────┘
```

---

##  Project Structure

```
system-monitoring-dashboard/
├── docker-compose.yml          # PostgreSQL + Grafana services
├── Dockerfile                  # Python app container (optional)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuration from .env
│   ├── collector.py            # System metrics collection
│   ├── database.py             # PostgreSQL operations
│   └── main.py                 # Application entry point
│
├── sql/
│   ├── init.sql                # Table creation script
│   └── views.sql               # Power BI ready views
│
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── datasource.yml  # PostgreSQL datasource config
│       └── dashboards/
│           ├── dashboard.yml   # Dashboard provider config
│           └── system_metrics.json  # Pre-built dashboard
│
└── docs/
    ├── architecture.md         # System architecture details
    ├── setup.md                # Complete setup instructions
    └── progress_log.md         # Development progress log

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Git

## Grafana Dashboard

The pre-configured dashboard includes:

| Panel                | Type        | Description                          |
| -------------------- | ----------- | ------------------------------------ |
| CPU Usage Over Time  | Time Series | Line chart of CPU % over time        |
| RAM Usage Over Time  | Time Series | Line chart of memory % over time     |
| Disk Usage           | Gauge       | Current disk usage with thresholds   |
| Current CPU          | Gauge       | Latest CPU reading with thresholds   |
| Network Activity     | Time Series | Bytes sent and received over time    |

The dashboard auto-refreshes every **5 seconds**.



##  Power BI Integration

SQL views are pre-created for Power BI connectivity:

| View              | Purpose                              |
| ----------------- | ------------------------------------ |
| `hourly_metrics`  | Hourly averages for trend analysis   |
| `daily_summary`   | Daily aggregates for exec reporting  |
| `latest_metrics`  | Most recent system reading           |


## 🗄️ Database

### Table: `system_metrics`

| Column             | Type      | Description                    |
| ------------------ | --------- | ------------------------------ |
| `id`               | SERIAL    | Auto-incrementing primary key  |
| `timestamp`        | TIMESTAMP | Time of measurement            |
| `cpu_usage`        | REAL      | CPU usage % (0–100)            |
| `ram_usage`        | REAL      | RAM usage % (0–100)            |
| `disk_usage`       | REAL      | Disk usage % (0–100)           |
| `network_sent`     | BIGINT    | Cumulative bytes sent          |
| `network_received` | BIGINT    | Cumulative bytes received      |





## Future Improvements

- [ ] Add alerting rules in Grafana (e.g., CPU > 90%)
- [ ] Add per-process CPU/RAM tracking
- [ ] Historical data cleanup (auto-delete records older than 30 days)
- [ ] Add temperature monitoring (if hardware supports it)
- [ ] Export metrics to CSV for offline analysis
- [ ] Add unit tests for collector and database modules

---

##  Skills Demonstrated

- **Python**: Data collection, scheduling, database interaction
- **SQL**: Schema design, aggregation views, indexing
- **ETL**: Extract (psutil) → Transform (Python) → Load (PostgreSQL)
- **Data Visualization**: Grafana dashboards with multiple panel types
- **Business Intelligence**: Power BI-ready SQL views
- **DevOps**: Docker Compose, environment configuration
- **Software Engineering**: Modular code, logging, error handling

