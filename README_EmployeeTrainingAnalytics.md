# Employee Training Session Analytics Portal

> A Django-based analytics dashboard for tracking employee training completion, attendance trends, and compliance metrics with data visualization.

![Django](https://img.shields.io/badge/Django-4-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-2-purple)
![Chart.js](https://img.shields.io/badge/Chart.js-4-pink)

---

## Problem Statement

HR departments and training coordinators face critical visibility gaps:
- **No centralized view** of who has completed mandatory training (compliance risk)
- **Manual spreadsheet tracking** that becomes obsolete the moment it's exported
- **No trend analysis** — Can't identify departments with declining attendance or courses with high dropout rates
- **Reactive compliance** — Discovering expired certifications during audits rather than before

This portal transforms training data from static records into **actionable intelligence** for proactive workforce development.

---

## Demo

### Completion Dashboard
*Organization-wide training completion rates with drill-down by department and course.*

### Attendance Trends
*Time-series visualization showing enrollment vs. actual attendance, highlighting dropout patterns.*

### Compliance Alerts
*Automated flagging of employees approaching certification expiration or missing mandatory courses.*

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend Framework | Django 4 | Rapid development with built-in admin, ORM, and security |
| Language | Python 3.11 | Data processing and analytics logic |
| Data Analysis | Pandas | Aggregation, filtering, and statistical computation |
| Visualization | Chart.js | Interactive, responsive charts in the browser |
| Database | SQLite (dev) / PostgreSQL (prod) | Lightweight development, production persistence |
| Frontend | Django Templates + Bootstrap 5 | Server-rendered pages with responsive design |
| Data Export | Pandas + OpenPyXL | Excel report generation for HR workflows |

---

## Key Features

- **Completion tracking** — Real-time dashboard of training completion rates by employee, department, and course
- **Attendance trend analysis** — Time-series charts showing enrollment patterns, no-show rates, and seasonal trends
- **Compliance monitoring** — Automated alerts for upcoming certification expirations and missing mandatory training
- **Department benchmarking** — Comparative analytics showing which departments lead or lag in training engagement
- **Course effectiveness metrics** — Dropout rates, average completion time, and post-training assessment scores
- **Exportable reports** — One-click generation of Excel and PDF reports for audits and management reviews
- **Role-based views** — HR sees organization-wide data; managers see their team; employees see their own record

---

## Architecture Decisions

**Why Django over Flask or FastAPI?**

Django's "batteries included" philosophy was ideal for this project because:
- **Admin interface:** Django's auto-generated admin panel provided CRUD operations for training records without writing a single line of frontend code
- **ORM:** Complex queries across employees, departments, courses, and sessions were expressible in Python rather than raw SQL
- **Security:** Built-in CSRF protection, SQL injection prevention, and XSS filtering—critical for HR data
- **Rapid prototyping:** From concept to functional prototype in 3 days

**Why Pandas + Chart.js instead of a dedicated BI tool?**

Enterprise BI tools (Tableau, PowerBI) require licensing and infrastructure. This solution provides 80% of the value with zero recurring cost, deployable to any server. Pandas handles the data transformation; Chart.js renders it beautifully in the browser.

---

## Challenges & Solutions

### Challenge: Slow analytics queries on large datasets
With 10,000+ training records, the completion rate dashboard took 8+ seconds to load due to repeated aggregate queries.

**Solution:** Implemented **materialized views** in PostgreSQL (and a Django management command to refresh them). Pre-computed completion metrics reduced dashboard load time from 8.2s to 340ms—a 24x improvement.

### Challenge: Complex date-based compliance logic
Determining "expired" vs. "expiring soon" vs. "valid" required handling timezone-aware dates, business day calculations, and grace periods.

**Solution:** Built a **compliance engine** using Python's `dateutil` and `relativedelta` that encapsulates all date arithmetic. This centralizes business rules and makes the system testable:
```python
class ComplianceEngine:
    def status(self, certification_date, validity_months, grace_days=30):
        expiration = certification_date + relativedelta(months=validity_months)
        warning_date = expiration - relativedelta(days=grace_days)

        if timezone.now() > expiration:
            return Status.EXPIRED
        elif timezone.now() > warning_date:
            return Status.EXPIRING_SOON
        return Status.VALID
```

### Challenge: Data quality issues
Imported training records had inconsistent date formats, duplicate entries, and missing employee IDs.

**Solution:** Built a **data validation pipeline** using Pandas that:
1. Standardizes date formats across multiple input sources
2. Deduplicates records using composite keys (employee_id + course_id + session_date)
3. Flags orphaned records for manual review rather than silently dropping them
4. Generates a quality report showing what was imported, modified, or rejected

---

## How to Run

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
git clone https://github.com/alfonsojose-go/EmployeeTrainingSessionAnalyticsPortal.git
cd EmployeeTrainingSessionAnalyticsPortal
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scriptsctivate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The application will be available at `http://localhost:8000`.

### Sample Data
```bash
python manage.py loaddata fixtures/sample_training_data.json
```

---

## What I Learned

- **Data engineering fundamentals:** Real-world data is messy. Building a validation pipeline taught me that 70% of analytics work is data cleaning, not visualization.
- **Database optimization:** The difference between a query that scans 10,000 rows and one that uses an index is the difference between a usable app and a broken one. I learned to read `EXPLAIN ANALYZE` output.
- **Stakeholder communication:** I presented this to a mock HR panel. Their first question wasn't "How pretty are the charts?" but "Can I export this to Excel?" I learned to prioritize business workflow integration over technical elegance.

---

## Links

- [GitHub Repository](https://github.com/alfonsojose-go/EmployeeTrainingSessionAnalyticsPortal)

---

**License:** MIT
