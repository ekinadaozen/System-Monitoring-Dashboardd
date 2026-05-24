# 🔧 Setup Guide

Complete setup instructions for the System Monitoring & Analytics Dashboard.

---

## Prerequisites

Before starting, make sure you have the following installed:

| Tool             | Version  | Download Link                                    |
| ---------------- | -------- | ------------------------------------------------ |
| Python           | 3.9+     | https://www.python.org/downloads/                |
| Docker           | 20.10+   | https://docs.docker.com/get-docker/              |
| Docker Compose   | 2.0+     | Included with Docker Desktop                     |
| Git              | Any      | https://git-scm.com/downloads                    |
| Power BI Desktop | Optional | https://powerbi.microsoft.com/desktop/           |

---

## Step 1: Clone the Project

```bash
git clone https://github.com/yourusername/system-monitoring-dashboard.git
cd system-monitoring-dashboard
```

---

## Step 2: Environment Configuration

Copy the example environment file and adjust if needed:

```bash
cp .env.example .env
```

Default values in `.env`:

```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=system_metrics_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
COLLECTION_INTERVAL=5
```

> **Note**: These defaults work out-of-the-box with the Docker Compose configuration.

---

## Step 3: Start Docker Services

Start PostgreSQL and Grafana:

```bash
docker-compose up -d
```

Verify the containers are running:

```bash
docker-compose ps
```

Expected output:

```
NAME               STATUS          PORTS
metrics_grafana    Up              0.0.0.0:3000->3000/tcp
metrics_postgres   Up              0.0.0.0:5432->5432/tcp
```

---

## Step 4: Install Python Dependencies

Create a virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 5: Run the Collector

```bash
python -m src.main
```

You'll see log output confirming metrics are being collected:

```
2026-05-23 14:00:00  INFO      ==================================================
2026-05-23 14:00:00  INFO      System Monitoring Collector Started
2026-05-23 14:00:00  INFO      Collection interval: 5 seconds
2026-05-23 14:00:00  INFO      ==================================================
2026-05-23 14:00:01  INFO      CPU: 12.3%  |  RAM: 45.6%  |  Disk: 62.1%  ...
```

Press `Ctrl+C` to stop the collector.

---

## Step 6: Grafana Setup

### Access Grafana

1. Open your browser and go to **http://localhost:3000**
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. Skip the password change prompt (or set a new password)

### Dashboard

The **System Metrics Dashboard** is automatically provisioned and available immediately. Navigate to:

**Dashboards → System Metrics Dashboard**

### Manual Datasource Setup (if needed)

If the auto-provisioned datasource doesn't connect:

1. Go to **Connections → Data Sources → Add data source**
2. Select **PostgreSQL**
3. Configure:
   - Host: `postgres:5432` (if Grafana is in Docker) or `localhost:5432` (if running locally)
   - Database: `system_metrics_db`
   - User: `admin`
   - Password: `admin123`
   - SSL Mode: `disable`
4. Click **Save & Test**

### Example Grafana Panels

To create panels manually:

**CPU Usage Time Series:**
```sql
SELECT timestamp AS time, cpu_usage
FROM system_metrics
WHERE $__timeFilter(timestamp)
ORDER BY timestamp
```

**RAM Usage Time Series:**
```sql
SELECT timestamp AS time, ram_usage
FROM system_metrics
WHERE $__timeFilter(timestamp)
ORDER BY timestamp
```

**Network Activity:**
```sql
SELECT timestamp AS time, network_sent, network_received
FROM system_metrics
WHERE $__timeFilter(timestamp)
ORDER BY timestamp
```

---

## Step 7: Power BI Setup (Optional)

1. Open **Power BI Desktop**
2. Click **Get Data → PostgreSQL Database**
3. Enter connection details:
   - Server: `localhost`
   - Database: `system_metrics_db`
4. Enter credentials:
   - User: `admin`
   - Password: `admin123`
5. Select the views to import:
   - `hourly_metrics` — Hourly averages for trend analysis
   - `daily_summary` — Daily summaries for executive reporting
   - `latest_metrics` — Most recent reading
6. Build reports using these views

---

## Step 8: Verify Everything Works

Run this checklist:

- [ ] `docker-compose ps` shows both containers running
- [ ] Python collector prints metrics to the terminal
- [ ] Grafana dashboard shows live data at http://localhost:3000
- [ ] (Optional) Power BI can connect and pull data

---

## Stopping the Project

```bash
# Stop the Python collector
Ctrl+C

# Stop Docker services
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## Troubleshooting

| Issue                          | Solution                                          |
| ------------------------------ | ------------------------------------------------- |
| Port 5432 already in use       | Stop local PostgreSQL or change port in `.env`    |
| Port 3000 already in use       | Change Grafana port in `docker-compose.yml`       |
| Connection refused errors      | Wait 10s after `docker-compose up` for DB startup |
| Grafana shows "No data"        | Check time range (top-right) is set to "Last 1h"  |
| psutil permission error        | Run with elevated permissions (admin/sudo)         |
