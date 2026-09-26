import unittest
import uuid

from database.setup import setupDatabase
from services.restaurantServices.restaurantAuthServices import createRestaurant, getRestaurantById, loginRestaurant
from utils.validators import validate_email, validate_name, validate_contact, validate_password


class RestaurantAuthTests(unittest.TestCase):
    def setUp(self):
        setupDatabase()
        self.restaurant_id = f"restaurant_{uuid.uuid4().hex[:8]}"
        self.password = "Password@123"
        self.email = f"{self.restaurant_id}@example.com"
        createRestaurant("Bite House", "Food Street", "+91 99888 77666", self.restaurant_id, self.email, self.password)

    def test_name_validation(self):
        valid, message = validate_name("Bite House")
        self.assertTrue(valid)

    def test_email_validation(self):
        valid, message = validate_email("bitehouse@example.com")
        self.assertTrue(valid)

    def test_contact_validation(self):
        valid, message = validate_contact("+91 99888 77666")
        self.assertTrue(valid)

    def test_password_validation(self):
        valid, message = validate_password("Password@123")
        self.assertTrue(valid)

    def test_registration_success(self):
        new_id = f"restaurant_{uuid.uuid4().hex[:8]}"
        new_email = f"{new_id}@example.com"
        result = createRestaurant("Cafe Food", "Street 9", "+91 99000 11111", new_id, new_email, "Password@123")
        self.assertTrue(result["success"])

    def test_duplicate_id_blocked(self):
        result = createRestaurant("Bite House", "Food Street", "+91 99888 77666", self.restaurant_id, "bitehouse@example.com", self.password)
        self.assertFalse(result["success"])

    def test_login_success(self):
        self.assertTrue(loginRestaurant(self.restaurant_id, self.password))

    def test_wrong_password_fails(self):
        self.assertFalse(loginRestaurant(self.restaurant_id, "wrongpassword"))

    def test_get_profile(self):
        result = getRestaurantById(self.restaurant_id)
        self.assertTrue(result["success"])
