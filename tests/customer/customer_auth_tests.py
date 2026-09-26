import unittest
import uuid

from database.setup import setupDatabase
from services.customerServices.customerAuthServices import createCustomer, getCustomerById, loginCustomer
from utils.validators import validate_email, validate_name, validate_contact


class CustomerAuthTests(unittest.TestCase):
    def setUp(self):
        setupDatabase()
        self.customer_id = f"customer_{uuid.uuid4().hex[:8]}"
        self.password = "Password@123"
        self.email = f"{self.customer_id}@example.com"
        createCustomer("Alice", "Main Street", "+91 98765 43210", self.customer_id, self.email, self.password)

    def test_name_validation(self):
        valid, message = validate_name("Alice")
        self.assertTrue(valid)

    def test_email_validation(self):
        valid, message = validate_email("alice@example.com")
        self.assertTrue(valid)

    def test_contact_validation(self):
        valid, message = validate_contact("+91 98765 43210")
        self.assertTrue(valid)

    def test_registration_success(self):
        new_id = f"customer_{uuid.uuid4().hex[:8]}"
        new_email = f"{new_id}@example.com"
        result = createCustomer("Bob", "Road 2", "+91 90000 11111", new_id, new_email, "Password@123")
        self.assertTrue(result["success"])

    def test_duplicate_id_blocked(self):
        result = createCustomer("Alice", "Main Street", "+91 98765 43210", self.customer_id, "alice@example.com", self.password)
        self.assertFalse(result["success"])

    def test_login_success(self):
        self.assertTrue(loginCustomer(self.customer_id, self.password))

    def test_wrong_password_fails(self):
        self.assertFalse(loginCustomer(self.customer_id, "wrongpassword"))

    def test_get_profile(self):
        result = getCustomerById(self.customer_id)
        self.assertTrue(result["success"])
