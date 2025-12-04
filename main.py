import logging

from auth import login
from menu import employee_menu


def main():
    """Main application entry point"""
    main_logger = logging.getLogger('expense_app.main')
    main_logger.info("=== Employee Expense Application Starting ===")

    print("=== Employee Expense App ===")

    login_attempts = 0
    while True:
        try:
            main_logger.debug("Waiting for user login")
            user = login()
            login_attempts += 1

            if user:
                main_logger.info(f"User {user['username']} logged in successfully (Attempt #{login_attempts})")
                login_attempts = 0  # Reset counter on successful login

                try:
                    employee_menu(user)
                    main_logger.info(f"User {user['username']} exited menu normally")
                except Exception as e:
                    main_logger.error(f"Error in employee menu for user {user.get('username', 'Unknown')}: {e}",
                                      exc_info=True)
                    print("An error occurred. Please try again.\n")
            else:
                main_logger.warning(f"Login failed (Attempt #{login_attempts})")

            again = input("Login again? (y/n): ")
            main_logger.debug(f"User chose to {'continue' if again.lower() == 'y' else 'exit'}")

            if again.lower() != "y":
                print("Goodbye!")
                main_logger.info("Application terminated by user")
                break

        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
            main_logger.warning("Application interrupted by KeyboardInterrupt")
            break
        except Exception as e:
            main_logger.critical(f"Unexpected error in main loop: {e}", exc_info=True)
            print("A critical error occurred. Please restart the application.\n")
            break

    main_logger.info("=== Employee Expense Application Ended ===")


if __name__ == "__main__":
    main()