# 📋 Progress Log

Development progress tracking for the System Monitoring & Analytics Dashboard.

---

## ✅ Completed Tasks

### Phase 1: Project Setup
- [x] Initialize project structure
- [x] Create `.gitignore`
- [x] Create `.env.example` with default configuration
- [x] Create `requirements.txt` with Python dependencies

### Phase 2: Database
- [x] Design `system_metrics` table schema
- [x] Write `init.sql` for table creation
- [x] Add timestamp index for query performance
- [x] Create Power BI views (`hourly_metrics`, `daily_summary`, `latest_metrics`)

### Phase 3: Python Application
- [x] Create `config.py` — environment variable loading
- [x] Create `collector.py` — psutil-based metrics collection
- [x] Create `database.py` — PostgreSQL connection and insertion
- [x] Create `main.py` — scheduled collection loop with logging
- [x] Add error handling and graceful shutdown

### Phase 4: Docker
- [x] Create `docker-compose.yml` with PostgreSQL and Grafana
- [x] Configure persistent volumes for data retention
- [x] Mount SQL init scripts for automatic table creation
- [x] Create `Dockerfile` for optional containerized Python app

### Phase 5: Grafana
- [x] Create datasource provisioning (auto-connect to PostgreSQL)
- [x] Create dashboard provisioning configuration
- [x] Build pre-configured dashboard with 5 panels:
  - CPU usage over time (time series)
  - RAM usage over time (time series)
  - Disk usage (gauge)
  - Current CPU (gauge)
  - Network activity (time series)
- [x] Set dashboard auto-refresh to 5 seconds

### Phase 6: Documentation
- [x] Write `README.md` with full project documentation
- [x] Write `docs/architecture.md` with system design details
- [x] Write `docs/setup.md` with step-by-step instructions
- [x] Write `docs/progress_log.md` (this file)

---

## 📝 Development Notes

### Design Decisions
1. **Python on host, not in Docker** — Running the collector on the host machine ensures `psutil` reads actual system metrics rather than container-level metrics.
2. **`schedule` library over APScheduler** — Chosen for simplicity. The `schedule` library has a minimal API that's easy to understand and debug.
3. **Cumulative network counters** — Stored as raw cumulative values from `psutil`. Delta calculations can be done in SQL or Grafana for flexibility.
4. **Grafana auto-provisioning** — Dashboard and datasource are loaded from files on startup, making the setup reproducible without manual configuration.

### Architecture Notes
- The project follows a standard **ETL pattern**: Extract (psutil) → Transform (Python formatting) → Load (PostgreSQL).
- SQL views serve as a clean abstraction layer between raw data and BI tools.
- The modular code structure (`config`, `collector`, `database`, `main`) keeps each component focused and testable.

---

## 🔮 Pending / Future Tasks

- [ ] Add screenshots to README after first run
- [ ] Add alerting rules in Grafana
- [ ] Add per-process CPU/RAM tracking
- [ ] Create automated data cleanup (e.g., delete records older than 30 days)
- [ ] Add temperature/battery monitoring (hardware-dependent)
- [ ] Export to CSV functionality
- [ ] Write unit tests for collector and database modules
- [ ] Add CI/CD pipeline configuration
