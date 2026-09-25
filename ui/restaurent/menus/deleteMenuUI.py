from services.menuServices.deleteMenu import (
    deleteMenu as deleteMenuService,
    getMenuForRestaurant,
)
from utils.input_helpers import confirm_action, safe_int_input


class deleteMenuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def deleteMenu(self):
        print()
        print("=" * 49)
        print("Delete Menu")
        print("=" * 49)

        while True:
            menu_id, error = safe_int_input(input("Enter Menu ID to delete: ").strip(), field_name="Menu ID", minimum=1)
            if error:
                print(error)
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != "y":
                    return
                continue
            break

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

        confirm, error = confirm_action(input("Are you sure you want to delete this menu? (y/n): ").strip())
        if error:
            print(error)
            return
        if not confirm:
            print("Delete cancelled.")
            return

        result = deleteMenuService(self.id, menu_id)

        print()
        print("=" * 49)
        print(result["message"])
        print("=" * 49)

