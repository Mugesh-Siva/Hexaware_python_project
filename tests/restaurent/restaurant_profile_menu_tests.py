import unittest
import uuid

from database.setup import setupDatabase
from services.menuServices.addMenu import addMenu
from services.menuServices.deleteMenu import deleteMenu
from services.menuServices.listMenu import getMenusByRestaurant
from services.menuServices.updateMenu import updateMenu
from services.restaurantServices.restaurantAuthServices import createRestaurant, updateRestaurantProfile


class RestaurantProfileMenuTests(unittest.TestCase):
    def setUp(self):
        setupDatabase()
        self.restaurant_id = f"restaurant_menu_{uuid.uuid4().hex[:8]}"
        self.email = f"{self.restaurant_id}@example.com"
        createRestaurant("Menu Kitchen", "Kitchen Road", "+91 98777 65432", self.restaurant_id, self.email, "Password@123")

    def test_update_profile(self):
        result = updateRestaurantProfile(self.restaurant_id, "name", "Updated Kitchen")
        self.assertTrue(result["success"])

    def test_add_menu(self):
        result = addMenu(self.restaurant_id, "Paneer Wrap", "Good food", 180, "Protein")
        self.assertTrue(result["success"])

    def test_list_menu(self):
        addMenu(self.restaurant_id, "Paneer Wrap", "Good food", 180, "Protein")
        result = getMenusByRestaurant(self.restaurant_id)
        self.assertTrue(result["success"])

    def test_update_menu(self):
        menu_result = addMenu(self.restaurant_id, "Paneer Wrap", "Good food", 180, "Protein")
        menu_id = menu_result["menu_id"]
        result = updateMenu(self.restaurant_id, menu_id, "Paneer Wrap Deluxe", "Better food", 1, 210, "Protein")
        self.assertTrue(result["success"])

    def test_delete_menu(self):
        menu_result = addMenu(self.restaurant_id, "Paneer Wrap", "Good food", 180, "Protein")
        menu_id = menu_result["menu_id"]
        result = deleteMenu(self.restaurant_id, menu_id)
        self.assertTrue(result["success"])
