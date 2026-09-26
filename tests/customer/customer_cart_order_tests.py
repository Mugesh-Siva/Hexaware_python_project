import unittest
import uuid

from database.setup import setupDatabase
from services.customerServices.browseItems import add_item_to_cart, get_menu_page
from services.customerServices.customerAuthServices import createCustomer
from services.customerServices.orderService import get_checkout_summary, place_order_from_cart
from services.menuServices.addMenu import addMenu
from services.restaurantServices.restaurantAuthServices import createRestaurant


class CustomerCartOrderTests(unittest.TestCase):
    def setUp(self):
        setupDatabase()
        self.customer_id = f"customer_cart_{uuid.uuid4().hex[:8]}"
        self.restaurant_id = f"restaurant_cart_{uuid.uuid4().hex[:8]}"

        createCustomer("Cart Buyer", "Cart Street", "+91 91111 22222", self.customer_id, f"{self.customer_id}@example.com", "Password@123")
        createRestaurant("Cart Kitchen", "Kitchen Street", "+91 92222 33333", self.restaurant_id, f"{self.restaurant_id}@example.com", "Password@123")

        result = addMenu(self.restaurant_id, "Crispy Burger", "Fresh burger", 120.0, "Protein")
        self.menu_id = result["menu_id"]

    def test_add_to_cart(self):
        result = add_item_to_cart(self.customer_id, self.menu_id, 2)
        self.assertTrue(result["success"])

    def test_menu_page(self):
        result = get_menu_page(0, 10)
        self.assertTrue(result["success"])

    def test_checkout(self):
        add_item_to_cart(self.customer_id, self.menu_id, 2)
        result = get_checkout_summary(self.customer_id)
        self.assertTrue(result["success"])

    def test_place_order(self):
        add_item_to_cart(self.customer_id, self.menu_id, 2)
        result = place_order_from_cart(self.customer_id, "cash")
        self.assertTrue(result["success"])
