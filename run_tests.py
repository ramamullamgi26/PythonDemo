import subprocess
import sys
from pathlib import Path
import datetime

BASE = Path(__file__).resolve().parent


def init_db_if_present():
    init_script = BASE / 'db' / 'init_db.py'
    if init_script.exists():
        subprocess.run([sys.executable, str(init_script)], cwd=BASE)


def run_behave():
    reports = BASE / 'reports'
    reports.mkdir(exist_ok=True)

    # Ensure sample DB exists
    init_db_if_present()

    report_file = reports / 'behave_report.json'
    cmd = [sys.executable, '-m', 'behave', '-f', 'json.pretty', '-o', str(report_file)]
    result = subprocess.run(cmd, cwd=BASE)

    # Create a small README in reports describing the run
    readme = reports / 'README_FROM_TESTS.md'
    with readme.open('w', encoding='utf-8') as fh:
        fh.write(f"# Test Run Report\n\nGenerated: {datetime.datetime.utcnow().isoformat()}Z\n\n")
        fh.write(f"Command: {' '.join(cmd)}\n\n")
        fh.write(f"Return code: {result.returncode}\n\n")
        fh.write(f"Report file: {report_file.name}\n")

    return result.returncode


if __name__ == '__main__':
    raise SystemExit(run_behave())
