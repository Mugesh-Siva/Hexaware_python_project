from services.menuServices.listMenu import getMenusByRestaurant


class displayAllMenuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def displayAllMenus(self):
        print()
        print("=" * 49)
        print("List of all Menus of your restaurant")
        print("=" * 49)

        result = getMenusByRestaurant(self.id)
        if not result["success"]:
            print(result["message"])
            return

        menus = result["menus"]
        if not menus:
            print("No menu found for this restaurant.")
            return

        for menu in menus:
            print()
            print("Menu ID     :", menu[0])
            print("Title       :", menu[1])
            print("Description :", menu[2])
            print("Availability:", "Available" if menu[3] else "Unavailable")
            print("Price       :", menu[4])
            print("Nutrients   :", menu[5])
            print("Created At  :", menu[6])
            print("-" * 49)
