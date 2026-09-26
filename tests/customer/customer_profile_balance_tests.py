import unittest
import uuid

from database.setup import setupDatabase
from services.customerServices.balanceService import add_hotbite_balance, deduct_hotbite_balance, get_hotbite_balance
from services.customerServices.customerAuthServices import createCustomer, updateCustomerProfile


class CustomerProfileBalanceTests(unittest.TestCase):
    def setUp(self):
        setupDatabase()
        self.customer_id = f"customer_profile_{uuid.uuid4().hex[:8]}"
        self.email = f"{self.customer_id}@example.com"
        createCustomer("Maya", "Street 8", "+91 90000 11111", self.customer_id, self.email, "Password@123")

    def test_update_name(self):
        result = updateCustomerProfile(self.customer_id, "name", "Maya New Name")
        self.assertTrue(result["success"])

    def test_update_address(self):
        result = updateCustomerProfile(self.customer_id, "address", "Updated Street 99")
        self.assertTrue(result["success"])

    def test_invalid_field_fails(self):
        result = updateCustomerProfile(self.customer_id, "password", "newpass")
        self.assertFalse(result["success"])

    def test_add_balance(self):
        before = get_hotbite_balance(self.customer_id)
        result = add_hotbite_balance(self.customer_id, 150)
        after = get_hotbite_balance(self.customer_id)
        self.assertTrue(result["success"])
        self.assertGreater(after, before)

    def test_deduct_balance(self):
        add_hotbite_balance(self.customer_id, 50)
        before = get_hotbite_balance(self.customer_id)
        result = deduct_hotbite_balance(self.customer_id, 25)
        after = get_hotbite_balance(self.customer_id)
        self.assertTrue(result["success"])
        self.assertLess(after, before)

    def test_insufficient_balance(self):
        result = deduct_hotbite_balance(self.customer_id, 9999)
        self.assertFalse(result["success"])
