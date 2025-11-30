from storage import add_expense, add_approval, get_expenses_for_user, \
                     get_expense_by_id, get_approval_by_expense, \
                     update_expense, delete_expense

import datetime


def submit_expense(user):
    print("\n=== Submit Expense ===")
    amt = float(input("Amount: "))
    desc = input("Description: ")
    date = input("Date (YYYY-MM-DD, leave empty for today): ")

    if not date:
        date = datetime.date.today().isoformat()

    # Create expense WITHOUT ID
    new_exp = {
        "user_id": user["id"],
        "amount": amt,
        "description": desc,
        "date": date
    }

    # Get the DB-generated expense ID
    expense_id = add_expense(new_exp)

    # Create an approval entry linked to new expense
    add_approval({
        "expense_id": expense_id,
        "status": "pending",
        "comment": ""
    })

    print("Expense submitted successfully!\n")


def view_expenses(user):
    print("\n=== My Expenses ===")
    records = get_expenses_for_user(user["id"])
    if not records:
        print("No expenses found.\n")
        return

    for e in records:
        print(f"""
ID: {e['id']}
Amount: ${e['amount']}
Description: {e['description']}
Date: {e['date']}
Status: {e['status']}
Comment: {e['comment'] if e['comment'] else 'None'}
------------------------
""")


def edit_expense(user):
    print("\n=== Edit Expense ===")
    eid = int(input("Expense ID: "))

    expense = get_expense_by_id(eid)
    approval = get_approval_by_expense(eid)

    if not expense or expense["user_id"] != user["id"]:
        print("Invalid expense ID.\n")
        return

    if approval["status"] != "pending":
        print("Only pending expenses can be edited.\n")
        return

    new_amt = float(input("New Amount: "))
    new_desc = input("New Description: ")
    new_date = input("New Date (YYYY-MM-DD): ")

    update_expense(eid, {
        "amount": new_amt,
        "description": new_desc,
        "date": new_date
    })

    print("Expense updated!\n")


def delete_exp(user):
    print("\n=== Delete Expense ===")
    eid = int(input("Expense ID: "))

    expense = get_expense_by_id(eid)
    approval = get_approval_by_expense(eid)

    if not expense or expense["user_id"] != user["id"]:
        print("Invalid expense ID.\n")
        return

    if approval["status"] != "pending":
        print("Only pending expenses can be deleted.\n")
        return

    delete_expense(eid)
    print("Expense deleted.\n")
