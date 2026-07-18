import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent

def run_behave():
    reports = BASE / 'reports'
    reports.mkdir(exist_ok=True)
    cmd = ['behave', '-f', 'json.pretty', '-o', str(reports / 'behave_report.json')]
    subprocess.run(cmd, cwd=BASE)

if __name__ == '__main__':
    run_behave()
