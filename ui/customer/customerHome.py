from services.customerServices.balanceService import add_hotbite_balance, get_hotbite_balance
from services.customerServices.browseItems import add_item_to_cart, get_menu_page, search_menu_items
from services.customerServices.cart import get_cart, remove_cart_item, update_cart_quantity
from services.customerServices.customerAuthServices import getCustomerById, updateCustomerProfile
from services.customerServices.orderService import get_checkout_summary, get_customer_orders, place_order_from_cart
from services.paymentServices.paymentService import (
    process_card_payment,
    process_cash_payment,
    process_hotbite_payment,
)
from utils.custom_exceptions import PaymentError, ValidationError
from utils.input_helpers import confirm_action, safe_choice_input, safe_int_input, safe_text_input
from utils.validators import (
    validate_address,
    validate_amount,
    validate_card_number,
    validate_contact,
    validate_cvv,
    validate_email,
    validate_expiry_date,
    validate_name,
)


class customerHome:
    def __init__(self, id, role):
        self.id = id
        self.role = role
        self.search_cache_term = ""

    def print_customer_header(self):
        profile_result = getCustomerById(self.id)
        name = self.id
        address = "Not set"
        contact = "Not set"
        balance = 0.0

        if profile_result["success"]:
            customer = profile_result["customer"]
            name = customer.get("name") or self.id
            address = customer.get("address") or "Not set"
            contact = customer.get("contact_number") or "Not set"
            balance = float(customer.get("balance") or 0.0)

        print()
        print("=" * 49)
        print(f"WELCOME {name.upper()}")
        print("=" * 49)
        print(f"Customer ID: {self.id}")
        print(f"Delivery Address: {address}")
        print(f"Contact Number: {contact}")
        print(f"Hotbite Balance: ₹{balance:.2f}")
        print("-" * 49)

    def start(self):
        self.print_customer_header()
        while True:
            try:
                print()
                print("=" * 49)
                print("CUSTOMER DASHBOARD")
                print("=" * 49)
                print("1. Search Menu")
                print("2. Browse Items")
                print("3. Cart")
                print("4. Orders")
                print("5. Profile")
                print("6. Logout")
                print("=" * 49)

                choice, error = safe_choice_input(input("Enter your choice (1-6): ").strip(), {"1", "2", "3", "4", "5", "6"}, field_name="Choice")
                if error:
                    print(error)
                    continue

                if choice == "1":
                    self.search_menu()
                elif choice == "2":
                    self.browse_items()
                elif choice == "3":
                    self.cart_menu()
                elif choice == "4":
                    self.order_history_menu()
                elif choice == "5":
                    self.profile_menu()
                elif choice == "6":
                    print("Logging out...")
                    return

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
            balance = float(customer.get("balance") or 0.0)
            print()
            print("=" * 49)
            print("PROFILE")
            print("=" * 49)
            print(f"Customer ID: {customer.get('id', self.id)}")
            print(f"Name: {customer.get('name', 'Not set')}")
            print(f"Address: {customer.get('address', 'Not set')}")
            print(f"Contact Number: {customer.get('contact_number', 'Not set')}")
            print(f"Recovery Email: {customer.get('recovery_email', 'Not set')}")
            print(f"Hotbite Balance: ₹{balance:.2f}")
            print("-" * 49)
            print("1. Edit name")
            print("2. Edit address")
            print("3. Edit contact number")
            print("4. Edit recovery email")
            print("5. Add Hotbite balance")
            print("6. Back to main menu")
            print("-" * 49)

            choice, error = safe_choice_input(input("Enter your choice (1-6): ").strip(), {"1", "2", "3", "4", "5", "6"}, field_name="Choice")
            if error:
                print(error)
                continue

            if choice == "1":
                self.edit_profile_field("name", "Name", validate_name)
            elif choice == "2":
                self.edit_profile_field("address", "Address", validate_address)
            elif choice == "3":
                self.edit_profile_field("contact_number", "Contact Number", validate_contact)
            elif choice == "4":
                self.edit_profile_field("recovery_email", "Recovery Email", validate_email)
            elif choice == "5":
                self.add_hotbite_balance()
            elif choice == "6":
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

    def search_menu(self):
        current_page = 0

        while True:
            try:
                print()
                print("-" * 49)
                print("SEARCH MENU")
                print("-" * 49)
                print("Type 'next' for next page")
                print("Type 'back' for previous page")
                print("Type item ID to add it to cart")
                print("Type '0' to exit this search menu")
                print("Type 'new' to search a different item")
                print("-" * 49)

                if current_page == 0:
                    search_term = input("Enter menu name to search: ").strip()
                    if search_term.lower() in {"0", "exit", "cancel", "back"}:
                        print("Exiting search menu.")
                        return
                    cleaned_term, error = safe_text_input(search_term, field_name="Search term", min_length=1, max_length=50)
                    if error:
                        print(error)
                        continue
                    result = search_menu_items(cleaned_term, current_page, 10)
                else:
                    result = search_menu_items(self.search_cache_term, current_page, 10)

                if not result["success"]:
                    print(result["message"])
                    return

                items = result["items"]
                if not items:
                    search_value = result.get("search_term", "your search")
                    print(f"No menu found for '{search_value}'.")
                    retry = input("Search again? (y/n): ").strip().lower()
                    if retry not in {"y", "yes"}:
                        return
                    current_page = 0
                    self.search_cache_term = ""
                    continue

                self.search_cache_term = result.get("search_term", self.search_cache_term)
                print()
                print("-" * 49)
                print(f"SEARCH RESULTS FOR: {self.search_cache_term.upper()}")
                print("-" * 49)
                for item in items:
                    menu_id, title, description, price, nutrients, availability, user_id = item
                    status = "Available" if availability == 1 else "Unavailable"
                    print(f"{menu_id}. {title} - ₹{price}")
                    print(f"   {description}")
                    print(f"   Nutrients: {nutrients or 'Not specified'} | Status: {status}")
                print("-" * 49)

                user_choice = input("Enter choice: ").strip()
                choice = user_choice.lower()
                valid_ids = {str(item[0]) for item in items}

                if choice == "next":
                    if (current_page + 1) * 10 >= result["total_count"]:
                        print("No more matching items.")
                    else:
                        current_page += 1
                    continue

                if choice == "back":
                    if current_page == 0:
                        print("Already on first search page.")
                    else:
                        current_page -= 1
                    continue

                if choice in {"0", "exit", "cancel"}:
                    print("Exiting search menu.")
                    return

                if choice == "new":
                    current_page = 0
                    self.search_cache_term = ""
                    continue

                if choice in valid_ids:
                    selected_item = next(item for item in items if str(item[0]) == choice)
                    self.add_to_cart(selected_item)
                    continue

                print("Invalid input. Please use item ID, next, back, new, or 0 to exit.")

            except ValueError:
                print("Invalid input. Please enter a valid menu search choice.")
            except Exception as exc:
                print(f"Error: {exc}")
                continue

    def add_to_cart(self, item):
        title = item[1]
        for attempt in range(3):
            try:
                qty = input(f'Enter quantity for "{title}": ').strip()
                if qty.lower() in {"0", "cancel", "back"}:
                    print("Add to cart cancelled.")
                    return

                quantity, error = safe_int_input(qty, field_name="Quantity", minimum=1)
                if error:
                    print(error)
                    continue

                result = add_item_to_cart(self.id, item[0], quantity)
                print(result["message"])
                return

            except Exception as exc:
                print(f"Error while adding to cart: {exc}")

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
                print("4. Proceed to checkout")
                print("-" * 49)

                choice, error = safe_choice_input(input("Enter choice: ").strip(), {"1", "2", "3", "4"}, field_name="Choice")
                if error:
                    print(error)
                    continue

                if choice == "1":
                    self.update_cart_quantity()
                elif choice == "2":
                    self.remove_cart_item()
                elif choice == "3":
                    return
                elif choice == "4":
                    self.checkout_flow()
                    return

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

                item_number_raw = input("Enter item number to update: ").strip()
                if item_number_raw.lower() in {"0", "cancel", "back"}:
                    print("Update cancelled.")
                    return

                item_number, error = safe_int_input(item_number_raw, field_name="Item number", minimum=1, maximum=len(items))
                if error:
                    print(error)
                    return

                selected = items[item_number - 1]
                new_quantity_raw = input(f"Enter new quantity for '{selected['title']}': ").strip()
                if new_quantity_raw.lower() in {"0", "cancel", "back"}:
                    print("Update cancelled.")
                    return
                if new_quantity_raw.lower() in {"remove", "delete"}:
                    confirm, error = confirm_action(input(f"Remove '{selected['title']}' from cart? (y/n): ").strip())
                    if error:
                        print(error)
                        return
                    if not confirm:
                        print("Removal cancelled.")
                        return
                    result = remove_cart_item(selected["cart_item_id"])
                    print(result["message"])
                    return

                new_quantity_int, error = safe_int_input(new_quantity_raw, field_name="Quantity", minimum=1)
                if error:
                    print(error)
                    return

                result = update_cart_quantity(selected["cart_item_id"], new_quantity_int)
                print(result["message"])
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

                item_number_raw = input("Enter item number to remove: ").strip()
                if item_number_raw.lower() in {"0", "cancel", "back"}:
                    print("Removal cancelled.")
                    return

                item_number, error = safe_int_input(item_number_raw, field_name="Item number", minimum=1, maximum=len(items))
                if error:
                    print(error)
                    return

                selected = items[item_number - 1]
                confirm, error = confirm_action(input(f"Remove '{selected['title']}' from cart? (y/n): ").strip())
                if error:
                    print(error)
                    return
                if not confirm:
                    print("Removal cancelled.")
                    return

                result = remove_cart_item(selected["cart_item_id"])
                print(result["message"])
                return

            except Exception as exc:
                print(f"Error: {exc}")
                return

    def collect_card_details(self):
        while True:
            try:
                card_number = input("Enter card number (16 digits) or 0 to cancel: ").strip()
                if card_number.lower() in {"0", "cancel", "back"}:
                    raise ValidationError("Card payment cancelled.")
                valid, message = validate_card_number(card_number)
                if not valid:
                    print(message)
                    continue
                break
            except ValidationError as exc:
                print(exc)
                raise
            except Exception as exc:
                print(f"Card number error: {exc}")
                raise

        while True:
            try:
                expiry_date = input("Enter expiry date (MM/YY) or 0 to cancel: ").strip()
                if expiry_date.lower() in {"0", "cancel", "back"}:
                    raise ValidationError("Card payment cancelled.")
                valid, message = validate_expiry_date(expiry_date)
                if not valid:
                    print(message)
                    continue
                break
            except ValidationError as exc:
                print(exc)
                raise
            except Exception as exc:
                print(f"Expiry date error: {exc}")
                raise

        while True:
            try:
                cvv = input("Enter CVV or 0 to cancel: ").strip()
                if cvv.lower() in {"0", "cancel", "back"}:
                    raise ValidationError("Card payment cancelled.")
                valid, message = validate_cvv(cvv)
                if not valid:
                    print(message)
                    continue
                break
            except ValidationError as exc:
                print(exc)
                raise
            except Exception as exc:
                print(f"CVV error: {exc}")
                raise

        return {
            "card_number": card_number,
            "expiry_date": expiry_date,
            "cvv": cvv,
        }

    def add_hotbite_balance(self):
        while True:
            try:
                print()
                print("=" * 49)
                print("TOP-UP HOTBITE BALANCE")
                print("=" * 49)
                amount = input("Enter amount to add or 0 to cancel: ").strip()
                if amount.lower() in {"0", "cancel", "back"}:
                    print("Top-up cancelled.")
                    return
                valid, message = validate_amount(amount)
                if not valid:
                    print(message)
                    retry, error = confirm_action(input("Try again? (y/n): ").strip())
                    if error:
                        print(error)
                        return
                    if not retry:
                        return
                    continue

                payment_type, error = safe_choice_input(input("Choose payment method:\n1. Card\n2. Cash\n0. Cancel\nEnter choice: ").strip(), {"0", "1", "2"}, field_name="Choice")
                if error:
                    print(error)
                    retry, confirm_error = confirm_action(input("Try again? (y/n): ").strip())
                    if confirm_error:
                        print(confirm_error)
                        return
                    if not retry:
                        return
                    continue

                if payment_type == "0":
                    print("Top-up cancelled.")
                    return

                if payment_type == "1":
                    try:
                        card_data = self.collect_card_details()
                    except ValidationError:
                        return
                    payment_result = process_card_payment(amount, card_data["card_number"], card_data["expiry_date"], card_data["cvv"])
                    if not payment_result["success"]:
                        print(payment_result["message"])
                        retry, confirm_error = confirm_action(input("Try again? (y/n): ").strip())
                        if confirm_error:
                            print(confirm_error)
                            return
                        if not retry:
                            return
                        continue

                    balance_result = add_hotbite_balance(self.id, amount)
                    print(balance_result["message"])
                    return

                if payment_type == "2":
                    payment_result = process_cash_payment(amount)
                    if not payment_result["success"]:
                        print(payment_result["message"])
                        return

                    balance_result = add_hotbite_balance(self.id, amount)
                    print(balance_result["message"])
                    return

                print("Invalid payment choice.")
            except Exception as exc:
                print(f"Error in Hotbite top-up: {exc}")
                return

    def checkout_flow(self):
        try:
            summary = get_checkout_summary(self.id)
            if not summary["success"]:
                print(summary["message"])
                return

            items = summary["items"]
            total = float(summary["total"])

            print()
            print("=" * 49)
            print("CHECKOUT")
            print("=" * 49)
            print("Your order summary:")
            for index, item in enumerate(items, start=1):
                print(f"{index}. {item['title']} x{item['quantity']} @ ₹{item['price']} = ₹{item['subtotal']:.2f}")
            print("-" * 49)
            print(f"TOTAL: ₹{total:.2f}")
            print("-" * 49)

            confirm = input("Press Enter to continue to payment, or type 0 to cancel: ").strip()
            if confirm in {"0", "cancel", "back"}:
                print("Checkout cancelled.")
                return

            while True:
                print("Payment options:")
                print("1. Card or Cash")
                print("2. Hotbite balance")
                print("0. Cancel")
                payment_choice, error = safe_choice_input(input("Select payment option: ").strip(), {"0", "1", "2"}, field_name="Choice")
                if error:
                    print(error)
                    retry, retry_error = confirm_action(input("Try again? (y/n): ").strip())
                    if retry_error:
                        print(retry_error)
                        return
                    if not retry:
                        return
                    continue

                if payment_choice == "0":
                    print("Checkout cancelled.")
                    return

                if payment_choice == "2":
                    balance = get_hotbite_balance(self.id)
                    print(f"Your Hotbite balance: ₹{balance:.2f}")
                    if balance < total:
                        print("Insufficient Hotbite balance.")
                        option, option_error = confirm_action(input("Would you like to add balance now? (y/n): ").strip())
                        if option_error:
                            print(option_error)
                            return
                        if option:
                            self.add_hotbite_balance()
                            balance = get_hotbite_balance(self.id)
                            if balance < total:
                                print("You still do not have enough balance. Checkout stopped.")
                                return
                        else:
                            print("Checkout stopped.")
                            return

                    payment_result = process_hotbite_payment(self.id, total)
                    if not payment_result["success"]:
                        print(payment_result["message"])
                        return

                    order_result = place_order_from_cart(self.id, "hotbite", {"total": total})
                    if not order_result["success"]:
                        print(order_result["message"])
                        return

                    print("=" * 49)
                    print(order_result["message"])
                    print(f"Order total: ₹{total:.2f}")
                    print(f"Payment mode: Hotbite balance")
                    print("=" * 49)
                    return

                if payment_choice == "1":
                    method_choice, method_error = safe_choice_input(input("Choose payment method:\n1. Card\n2. Cash\n0. Cancel\nEnter choice: ").strip(), {"0", "1", "2"}, field_name="Choice")
                    if method_error:
                        print(method_error)
                        continue
                    if method_choice == "0":
                        print("Checkout cancelled.")
                        return
                    if method_choice == "1":
                        try:
                            card_data = self.collect_card_details()
                        except ValidationError:
                            return
                        payment_result = process_card_payment(total, card_data["card_number"], card_data["expiry_date"], card_data["cvv"])
                        if not payment_result["success"]:
                            print(payment_result["message"])
                            retry, retry_error = confirm_action(input("Try another card? (y/n): ").strip())
                            if retry_error:
                                print(retry_error)
                                return
                            if not retry:
                                return
                            continue
                        payment_mode = "Card"
                    elif method_choice == "2":
                        payment_result = process_cash_payment(total)
                        if not payment_result["success"]:
                            print(payment_result["message"])
                            return
                        payment_mode = "Cash"

                    order_result = place_order_from_cart(self.id, payment_mode.lower(), {"total": total})
                    if not order_result["success"]:
                        print(order_result["message"])
                        return

                    print("=" * 49)
                    print(order_result["message"])
                    print(f"Order total: ₹{total:.2f}")
                    print(f"Payment mode: {payment_mode}")
                    print("=" * 49)
                    return

                print("Invalid payment option. Please choose 1, 2, or 0.")

        except PaymentError as exc:
            print(exc)
        except ValidationError as exc:
            print(exc)
        except Exception as exc:
            print(f"Checkout error: {exc}")

    def order_history_menu(self):
        try:
            result = get_customer_orders(self.id)
            if not result["success"]:
                print(result["message"])
                return

            orders = result["orders"]
            if not orders:
                print("No orders found yet.")
                return

            print()
            print("=" * 49)
            print("YOUR ORDERS")
            print("=" * 49)

            for order in orders:
                print(f"Order ID: {order['order_id']}")
                print(f"Status: {order['status']}")
                print(f"Date: {order['created_at']}")
                print("Items:")
                for item in order["items"]:
                    print(f"  - {item['title']} x{item['quantity']} @ ₹{item['price_at_order']:.2f}")
                print(f"Total: ₹{order['total_price']:.2f}")
                print("-" * 49)

        except Exception as exc:
            print(f"Error while loading orders: {exc}")
