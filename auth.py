# auth.py
from storage import get_user


def login():
    print("\n=== Employee Login ===")
    uname = input("Username: ")
    pwd = input("Password: ")

    user = get_user(uname, pwd)
    if user:
        print("Login successful.\n")
        return user
    else:
        print("Invalid credentials.\n")
        return None
