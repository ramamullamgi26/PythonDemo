import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        email TEXT NOT NULL,
        name TEXT,
        signup_date TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        order_date TEXT,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')

    # seed sample data
    cur.execute("DELETE FROM orders")
    cur.execute("DELETE FROM users")

    users = [
        (1, 'alice@example.com', 'Alice', '2024-01-10'),
        (2, 'bob@example.com', 'Bob', '2024-02-15'),
        (3, 'charlie@example.com', 'Charlie', '2024-03-01'),
    ]
    cur.executemany("INSERT INTO users(user_id, email, name, signup_date) VALUES (?, ?, ?, ?)", users)

    orders = [
        (1, 1, 120.50, '2024-04-01', 'completed'),
        (2, 1, 35.00, '2024-04-03', 'shipped'),
        (3, 2, 9.99, '2024-05-12', 'cancelled'),
    ]
    cur.executemany("INSERT INTO orders(order_id, user_id, amount, order_date, status) VALUES (?, ?, ?, ?, ?)", orders)

    conn.commit()
    conn.close()
    print(f"Initialized DB at {DB_PATH}")

if __name__ == '__main__':
    init_db()
