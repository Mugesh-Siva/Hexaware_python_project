import database.setup as setup
from services.restaurantServices.restaurantAuthServices import createRestaurant, isIdTaken
from utils.validators import validate_address, validate_contact, validate_email, validate_name, validate_password


def registerRestaurent():
    setup.setupDatabase()

    print("=" * 49)
    print("Welcome to Restaurant Registration")
    print("=" * 49)

    print()
    print("Enter 0 in the ID and Password fields to exit to the previous menu")

    while True:
        while True:
            name = input("Enter your restaurant name: ").strip()
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
            address = input("Enter your restaurant address: ").strip()
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
            contact_number = input("Enter your restaurant contact number: ").strip()
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
            user_id = input("Enter your restaurant ID: ").strip()
            if user_id == "0":
                print()
                return
            if len(user_id) < 3:
                print()
                print("=" * 49)
                print("Restaurant ID must be at least 3 characters long.")
                print("=" * 49)
                continue
            if isIdTaken(user_id):
                print()
                print("=" * 49)
                print("Restaurant already exists with this ID. Please choose another one.")
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

        result = createRestaurant(name, address, contact_number, user_id, recovery_email, password)
        if result["success"]:
            print()
            print("=" * 49)
            print("Restaurant Registration Successful")
            print("=" * 49)
            return

        print()
        print("=" * 49)
        print(result["message"])
        print("=" * 49)
        continue

