import ui.restaurent.restaurentHome as restHome
from services.restaurantServices.restaurantAuthServices import loginRestaurant


def restaurentLogin():
    role = "restaurant"
    print("=" * 49)
    print("Welcome to Restaurant Login")
    print("=" * 49)

    while True:
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

        if loginRestaurant(user_id, password):
            print()
            print("=" * 49)
            print("Login Successful")
            print("=" * 49)
            restaurant_user = restHome.restaurentHome(user_id, role)
            restaurant_user.restUI()
            return

        print()
        print("=" * 49)
        print("Invalid ID or Password")
        print("=" * 49)

