import sqlite3
from pathlib import Path

def get_connection():
    # DB file is created at project root as `data.db` by db/init_db.py
    base = Path(__file__).resolve().parents[1]
    db_path = base / 'data.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
