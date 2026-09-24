import ui.restaurent.menus.menuUI as menu
class restaurentHome:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def restUI(self):
        print("=" * 49)
        print("Welcome To Restaurant Home")
        print("=" * 49)

        while True:
            print()
            print("1. Menus")
            print("2. Orders")
            print("3. Profile")
            print("4. Logout")

            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    print()
                    print("Menus")
                    # Call menu function here
                    restMenu=menu.menuUI(self.id,self.role)
                    restMenu.menuList()

                case "2":
                    print()
                    print("Orders")
                    # Call orders function here

                case "3":
                    print()
                    print("Profile")
                    # Call profile function here

                case "4":
                    print()
                    print("Logging out...")
                    break

                case _:
                    print()
                    print("Invalid choice. Please try again.")