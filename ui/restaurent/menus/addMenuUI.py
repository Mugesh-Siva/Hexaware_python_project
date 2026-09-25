from services.menuServices.addMenu import addMenu as addMenuService
from utils.input_helpers import safe_decimal_input, safe_text_input


class addMenuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def addMenu(self):
        print()
        print("=" * 49)
        print("Add Menu")
        print("=" * 49)

        while True:
            title, error = safe_text_input(
                input("Enter menu title: ").strip(),
                field_name="Menu title",
                min_length=2,
                max_length=100,
            )
            if error:
                print(error)
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != "y":
                    return
                continue
            break

        while True:
            description, error = safe_text_input(
                input("Enter description: ").strip(),
                field_name="Description",
                min_length=0,
                max_length=300,
            )
            if error:
                print(error)
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != "y":
                    return
                continue
            break

        while True:
            price_raw = input("Enter price: ").strip()
            price, error = safe_decimal_input(price_raw, field_name="Price", minimum=0.01)
            if error:
                print(error)
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != "y":
                    return
                continue
            break

        while True:
            nutrients, error = safe_text_input(
                input("Enter nutrients: ").strip(),
                field_name="Nutrients",
                min_length=0,
                max_length=500,
            )
            if error:
                print(error)
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != "y":
                    return
                continue
            break

        result = addMenuService(
            self.id,
            title,
            description,
            price,
            nutrients,
            self.role,
        )

        print()
        print("=" * 49)
        print(result["message"])
        if result.get("menu_id"):
            print("Menu ID:", result["menu_id"])
        print("=" * 49)
