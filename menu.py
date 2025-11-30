# menu.py
from expense import submit_expense, view_expenses, edit_expense, delete_exp


def employee_menu(user):
    while True:
        print("""
========== Employee Menu ==========
1. Submit Expense
2. View My Expenses
3. Edit Pending Expense
4. Delete Pending Expense
5. Logout
""")
        choice = input("Select option: ")

        if choice == "1":
            submit_expense(user)
        elif choice == "2":
            view_expenses(user)
        elif choice == "3":
            edit_expense(user)
        elif choice == "4":
            delete_exp(user)
        elif choice == "5":
            print("Logging out...\n")
            break
        else:
            print("Invalid option.\n")
