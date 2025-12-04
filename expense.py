from storage import add_expense, add_approval, get_expenses_for_user, \
    get_expense_by_id, get_approval_by_expense, \
    update_expense, delete_expense

import datetime
import logging
import os


# Setup logging
def setup_logging():
    """Configure logging for the expense application"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # File handler - logs everything to file
    file_handler = logging.FileHandler('logs/employee_app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))

    # Console handler - logs warnings and above to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))

    # Configure root logger
    logger = logging.getLogger('expense_app')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Initialize logger
logger = setup_logging()


def submit_expense(user):
    logger.info(f"User {user['username']} (ID: {user['id']}) starting expense submission")
    print("\n=== Submit Expense ===")

    # Validate amount with loop
    amt = None
    attempts = 0
    while True:
        try:
            amt = float(input("Amount: "))
            attempts += 1

            if amt > 5000:
                print("Error: Amount cannot exceed $5000. Please re-enter.")
                logger.warning(f"User {user['username']} attempted to submit amount over $5000: ${amt}")
                continue
            if amt <= 0:
                print("Error: Amount must be greater than $0. Please re-enter.")
                logger.warning(f"User {user['username']} attempted to submit non-positive amount: ${amt}")
                continue
            break
        except ValueError as e:
            print("Error: Invalid amount. Please enter a valid number.")
            logger.warning(f"User {user['username']} entered invalid amount format: {e}")

    desc = input("Description: ")
    date = input("Date (YYYY-MM-DD, leave empty for today): ")

    if not date:
        date = datetime.date.today().isoformat()
        logger.debug(f"Using today's date: {date}")

    # Create expense WITHOUT ID
    new_exp = {
        "user_id": user["id"],
        "amount": amt,
        "description": desc,
        "date": date
    }

    try:
        # Get the DB-generated expense ID
        expense_id = add_expense(new_exp)
        logger.info(
            f"Expense created - ID: {expense_id}, User: {user['username']}, Amount: ${amt}, Description: {desc}")

        # Create an approval entry linked to new expense
        add_approval({
            "expense_id": expense_id,
            "status": "pending",
            "comment": ""
        })
        logger.debug(f"Approval entry created for expense ID: {expense_id}")

        print("Expense submitted successfully!\n")
        logger.info(f"Expense submission completed successfully for user {user['username']}")
    except Exception as e:
        logger.error(f"Failed to submit expense for user {user['username']}: {e}", exc_info=True)
        print("Error: Failed to submit expense. Please try again.\n")


def view_expenses(user):
    logger.info(f"User {user['username']} (ID: {user['id']}) viewing expenses")
    print("\n=== My Expenses ===\n")

    try:
        records = get_expenses_for_user(user["id"])

        if not records:
            print("No expenses found.\n")
            logger.debug(f"No expenses found for user {user['username']}")
            return

        logger.info(f"Retrieved {len(records)} expenses for user {user['username']}")

        # Print table header
        header_format = "{:<8} {:<12} {:<35} {:<12} {:<12} {:<20}"
        print(header_format.format("ID", "Amount", "Description", "Date", "Status", "Comment"))
        print("─" * 105)

        # Print each expense as a table row
        row_format = "{:<8} ${:<11.2f} {:<35} {:<12} {:<12} {:<20}"
        for e in records:
            description = e['description']
            if len(description) > 35:
                description = description[:32] + "..."

            comment = e['comment'] if e['comment'] else 'None'
            if len(comment) > 20:
                comment = comment[:17] + "..."

            print(row_format.format(
                e['id'],
                e['amount'],
                description,
                e['date'],
                e['status'],
                comment
            ))

        print("─" * 105)
        print(f"Total expenses: {len(records)}\n")
    except Exception as e:
        logger.error(f"Error viewing expenses for user {user['username']}: {e}", exc_info=True)
        print("Error: Failed to retrieve expenses.\n")


def edit_expense(user):
    logger.info(f"User {user['username']} (ID: {user['id']}) attempting to edit expense")
    print("\n=== Edit Expense ===")

    try:
        eid = int(input("Expense ID: "))
        logger.debug(f"User {user['username']} attempting to edit expense ID: {eid}")

        expense = get_expense_by_id(eid)
        approval = get_approval_by_expense(eid)

        if not expense or expense["user_id"] != user["id"]:
            print("Invalid expense ID.\n")
            logger.warning(f"User {user['username']} attempted to edit invalid/unauthorized expense ID: {eid}")
            return

        if approval["status"] != "pending":
            print("Only pending expenses can be edited.\n")
            logger.warning(
                f"User {user['username']} attempted to edit non-pending expense ID: {eid} (Status: {approval['status']})")
            return

        logger.debug(
            f"Expense ID {eid} validated for editing - Current amount: ${expense['amount']}, Description: {expense['description']}")

        new_amt = float(input("New Amount: "))
        new_desc = input("New Description: ")
        new_date = input("New Date (YYYY-MM-DD): ")

        update_expense(eid, {
            "amount": new_amt,
            "description": new_desc,
            "date": new_date
        })

        logger.info(
            f"Expense ID {eid} updated by user {user['username']} - New amount: ${new_amt}, New description: {new_desc}, New date: {new_date}")
        print("Expense updated!\n")

    except ValueError as e:
        print("Invalid input. Please enter valid data.\n")
        logger.warning(f"User {user['username']} entered invalid data during edit: {e}")
    except Exception as e:
        logger.error(f"Error editing expense for user {user['username']}: {e}", exc_info=True)
        print("Error: Failed to update expense.\n")


def delete_exp(user):
    logger.info(f"User {user['username']} (ID: {user['id']}) attempting to delete expense")
    print("\n=== Delete Expense ===")

    try:
        eid = int(input("Expense ID: "))
        logger.debug(f"User {user['username']} attempting to delete expense ID: {eid}")

        expense = get_expense_by_id(eid)
        approval = get_approval_by_expense(eid)

        if not expense or expense["user_id"] != user["id"]:
            print("Invalid expense ID.\n")
            logger.warning(f"User {user['username']} attempted to delete invalid/unauthorized expense ID: {eid}")
            return

        if approval["status"] != "pending":
            print("Only pending expenses can be deleted.\n")
            logger.warning(
                f"User {user['username']} attempted to delete non-pending expense ID: {eid} (Status: {approval['status']})")
            return

        logger.debug(
            f"Expense ID {eid} validated for deletion - Amount: ${expense['amount']}, Description: {expense['description']}")

        delete_expense(eid)
        logger.info(
            f"Expense ID {eid} deleted by user {user['username']} - Amount: ${expense['amount']}, Description: {expense['description']}")
        print("Expense deleted.\n")

    except ValueError as e:
        print("Invalid input. Please enter a valid number.\n")
        logger.warning(f"User {user['username']} entered invalid ID during delete: {e}")
    except Exception as e:
        logger.error(f"Error deleting expense for user {user['username']}: {e}", exc_info=True)
        print("Error: Failed to delete expense.\n")