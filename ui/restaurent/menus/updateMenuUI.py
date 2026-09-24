from services.menuServices.updateMenu import (
    getMenuForRestaurant,
    updateMenu as updateMenuService,
)


class updateMenuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def updateMenu(self):
        print()
        print("=" * 49)
        print("Update Menu")
        print("=" * 49)

        menu_id = input("Enter Menu ID to update: ").strip()

        if not menu_id:
            print("Menu ID cannot be empty.")
            return

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

        title = input(f"Title [{menu[1]}]: ").strip()
        description = input(f"Description [{menu[2]}]: ").strip()
        availability = input(f"Availability [1=Available, 0=Unavailable] [{menu[3]}]: ").strip()
        price = input(f"Price [{menu[4]}]: ").strip()
        nutrients = input(f"Nutrients [{menu[5]}]: ").strip()

        if not title:
            title = menu[1]
        if not description:
            description = menu[2]
        if not availability:
            availability = menu[3]
        if not price:
            price = menu[4]
        if not nutrients:
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
