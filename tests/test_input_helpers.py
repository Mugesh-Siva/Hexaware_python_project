import unittest

from utils.input_helpers import safe_choice_input, safe_decimal_input, safe_int_input


class InputHelperTests(unittest.TestCase):
    def test_safe_int_input_accepts_valid_number(self):
        value, error = safe_int_input("4", minimum=1, maximum=10)
        self.assertEqual(value, 4)
        self.assertIsNone(error)

    def test_safe_int_input_rejects_out_of_range(self):
        value, error = safe_int_input("15", minimum=1, maximum=10)
        self.assertIsNone(value)
        self.assertIn("at most", error)

    def test_safe_decimal_input_accepts_valid_number(self):
        value, error = safe_decimal_input("12.5", minimum=0.1)
        self.assertEqual(value, 12.5)
        self.assertIsNone(error)

    def test_safe_choice_input_accepts_valid_choice(self):
        value, error = safe_choice_input("2", valid_choices={"1", "2", "3"})
        self.assertEqual(value, "2")
        self.assertIsNone(error)

    def test_safe_choice_input_rejects_invalid_choice(self):
        value, error = safe_choice_input("9", valid_choices={"1", "2", "3"})
        self.assertIsNone(value)
        self.assertIn("Invalid choice", error)


if __name__ == "__main__":
    unittest.main()
