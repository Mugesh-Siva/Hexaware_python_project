import ui.restaurent.menus.addMenuUI as addMenu
import ui.restaurent.menus.deleteMenuUI as deleteMenu
import ui.restaurent.menus.displayAllMenuUI as displayAllMenu
import ui.restaurent.menus.updateMenuUI as updateMenu
from utils.input_helpers import safe_choice_input


class menuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def menuList(self):
        while True:
            print()
            print("=" * 49)
            print("Menu Management")
            print("=" * 49)

            print("1. Add Menu")
            print("2. Update Menu")
            print("3. Delete Menu")
            print("4. View all Menus")
            print("5. Exit to Main Menu")

            choice, error = safe_choice_input(input("Enter your choice: ").strip(), {"1", "2", "3", "4", "5"}, field_name="Choice")
            if error:
                print(error)
                continue

            if choice == "1":
                print()
                print("Add Menu")
                add = addMenu.addMenuUI(self.id, self.role)
                add.addMenu()

            elif choice == "2":
                print()
                print("Update Menu")
                update = updateMenu.updateMenuUI(self.id, self.role)
                update.updateMenu()

            elif choice == "3":
                print()
                print("Delete Menu")
                delete = deleteMenu.deleteMenuUI(self.id, self.role)
                delete.deleteMenu()

            elif choice == "4":
                print()
                display = displayAllMenu.displayAllMenuUI(self.id, self.role)
                display.displayAllMenus()

            elif choice == "5":
                print()
                print("Returning to Main Menu...")
                break