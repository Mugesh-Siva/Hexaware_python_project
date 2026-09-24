from services.customerServices.browseItems import add_item_to_cart, get_menu_page
from services.customerServices.cart import get_cart, remove_cart_item, update_cart_quantity
from services.customerServices.customerAuthServices import getCustomerById, updateCustomerProfile
from utils.validators import validate_address, validate_contact, validate_email, validate_name


class customerHome:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def print_customer_header(self):
        profile_result = getCustomerById(self.id)
        name = self.id
        address = "Not set"
        contact = "Not set"

        if profile_result["success"]:
            customer = profile_result["customer"]
            name = customer.get("name") or self.id
            address = customer.get("address") or "Not set"
            contact = customer.get("contact_number") or "Not set"

        print()
        print("=" * 49)
        print(f"WELCOME {name.upper()}")
        print("=" * 49)
        print(f"Customer ID: {self.id}")
        print(f"Delivery Address: {address}")
        print(f"Contact Number: {contact}")
        print("-" * 49)

    def start(self):
        self.print_customer_header()
        while True:
            try:
                print()
                print("=" * 49)
                print("CUSTOMER DASHBOARD")
                print("=" * 49)
                print("1. Browse Items")
                print("2. Cart")
                print("3. Orders")
                print("4. Profile")
                print("5. Logout")
                print("=" * 49)
                choice = input("Enter your choice (1-5): ").strip()

                if choice == "":
                    raise ValueError("empty")

                choice = int(choice)

                if choice == 1:
                    self.browse_items()
                elif choice == 2:
                    self.cart_menu()
                elif choice == 3:
                    print("Orders are not implemented yet.")
                elif choice == 4:
                    self.profile_menu()
                elif choice == 5:
                    print("Logging out...")
                    return
                else:
                    print("Invalid choice. Please select a valid option.")

            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as exc:
                print(f"Error: {exc}")
                continue

    def profile_menu(self):
        while True:
            profile_result = getCustomerById(self.id)
            if not profile_result["success"]:
                print(profile_result["message"])
                return

            customer = profile_result["customer"]
            print()
            print("=" * 49)
            print("PROFILE")
            print("=" * 49)
            print(f"Customer ID: {customer.get('id', self.id)}")
            print(f"Name: {customer.get('name', 'Not set')}")
            print(f"Address: {customer.get('address', 'Not set')}")
            print(f"Contact Number: {customer.get('contact_number', 'Not set')}")
            print(f"Recovery Email: {customer.get('recovery_email', 'Not set')}")
            print("-" * 49)
            print("1. Edit name")
            print("2. Edit address")
            print("3. Edit contact number")
            print("4. Edit recovery email")
            print("5. Back to main menu")
            print("-" * 49)

            choice = input("Enter your choice (1-5): ").strip()
            if choice == "1":
                self.edit_profile_field("name", "Name", validate_name)
            elif choice == "2":
                self.edit_profile_field("address", "Address", validate_address)
            elif choice == "3":
                self.edit_profile_field("contact_number", "Contact Number", validate_contact)
            elif choice == "4":
                self.edit_profile_field("recovery_email", "Recovery Email", validate_email)
            elif choice == "5":
                return
            else:
                print("Invalid choice. Please select a valid option.")

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

            result = updateCustomerProfile(self.id, field_name, new_value)
            if result["success"]:
                print(result["message"])
                return
            print(result["message"])
            return

    def browse_items(self):
        current_page = 0

        while True:
            try:
                result = get_menu_page(current_page, 10)
                if not result["success"]:
                    print(result["message"])
                    return

                items = result["items"]
                if not items:
                    print("No items available.")
                    return

                print()
                print("-" * 49)
                print("MENU ITEMS")
                print("-" * 49)
                for item in items:
                    menu_id, title, description, price, nutrients, availability, user_id = item
                    status = "Available" if availability == 1 else "Unavailable"
                    print(f"{menu_id}. {title} - ₹{price}")
                    print(f"   {description}")
                    print(f"   Nutrients: {nutrients or 'Not specified'} | Status: {status}")
                print("-" * 49)
                print("Type 'next' for next page")
                print("Type 'back' for previous page")
                print("Type item ID to add it to cart")
                print("Type '0' to return to main menu")
                print("-" * 49)

                user_choice = input("Enter choice: ").strip()
                choice = user_choice.lower()
                valid_ids = {str(item[0]) for item in items}

                if choice == "next":
                    if (current_page + 1) * 10 >= result["total_count"]:
                        print("No more items.")
                    else:
                        current_page += 1
                    continue

                if choice == "back":
                    if current_page == 0:
                        print("Already on first page.")
                    else:
                        current_page -= 1
                    continue

                if choice == "0":
                    return

                if choice in valid_ids:
                    selected_item = next(item for item in items if str(item[0]) == choice)
                    self.add_to_cart(selected_item)
                    continue

                print("Invalid input.")

            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as exc:
                print(f"Error: {exc}")
                continue

    def add_to_cart(self, item):
        title = item[1]
        for attempt in range(3):
            try:
                qty = input(f'Enter quantity for "{title}": ').strip()
                if qty == "":
                    raise ValueError

                quantity = int(qty)
                if quantity <= 0:
                    raise ValueError

                result = add_item_to_cart(self.id, item[0], quantity)
                if result["success"]:
                    print(result["message"])
                else:
                    print(result["message"])
                return

            except ValueError:
                print("Invalid quantity. Please enter a positive integer.")

        print("Add to cart cancelled.")

    def cart_menu(self):
        while True:
            try:
                result = get_cart(self.id)
                if not result["success"]:
                    print(result["message"])
                    return

                items = result["items"]
                if not items:
                    print("Your cart is empty.")
                    return

                print()
                print("=" * 49)
                print("YOUR CART")
                print("=" * 49)

                profile_result = getCustomerById(self.id)
                if profile_result["success"]:
                    customer = profile_result["customer"]
                    print(f"Customer: {customer.get('name') or self.id}")
                    print(f"Delivery Address: {customer.get('address') or 'Not set'}")

                for index, item in enumerate(items, start=1):
                    print(
                        f"{index}. {item['title']}   x{item['quantity']}   ₹{item['price']}   = ₹{item['subtotal']}"
                    )

                print("-" * 49)
                print(f"Cart Total: ₹{result['total']:.2f}")
                print(f"Total Items: {sum(item['quantity'] for item in items)}")
                print("-" * 49)
                print("1. Update quantity")
                print("2. Remove item")
                print("3. Back to main menu")

                choice = input("Enter choice: ").strip()
                if choice == "":
                    raise ValueError("empty")

                choice = int(choice)

                if choice == 1:
                    self.update_cart_quantity()
                elif choice == 2:
                    self.remove_cart_item()
                elif choice == 3:
                    return
                else:
                    print("Invalid choice. Please select a valid option.")

            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as exc:
                print(f"Error: {exc}")
                continue

    def update_cart_quantity(self):
        while True:
            try:
                cart_result = get_cart(self.id)
                if not cart_result["success"]:
                    print(cart_result["message"])
                    return

                items = cart_result["items"]
                if not items:
                    print("Your cart is empty.")
                    return

                item_number = input("Enter item number to update: ").strip()
                if item_number == "":
                    raise ValueError

                item_number = int(item_number)
                if item_number < 1 or item_number > len(items):
                    print("Invalid item number.")
                    return

                selected = items[item_number - 1]
                new_quantity = input(f"Enter new quantity for '{selected['title']}': ").strip()
                if new_quantity == "":
                    raise ValueError

                new_quantity_int = int(new_quantity)
                if new_quantity_int == 0:
                    confirm = input(f"Remove '{selected['title']}' from cart? (y/n): ").strip().lower()
                    if confirm != "y":
                        print("Removal cancelled.")
                        return
                    result = remove_cart_item(selected["cart_item_id"])
                    print(result["message"])
                    return

                if new_quantity_int < 0:
                    print("Invalid quantity. Please enter a positive integer.")
                    return

                result = update_cart_quantity(selected["cart_item_id"], new_quantity_int)
                print(result["message"])
                return

            except ValueError:
                print("Invalid item number or quantity.")
                return
            except Exception as exc:
                print(f"Error: {exc}")
                return

    def remove_cart_item(self):
        while True:
            try:
                cart_result = get_cart(self.id)
                if not cart_result["success"]:
                    print(cart_result["message"])
                    return

                items = cart_result["items"]
                if not items:
                    print("Your cart is empty.")
                    return

                item_number = input("Enter item number to remove: ").strip()
                if item_number == "":
                    raise ValueError

                item_number = int(item_number)
                if item_number < 1 or item_number > len(items):
                    print("Invalid item number.")
                    return

                selected = items[item_number - 1]
                confirm = input(f"Remove '{selected['title']}' from cart? (y/n): ").strip().lower()
                if confirm != "y":
                    print("Removal cancelled.")
                    return

                result = remove_cart_item(selected["cart_item_id"])
                print(result["message"])
                return

            except ValueError:
                print("Invalid item number.")
                return
            except Exception as exc:
                print(f"Error: {exc}")
                return
