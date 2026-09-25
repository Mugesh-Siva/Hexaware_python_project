import re
from datetime import datetime


def validate_name(value):
    if value is None:
        return False, "Name is required."

    name = str(value).strip()
    if not name:
        return False, "Name cannot be empty."
    if len(name) < 2 or len(name) > 50:
        return False, "Name must be between 2 and 50 characters."
    if not re.fullmatch(r"[A-Za-z][A-Za-z\s.'-]*", name):
        return False, "Name can only contain letters, spaces, periods, apostrophes, and hyphens."
    return True, "Name is valid."


def validate_address(value):
    if value is None:
        return False, "Address is required."

    address = str(value).strip()
    if not address:
        return False, "Address cannot be empty."
    if len(address) < 5 or len(address) > 255:
        return False, "Address must be between 5 and 255 characters."
    return True, "Address is valid."


def validate_contact(value):
    if value is None:
        return False, "Contact number is required."

    contact = str(value).strip()
    if not contact:
        return False, "Contact number cannot be empty."
    if not re.fullmatch(r"^\+?[0-9][0-9\s.-]{8,}[0-9]$", contact):
        return False, "Contact number must contain at least 10 digits and may include +, spaces, hyphens, or dots."
    digits = re.sub(r"\D", "", contact)
    if len(digits) < 10:
        return False, "Contact number must contain at least 10 digits."
    return True, "Contact number is valid."


def validate_email(value):
    if value is None:
        return False, "Recovery email is required."

    email = str(value).strip()
    if not email:
        return False, "Recovery email cannot be empty."
    if not re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
        return False, "Recovery email must be a valid email address."
    return True, "Recovery email is valid."


def validate_password(value):
    if value is None:
        return False, "Password is required."

    password = str(value)
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must include at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must include at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must include at least one number."
    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Password must include at least one special character."
    return True, "Password is valid."


def validate_amount(value):
    if value is None:
        return False, "Amount is required."

    try:
        amount = float(str(value).strip())
    except ValueError:
        return False, "Amount must be a valid number."

    if amount <= 0:
        return False, "Amount must be greater than 0."
    if amount > 1000000:
        return False, "Amount cannot exceed ₹1,000,000."
    return True, "Amount is valid."


def validate_card_number(value):
    if value is None:
        return False, "Card number is required."

    card_number = str(value).strip().replace(" ", "").replace("-", "")
    if not re.fullmatch(r"\d{16}", card_number):
        return False, "Card number must contain exactly 16 digits."

    total = 0
    is_second = False
    for ch in reversed(card_number):
        digit = int(ch)
        if is_second:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
        is_second = not is_second

    if total % 10 != 0:
        return False, "Card number is invalid."

    return True, "Card number is valid."


def validate_expiry_date(value):
    if value is None:
        return False, "Expiry date is required."

    expiry = str(value).strip()
    if not re.fullmatch(r"\d{2}/\d{2,4}", expiry):
        return False, "Expiry date must be in MM/YY or MM/YYYY format."

    try:
        month_str, year_str = expiry.split("/", 1)
        month = int(month_str)
        year = int(year_str)
        if len(year_str) == 2:
            year = 2000 + year
        if month < 1 or month > 12:
            return False, "Expiry month must be between 01 and 12."

        today = datetime.now()
        expiry_date = datetime(year, month, 1)
        if expiry_date < datetime(today.year, today.month, 1):
            return False, "Card has expired. Please use a valid expiry date."
        return True, "Expiry date is valid."
    except ValueError:
        return False, "Expiry date is invalid. Please use MM/YY or MM/YYYY."


def validate_cvv(value):
    if value is None:
        return False, "CVV is required."

    cvv = str(value).strip()
    if not re.fullmatch(r"\d{3,4}", cvv):
        return False, "CVV must contain 3 or 4 digits."
    return True, "CVV is valid."
