import re
from collections import Counter, defaultdict
from functools import wraps


def safe_text_input(raw_value, field_name="Value", min_length=1, max_length=None, pattern=None):
    if raw_value is None:
        return None, f"{field_name} is required."

    text = str(raw_value).strip()
    if len(text) < min_length:
        return None, f"{field_name} cannot be empty."

    if max_length is not None and len(text) > max_length:
        return None, f"{field_name} is too long. Maximum {max_length} characters allowed."

    if pattern is not None and not re.fullmatch(pattern, text):
        return None, f"{field_name} format is invalid."

    return text, None


def safe_choice_input(raw_value, valid_choices, field_name="Choice"):
    if raw_value is None:
        return None, f"{field_name} is required."

    text = str(raw_value).strip()
    if not text:
        return None, f"{field_name} cannot be empty."

    normalized = text.lower()
    valid = {str(choice).lower() for choice in valid_choices}

    if normalized not in valid:
        return None, f"Invalid {field_name.lower()}. Please select a valid option."

    return normalized, None


def safe_int_input(raw_value, field_name="Value", minimum=None, maximum=None, allow_zero=False):
    if raw_value is None:
        return None, f"{field_name} is required."

    text = str(raw_value).strip()
    if text == "":
        return None, f"{field_name} cannot be empty."

    try:
        value = int(text)
    except ValueError:
        return None, f"{field_name} must be a valid integer."

    if value == 0 and not allow_zero:
        return None, f"{field_name} must be greater than 0."

    if minimum is not None and value < minimum:
        return None, f"{field_name} must be at least {minimum}."

    if maximum is not None and value > maximum:
        return None, f"{field_name} must be at most {maximum}."

    return value, None


def safe_decimal_input(raw_value, field_name="Value", minimum=0.0, maximum=None, allow_zero=False):
    if raw_value is None:
        return None, f"{field_name} is required."

    text = str(raw_value).strip()
    if text == "":
        return None, f"{field_name} cannot be empty."

    try:
        value = float(text)
    except ValueError:
        return None, f"{field_name} must be a valid number."

    if value == 0 and not allow_zero:
        return None, f"{field_name} must be greater than 0."

    if value < minimum:
        return None, f"{field_name} must be at least {minimum}."

    if maximum is not None and value > maximum:
        return None, f"{field_name} must be at most {maximum}."

    return value, None


def confirm_action(raw_value, field_name="Confirmation"):
    if raw_value is None:
        return False, f"{field_name} is required."

    text = str(raw_value).strip().lower()
    if text in {"y", "yes"}:
        return True, None
    if text in {"n", "no"}:
        return False, None
    return False, "Please enter 'y' for yes or 'n' for no."


# Advanced Python concepts used in the same app flow
# 1. Decorators (one with arguments)
def log_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{action_name}: {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_value(field_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = kwargs.get(field_name)
            if value is None:
                parameter_names = func.__code__.co_varnames[: func.__code__.co_argcount]
                if field_name in parameter_names:
                    index = parameter_names.index(field_name)
                    if index < len(args):
                        value = args[index]
                if value is None:
                    raise ValueError(f"{field_name} cannot be empty.")

            if str(value).strip() == "":
                raise ValueError(f"{field_name} cannot be empty.")
            return func(*args, **kwargs)

        return wrapper

    return decorator


# 2. Lambda + map/filter/sorted
@log_action("Menu labels prepared")
def format_choice_labels(items):
    labels = list(map(lambda item: str(item).strip().lower(), items))
    return sorted(labels)


# 3. *args and **kwargs
@log_action("Order summary created")
def build_order_report(*items, **extra):
    totals = defaultdict(float)
    counts = Counter()

    for item in items:
        if isinstance(item, dict):
            title = str(item.get("title", "unknown")).strip()
            quantity = int(item.get("quantity", 1))
            price = float(item.get("price", 0))
            totals[title] += price * quantity
            counts[title] += quantity

    report = {"totals": dict(totals), "counts": dict(counts)}
    report.update(extra)
    return report


# 4. Inheritance, encapsulation and method overriding
class BaseAccount:
    def __init__(self, user_id, name, address="Not set"):
        self._user_id = None
        self._name = None
        self._address = address
        self.user_id = user_id
        self.name = name

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if value is None or len(str(value).strip()) < 3:
            raise ValueError("User ID must be at least 3 characters long.")
        self._user_id = str(value).strip()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None or len(str(value).strip()) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        self._name = str(value).strip()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = str(value).strip() if value else "Not set"

    def get_role_label(self):
        return "Account"

    def __str__(self):
        return f"{self.get_role_label()}({self.user_id})"


class CustomerAccount(BaseAccount):
    def __init__(self, user_id, name, address="Not set", contact_number="Not set"):
        super().__init__(user_id, name, address)
        self._contact_number = contact_number

    @property
    def contact_number(self):
        return self._contact_number

    @contact_number.setter
    def contact_number(self, value):
        self._contact_number = str(value).strip() or "Not set"

    def get_role_label(self):
        return "Customer"

    def display(self):
        return f"{self.name} - {self.contact_number}"


class RestaurantAccount(BaseAccount):
    def __init__(self, user_id, name, address="Not set", restaurant_type="General"):
        super().__init__(user_id, name, address)
        self._restaurant_type = restaurant_type

    @property
    def restaurant_type(self):
        return self._restaurant_type

    @restaurant_type.setter
    def restaurant_type(self, value):
        self._restaurant_type = str(value).strip() or "General"

    def get_role_label(self):
        return "Restaurant"

    def display(self):
        return f"{self.name} - {self.restaurant_type}"


# 5. Iterator and generator
class OrderIterator:
    def __init__(self, items):
        self._items = list(items)
        self._index = 0

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item


def generate_menu_titles(menu_items):
    for item in menu_items:
        yield item["title"]


# 6. generator expression example
# This is a simple, beginner-friendly way to use a generator expression.
def generate_title_list(menu_items):
    return (item["title"] for item in menu_items)


# 7. Example of use in main program
@require_value("name")
def show_account_name(name):
    return name.upper()


if __name__ == "__main__":
    customer = CustomerAccount("cust01", "Alice", "Main Road")
    restaurant = RestaurantAccount("rest01", "Hot Bite", "Market Street", "Fast Food")

    accounts = [customer, restaurant]
    for account in accounts:
        print(account.get_role_label(), account.name)

    items = [{"title": "Burger", "quantity": 2, "price": 50}, {"title": "Pizza", "quantity": 1, "price": 80}]
    print(build_order_report(*items, restaurant="Hot Bite"))
    print(list(generate_menu_titles(items)))
    print(show_account_name("alice"))
