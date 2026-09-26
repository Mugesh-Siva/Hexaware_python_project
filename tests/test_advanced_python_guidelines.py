import pytest

from services.paymentServices.paymentService import CardPayment, CashPayment
from utils.input_helpers import (
    BaseAccount,
    CustomerAccount,
    OrderIterator,
    RestaurantAccount,
    build_order_report,
    format_choice_labels,
    generate_menu_titles,
    require_value,
    show_account_name,
)


class TestAdvancedPythonConcepts:
    def test_inheritance_and_encapsulation(self):
        customer = CustomerAccount("cust01", "Alice", "Main Road")
        restaurant = RestaurantAccount("rest01", "Hot Bite", "Market Street")

        assert customer.get_role_label() == "Customer"
        assert restaurant.get_role_label() == "Restaurant"
        assert customer.user_id == "cust01"
        assert customer.name == "Alice"

        with pytest.raises(ValueError):
            customer.user_id = "ab"

        with pytest.raises(ValueError):
            BaseAccount("ab", "x")

    @pytest.mark.parametrize("value", ["Burger", "Pizza", "Sandwich"])
    def test_lambda_and_sorting(self, value):
        labels = format_choice_labels([value])
        assert labels == [value.lower()]

    def test_args_kwargs_and_collections(self):
        report = build_order_report(
            {"title": "Burger", "quantity": 2, "price": 50},
            {"title": "Burger", "quantity": 1, "price": 50},
            {"title": "Pizza", "quantity": 1, "price": 80},
            restaurant="Hot Bite",
        )

        assert report["counts"]["Burger"] == 3
        assert report["totals"]["Burger"] == 150.0
        assert report["restaurant"] == "Hot Bite"

    def test_iterator_and_generator(self):
        items = [{"title": "Burger"}, {"title": "Pizza"}]
        iterator = OrderIterator(items)

        assert list(iterator) == items
        assert list(generate_menu_titles(items)) == ["Burger", "Pizza"]

    @pytest.mark.parametrize("name", ["alice", "bob"])
    def test_decorator_with_argument(self, name):
        assert show_account_name(name) == name.upper()

        with pytest.raises(ValueError):
            show_account_name("")

    def test_payment_polymorphism(self):
        payments = [CardPayment("1234567890123456", "12/29", "123"), CashPayment()]

        for payment in payments:
            result = payment.pay(50)
            assert result["success"] is True
            assert result["amount"] == 50.0

    @pytest.mark.parametrize("field_name, value", [("name", ""), ("email", "")])
    def test_required_value_decorator_raises(self, field_name, value):
        @require_value(field_name)
        def sample_function(**kwargs):
            return kwargs

        with pytest.raises(ValueError):
            sample_function(**{field_name: value})
