import auth.customerLogin as custLogin
import auth.restaurentLogin as restLogin
import auth.registerCustomer as regCustomer
import auth.restaurentRegister as regRestaurent
from utils.input_helpers import safe_choice_input


def welcome():
    while True:
        try:
            print()
            print("=" * 49)
            print("Welcome")
            print("=" * 49)
            print()
            print("1. Customer Login")
            print("2. Restaurant Login")
            print("3. Create Customer Account")
            print("4. Create Restaurant Account")
            print("5. Exit The App")
            choice, error = safe_choice_input(input("Enter your choice: ").strip(), {"1", "2", "3", "4", "5"}, field_name="Choice")
            if error:
                print()
                print("=" * 49)
                print(error)
                print("=" * 49)
                continue

            if choice == "1":
                custLogin.customerLogin()
            elif choice == "2":
                restLogin.restaurentLogin()
            elif choice == "3":
                regCustomer.registerCustomer()
            elif choice == "4":
                regRestaurent.registerRestaurent()
            elif choice == "5":
                print()
                print("=" * 49)
                print("Thank You")
                print("=" * 49)
                print()
                break
        except Exception as exc:
            print()
            print("=" * 49)
            print(f"Unexpected error: {exc}")
            print("=" * 49)
