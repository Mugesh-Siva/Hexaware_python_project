import ui.customer.customerHome as customerHome
from services.customerServices.customerAuthServices import loginCustomer


def customerLogin():
    role = "customer"

    try:
        while True:
            print()
            print("=" * 49)
            print("Welcome Customer")
            print("=" * 49)
            print()
            print("Enter 0 in the ID and Password fields to exit to the previous menu")
            user_id = input("Enter your ID: ").strip()
            password = input("Enter your password: ").strip()

            if user_id == "0" and password == "0":
                print()
                return

            if not user_id or not password:
                print()
                print("=" * 49)
                print("ID and password cannot be empty")
                print("=" * 49)
                continue

            if loginCustomer(user_id, password):
                print()
                print("=" * 49)
                print("Login Successful")
                print("=" * 49)
                customer_app = customerHome.customerHome(user_id, role)
                customer_app.start()
                return

            print()
            print("=" * 49)
            print("Invalid ID or Password")
            print("=" * 49)
    except EOFError:
        print()
        print("=" * 49)
        print("Input closed. Returning to previous menu.")
        print("=" * 49)

