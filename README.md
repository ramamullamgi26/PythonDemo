# Data Testing Framework - Sample

This repository is a lightweight example data-quality testing framework using:
- Behave (BDD) for acceptance-style tests
- Great Expectations (lightweight inclusion for demonstration)
- A minimal DBT models skeleton (under `dbt/`) to show where transformations would live

The tests validate two example tables in a local SQLite database: `users` and `orders`.

**Contents**
- `db/` — DB helpers and `init_db.py` to create and seed `data.db`.
- `features/` — Behave feature files and step implementations.
	- `features/users_table_validation.feature`
	- `features/orders_table_validation.feature`
	- `features/steps/data_steps.py` — step definitions used by the features.
- `utils/` — helper utilities (e.g. `db_connection.py`).
- `reports/` — generated test reports and run metadata.
- `run_tests.py` — robust test runner that initializes DB, runs Behave, and writes `reports/README_FROM_TESTS.md`.
- `behave.ini` — default Behave configuration.

Prerequisites
1. Python 3.8+ installed
2. Recommended: create an isolated virtual environment

Quick start (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Initialize the database (creates `data.db` at repo root)

```powershell
python db\init_db.py
```

Run the full test suite (preferred single command)

```powershell
python run_tests.py
```

This will:
- Initialize the sample SQLite DB (if `db/init_db.py` exists).
- Run Behave via `python -m behave` (avoids PATH issues).
- Write `reports/behave_report.json` and `reports/README_FROM_TESTS.md`.

Alternative direct Behave run

```powershell
python -m behave -f json.pretty -o reports/behave_report.json
```

Project structure and details

- `db/init_db.py` — creates two tables and seeds sample data:
	- `users(user_id, email, name, signup_date)`
	- `orders(order_id, user_id, amount, order_date, status)`

- `features/` & Behave specifics:
	- Feature files describe acceptance criteria for `users` and `orders` tables.
	- Step definitions are implemented in `features/steps/data_steps.py` and call helpers in `utils/` to connect to the DB and run assertions.

- `utils/db_connection.py` — convenience functions to open a SQLite connection and return pandas DataFrames for assertions.

- `run_tests.py` — a small runner that:
	1. Runs `db/init_db.py` to ensure the DB is present.
	2. Executes Behave via the current Python interpreter.
	3. Writes `reports/README_FROM_TESTS.md` with command, timestamp, and exit code.

Reports
- JSON report: `reports/behave_report.json` (machine-readable)
- Run summary: `reports/README_FROM_TESTS.md` (human-readable)

Extending the framework
- Add new feature files under `features/` and corresponding step implementations under `features/steps/`.
- Put reusable helpers in `utils/` (DB access, data generation, comparison utilities).
- Add Great Expectations expectation suites under a `great_expectations/` directory if you want more dataset-level checks.

CI recommendations
- Use `python -m pip install -r requirements.txt` in your CI job to avoid PATH/script issues.
- Run `python run_tests.py` as the single test command.
- Archive `reports/` as build artifacts.

Notes
- `run_tests.py` uses `sys.executable -m behave` to avoid relying on `Scripts` being on PATH.
- The sample uses SQLite for simplicity; swap in Postgres/MySQL by updating `utils/db_connection.py` and `db/init_db.py` (or replace init logic with migrations).

Contact / Contributing
If you add features or change test behavior, please:
1. Add feature files under `features/`.
2. Implement or refactor steps under `features/steps/`.
3. Add or update helpers in `utils/`.

Enjoy experimenting and extending this sample framework!

Examples
--------

Below are small excerpts from the repository that illustrate how features, step definitions, and utilities work together.

Feature example (`features/users_table_validation.feature`)

```gherkin
Feature: Users table data quality
  Validate the `users` table for schema, uniqueness, nulls and business rules.

  Scenario: Users table has expected columns
	Given the database is available
	When I inspect the `users` table schema
	Then the table should contain columns `user_id`, `email`, `name`, `signup_date`
```

Step definitions excerpt (`features/steps/data_steps.py`)

```python
@given('the `{table}` table is loaded')
def step_table_loaded(context, table):
	conn = get_connection()
	df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
	conn.close()
	context.table = table
	context.df = df

@then('values in column `{col}` should be unique')
def step_unique(context, col):
	assert context.df[col].is_unique, f"Duplicate values found in {col}"
```

Utility example (`utils/db_connection.py`)

```python
from pathlib import Path
import sqlite3

def get_connection():
	base = Path(__file__).resolve().parents[1]
	db_path = base / 'data.db'
	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row
	return conn
```

Where to extend
- Add new scenarios in `features/` and corresponding implementations in `features/steps/`.
- Use `utils/` to add reusable helpers (data builders, DB fixtures, comparison helpers).

