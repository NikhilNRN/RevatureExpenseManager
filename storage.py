import sqlite3

DB = "my_database.db"


def connect():
    return sqlite3.connect(DB)


def get_user(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, username, role FROM users
        WHERE username=? AND password=? AND role='Employee'
    """, (username, password))
    row = cur.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "username": row[1], "role": row[2]}
    return None


def add_expense(expense):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO expenses (user_id, amount, description, date)
        VALUES (?, ?, ?, ?)
    """, (expense["user_id"], expense["amount"], expense["description"], expense["date"]))
    conn.commit()

    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_expense_by_id(eid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, amount, description, date FROM expenses WHERE id=?", (eid,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "user_id": row[1], "amount": row[2], "description": row[3], "date": row[4]}
    return None


def update_expense(expense_id, new_data):
    conn = connect()
    cur = conn.cursor()

    fields = []
    values = []

    for k, v in new_data.items():
        fields.append(f"{k}=?")
        values.append(v)

    values.append(expense_id)

    cur.execute(f"UPDATE expenses SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM approvals WHERE expense_id=?", (expense_id,))
    cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))

    conn.commit()
    conn.close()


def add_approval(approval):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO approvals (expense_id, status, comment)
        VALUES (?, ?, ?)
    """, (approval["expense_id"], approval["status"], approval.get("comment")))
    conn.commit()
    conn.close()


def get_approval_by_expense(eid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT status, comment FROM approvals WHERE expense_id=?
    """, (eid,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {"status": row[0], "comment": row[1]}
    return None


def get_expenses_for_user(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id, amount, description, date FROM expenses WHERE user_id=?", (user_id,))
    expense_rows = cur.fetchall()

    result = []

    for e in expense_rows:
        eid, amount, description, date = e

        cur.execute("SELECT status, comment FROM approvals WHERE expense_id=?", (eid,))
        approval = cur.fetchone()

        merged = {
            "id": eid,
            "amount": amount,
            "description": description,
            "date": date,
            "status": approval[0] if approval else None,
            "comment": approval[1] if approval else None,
        }

        result.append(merged)

    conn.close()
    return result
