# main.py
from auth import login
from menu import employee_menu


def main():
    print("=== Employee Expense App ===")
    while True:
        user = login()
        if user:
            employee_menu(user)

        again = input("Login again? (y/n): ")
        if again.lower() != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
