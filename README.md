# Data Testing Framework - Sample

This sample automation framework demonstrates data quality testing using Behave (BDD), Great Expectations, and a minimal DBT skeleton. It validates two example tables: `users` and `orders` in a local SQLite database.

Quick start

1. Create and activate a virtualenv:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Initialize the sample database and run tests:

```powershell
python db\init_db.py
behave -f pretty -o reports/behave_report.txt
```

3. Reports are written to `reports/`.

This repository is intended as a sample; extend expectations, DBT models, and CI integration as needed.
