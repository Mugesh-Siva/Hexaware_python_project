import ui.restaurent.menus.menuUI as menu
import ui.restaurent.orders.orderListUI as orderListUI
from services.menuServices.listMenu import getMenusByRestaurant
from services.restaurantServices.restaurantAuthServices import getRestaurantById, updateRestaurantProfile
from utils.input_helpers import safe_choice_input
from utils.validators import validate_address, validate_contact, validate_email, validate_name


class restaurentHome:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def print_restaurant_header(self):
        profile_result = getRestaurantById(self.id)
        name = self.id
        address = "Not set"
        contact = "Not set"
        menu_count = 0

        if profile_result["success"]:
            restaurant = profile_result["restaurant"]
            name = restaurant.get("name") or self.id
            address = restaurant.get("address") or "Not set"
            contact = restaurant.get("contact_number") or "Not set"

        menu_result = getMenusByRestaurant(self.id)
        if menu_result["success"]:
            menu_count = len(menu_result["menus"])

        print()
        print("=" * 49)
        print(f"RESTAURANT: {name.upper()}")
        print("=" * 49)
        print(f"Owner ID: {self.id}")
        print(f"Address: {address}")
        print(f"Contact Number: {contact}")
        print(f"Menu Items Listed: {menu_count}")
        print("-" * 49)

    def restUI(self):
        self.print_restaurant_header()

        while True:
            print()
            print("=" * 49)
            print("RESTAURANT DASHBOARD")
            print("=" * 49)
            print("1. Menus")
            print("2. Orders")
            print("3. Profile")
            print("4. Logout")

            choice, error = safe_choice_input(input("Enter your choice: ").strip(), {"1", "2", "3", "4"}, field_name="Choice")
            if error:
                print(error)
                continue

            if choice == "1":
                print()
                print("Menus")
                rest_menu = menu.menuUI(self.id, self.role)
                rest_menu.menuList()

            elif choice == "2":
                print()
                order_screen = orderListUI.orderListUI(self.id, self.role)
                order_screen.listOrders()

            elif choice == "3":
                self.profile_menu()

            elif choice == "4":
                print()
                print("Logging out...")
                return

    def profile_menu(self):
        while True:
            result = getRestaurantById(self.id)
            if not result["success"]:
                print(result["message"])
                return

            restaurant = result["restaurant"]
            print()
            print("=" * 49)
            print("PROFILE")
            print("=" * 49)
            print(f"Restaurant ID: {restaurant.get('id', self.id)}")
            print(f"Restaurant Name: {restaurant.get('name', 'Not set')}")
            print(f"Address: {restaurant.get('address', 'Not set')}")
            print(f"Contact Number: {restaurant.get('contact_number', 'Not set')}")
            print(f"Recovery Email: {restaurant.get('recovery_email', 'Not set')}")
            print("-" * 49)
            print("1. Edit restaurant name")
            print("2. Edit address")
            print("3. Edit contact number")
            print("4. Edit recovery email")
            print("5. Back to main menu")
            print("-" * 49)

            choice, error = safe_choice_input(input("Enter your choice (1-5): ").strip(), {"1", "2", "3", "4", "5"}, field_name="Choice")
            if error:
                print(error)
                continue

            if choice == "1":
                self.edit_profile_field("name", "restaurant name", validate_name)
            elif choice == "2":
                self.edit_profile_field("address", "address", validate_address)
            elif choice == "3":
                self.edit_profile_field("contact_number", "contact number", validate_contact)
            elif choice == "4":
                self.edit_profile_field("recovery_email", "recovery email", validate_email)
            elif choice == "5":
                return

    def edit_profile_field(self, field_name, label, validator):
        while True:
            new_value = input(f"Enter new {label}: ").strip()
            if new_value.lower() in {"0", "cancel", "back"}:
                print("Edit cancelled.")
                return

            valid, message = validator(new_value)
            if not valid:
                print(message)
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != "y":
                    return
                continue

            result = updateRestaurantProfile(self.id, field_name, new_value)
            if result["success"]:
                print(result["message"])
                return
            print(result["message"])
            return
