from services.menuServices.listMenu import getMenusByRestaurant
from services.restaurantServices.restaurantAuthServices import getRestaurantById


class displayAllMenuUI:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def displayAllMenus(self):
        print()
        print("=" * 49)
        print("LIST OF ALL MENUS")
        print("=" * 49)

        profile_result = getRestaurantById(self.id)
        restaurant_name = self.id
        if profile_result["success"]:
            restaurant_name = profile_result["restaurant"].get("name") or self.id

        print(f"Restaurant: {restaurant_name}")

        result = getMenusByRestaurant(self.id)
        if not result["success"]:
            print(result["message"])
            return

        menus = result["menus"]
        if not menus:
            print("No menu found for this restaurant.")
            return

        print(f"Total menu items: {len(menus)}")
        print("-" * 49)

        for menu in menus:
            menu_id, title, description, availability, price, nutrients, created_at = menu
            status = "Available" if availability == 1 else "Unavailable"
            print()
            print(f"Menu ID     : {menu_id}")
            print(f"Title       : {title}")
            print(f"Description : {description}")
            print(f"Price       : ₹{price}")
            print(f"Status      : {status}")
            print(f"Nutrients   : {nutrients or 'Not specified'}")
            print(f"Created At  : {created_at}")
            print("-" * 49)
