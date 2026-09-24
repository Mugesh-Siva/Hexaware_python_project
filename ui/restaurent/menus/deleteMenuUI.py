from services.menuServices.deleteMenu import (
    deleteMenu as deleteMenuService,
    getMenuForRestaurant,
)


class deleteMenuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def deleteMenu(self):
        print()
        print("=" * 49)
        print("Delete Menu")
        print("=" * 49)

        menu_id = input("Enter Menu ID to delete: ").strip()

        if not menu_id:
            print("Menu ID cannot be empty.")
            return

        menu_result = getMenuForRestaurant(self.id, menu_id)
        if not menu_result["success"]:
            print()
            print("=" * 49)
            print(menu_result["message"])
            print("=" * 49)
            return

        menu = menu_result["menu"]
        print()
        print("Menu ID:", menu[0])
        print("Title:", menu[1])

        confirm = input("Are you sure you want to delete this menu? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            return

        result = deleteMenuService(self.id, menu_id)

        print()
        print("=" * 49)
        print(result["message"])
        print("=" * 49)

