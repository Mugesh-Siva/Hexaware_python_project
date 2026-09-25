from services.menuServices.updateMenu import (
    getMenuForRestaurant,
    updateMenu as updateMenuService,
)
from utils.input_helpers import safe_decimal_input, safe_int_input, safe_text_input


class updateMenuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def updateMenu(self):
        print()
        print("=" * 49)
        print("Update Menu")
        print("=" * 49)

        while True:
            menu_id, error = safe_int_input(input("Enter Menu ID to update: ").strip(), field_name="Menu ID", minimum=1)
            if error:
                print(error)
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != "y":
                    return
                continue
            break

        loaded_menu = getMenuForRestaurant(self.id, menu_id)
        if not loaded_menu["success"]:
            print()
            print("=" * 49)
            print(loaded_menu["message"])
            print("=" * 49)
            return

        menu = loaded_menu["menu"]
        print()
        print("Current Menu Details")
        print("-" * 49)
        print("Menu ID     :", menu[0])
        print("Title       :", menu[1])
        print("Description :", menu[2])
        print("Availability:", "Available" if menu[3] else "Unavailable")
        print("Price       :", menu[4])
        print("Nutrients   :", menu[5])
        print("-" * 49)

        print()
        print("Enter new values.")
        print("Press Enter to keep the current value.")

        title_raw = input(f"Title [{menu[1]}]: ").strip()
        if title_raw:
            title, error = safe_text_input(title_raw, field_name="Title", min_length=2, max_length=100)
            if error:
                print(error)
                return
        else:
            title = menu[1]

        description_raw = input(f"Description [{menu[2]}]: ").strip()
        if description_raw:
            description, error = safe_text_input(description_raw, field_name="Description", min_length=0, max_length=300)
            if error:
                print(error)
                return
        else:
            description = menu[2]

        availability_raw = input(f"Availability [1=Available, 0=Unavailable] [{menu[3]}]: ").strip()
        if availability_raw:
            availability, error = safe_int_input(availability_raw, field_name="Availability", minimum=0, maximum=1, allow_zero=True)
            if error:
                print(error)
                return
        else:
            availability = menu[3]

        price_raw = input(f"Price [{menu[4]}]: ").strip()
        if price_raw:
            price, error = safe_decimal_input(price_raw, field_name="Price", minimum=0.01)
            if error:
                print(error)
                return
        else:
            price = menu[4]

        nutrients_raw = input(f"Nutrients [{menu[5]}]: ").strip()
        if nutrients_raw:
            nutrients, error = safe_text_input(nutrients_raw, field_name="Nutrients", min_length=0, max_length=500)
            if error:
                print(error)
                return
        else:
            nutrients = menu[5]

        result = updateMenuService(
            self.id,
            menu_id,
            title,
            description,
            availability,
            price,
            nutrients,
        )

        print()
        print("=" * 49)
        print(result["message"])
        print("=" * 49)
