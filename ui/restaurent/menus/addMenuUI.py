from services.menuServices.addMenu import addMenu as addMenuService


class addMenuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def addMenu(self):
        print()
        print("=" * 49)
        print("Add Menu")
        print("=" * 49)

        title = input("Enter menu title: ").strip()
        description = input("Enter description: ").strip()
        price = input("Enter price: ").strip()
        nutrients = input("Enter nutrients: ").strip()

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
