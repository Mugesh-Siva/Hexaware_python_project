import unittest
import uuid

from database.setup import setupDatabase
from services.customerServices.browseItems import add_item_to_cart
from services.customerServices.customerAuthServices import createCustomer
from services.customerServices.orderService import place_order_from_cart
from services.menuServices.addMenu import addMenu
from services.restaurantServices.orderService import get_orders_for_restaurant, update_order_status
from services.restaurantServices.restaurantAuthServices import createRestaurant


class RestaurantOrderTests(unittest.TestCase):
    def setUp(self):
        setupDatabase()
        self.customer_id = f"customer_order_{uuid.uuid4().hex[:8]}"
        self.restaurant_id = f"restaurant_order_{uuid.uuid4().hex[:8]}"

        createCustomer("Order Customer", "Order Street", "+91 90001 23456", self.customer_id, f"{self.customer_id}@example.com", "Password@123")
        createRestaurant("Order Kitchen", "Kitchen Road", "+91 97777 66555", self.restaurant_id, f"{self.restaurant_id}@example.com", "Password@123")

        menu_result = addMenu(self.restaurant_id, "Noodles Bowl", "Fresh noodles", 250, "Carbs")
        self.menu_id = menu_result["menu_id"]
        add_item_to_cart(self.customer_id, self.menu_id, 2)

    def test_restaurant_can_see_order(self):
        place_order_from_cart(self.customer_id, "cash")
        result = get_orders_for_restaurant(self.restaurant_id)
        self.assertTrue(result["success"])

    def test_order_status_update(self):
        place_order_from_cart(self.customer_id, "cash")
        orders = get_orders_for_restaurant(self.restaurant_id)
        order_id = orders["orders"][0]["order_id"]
        result = update_order_status(order_id, self.restaurant_id, "cooked")
        self.assertTrue(result["success"])
