import database.setup as setup
from services.customerServices.customerAuthServices import createCustomer, isIdTaken
from utils.validators import (
    validate_address,
    validate_contact,
    validate_email,
    validate_name,
    validate_password,
)


def _prompt_validated_field(prompt, validator, exit_value=None):
    while True:
        value = input(prompt).strip()
        if exit_value is not None and value == str(exit_value):
            return value

        valid, message = validator(value)
        if valid:
            return value

        print()
        print("=" * 49)
        print(message)
        print("=" * 49)


def registerCustomer():
    try:
        setup.setupDatabase()

        print("=" * 49)
        print("Welcome to Customer Registration")
        print("=" * 49)

        print()
        print("Enter 0 in the ID and Password fields to exit to the previous menu")

        while True:
            while True:
                name = input("Enter your full name: ").strip()
                if name == "0":
                    print()
                    return
                valid, message = validate_name(name)
                if valid:
                    break
                print()
                print("=" * 49)
                print(message)
                print("=" * 49)

            while True:
                address = input("Enter your address: ").strip()
                if address == "0":
                    print()
                    return
                valid, message = validate_address(address)
                if valid:
                    break
                print()
                print("=" * 49)
                print(message)
                print("=" * 49)

            while True:
                contact_number = input("Enter your contact number: ").strip()
                if contact_number == "0":
                    print()
                    return
                valid, message = validate_contact(contact_number)
                if valid:
                    break
                print()
                print("=" * 49)
                print(message)
                print("=" * 49)

            while True:
                user_id = input("Enter your ID: ").strip()
                if user_id == "0":
                    print()
                    return
                if len(user_id) < 3:
                    print()
                    print("=" * 49)
                    print("ID must be at least 3 characters long.")
                    print("=" * 49)
                    continue
                if isIdTaken(user_id):
                    print()
                    print("=" * 49)
                    print("User already exists with this ID. Please choose another one.")
                    print("=" * 49)
                    continue
                break

            while True:
                recovery_email = input("Enter your recovery email: ").strip()
                if recovery_email == "0":
                    print()
                    return
                valid, message = validate_email(recovery_email)
                if valid:
                    break
                print()
                print("=" * 49)
                print(message)
                print("=" * 49)

            while True:
                password = input("Enter your password: ").strip()
                if password == "0":
                    print()
                    return
                valid, message = validate_password(password)
                if valid:
                    break
                print()
                print("=" * 49)
                print(message)
                print("=" * 49)

            while True:
                re_password = input("Re-enter your password: ").strip()
                if re_password == "0":
                    print()
                    return
                if password == re_password:
                    break
                print()
                print("=" * 49)
                print("Passwords do not match. Please try again.")
                print("=" * 49)

            result = createCustomer(name, address, contact_number, user_id, recovery_email, password)
            if result["success"]:
                print()
                print("=" * 49)
                print("User Registration Successful")
                print("=" * 49)
                return

            print()
            print("=" * 49)
            print(result["message"])
            print("=" * 49)
            continue
    except EOFError:
        print()
        print("=" * 49)
        print("Input closed. Returning to previous menu.")
        print("=" * 49)
