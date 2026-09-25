import unittest

from utils.validators import validate_card_number, validate_cvv, validate_expiry_date


class PaymentValidationTests(unittest.TestCase):
    def test_valid_card_number(self):
        ok, msg = validate_card_number("4242424242424242")
        self.assertTrue(ok, msg)

    def test_invalid_card_number(self):
        ok, _ = validate_card_number("1234")
        self.assertFalse(ok)

    def test_valid_expiry_date(self):
        ok, msg = validate_expiry_date("12/30")
        self.assertTrue(ok, msg)

    def test_expired_expiry_date(self):
        ok, _ = validate_expiry_date("01/20")
        self.assertFalse(ok)

    def test_valid_cvv(self):
        ok, msg = validate_cvv("123")
        self.assertTrue(ok, msg)

    def test_invalid_cvv(self):
        ok, _ = validate_cvv("12a")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
