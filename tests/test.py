import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(".."))

from tests.customer.customer_auth_tests import CustomerAuthTests
from tests.customer.customer_profile_balance_tests import CustomerProfileBalanceTests
from tests.customer.customer_cart_order_tests import CustomerCartOrderTests
from tests.restaurent.restaurant_auth_tests import RestaurantAuthTests
from tests.restaurent.restaurant_profile_menu_tests import RestaurantProfileMenuTests
from tests.restaurent.restaurant_order_tests import RestaurantOrderTests


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(CustomerAuthTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(CustomerProfileBalanceTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(CustomerCartOrderTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(RestaurantAuthTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(RestaurantProfileMenuTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(RestaurantOrderTests))

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)

    if result.failures or result.errors:
        raise SystemExit(1)
