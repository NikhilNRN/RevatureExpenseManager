import sqlite3

conn = sqlite3.connect("my_database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    description TEXT,
    date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER,
    status TEXT,
    comment TEXT,
    FOREIGN KEY(expense_id) REFERENCES expenses(id)
)
""")

cur.execute("SELECT COUNT(*) FROM users")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("employee1", "pass123", "Employee"))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("manager1", "admin", "Manager"))

conn.commit()
conn.close()
