import re


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
    if len(address) < 10 or len(address) > 255:
        return False, "Address must be between 10 and 255 characters."
    return True, "Address is valid."


def validate_contact(value):
    if value is None:
        return False, "Contact number is required."

    contact = str(value).strip()
    if not contact:
        return False, "Contact number cannot be empty."
    if not re.fullmatch(r"[+]?\d[\d\s.-]{8,}\d", contact):
        return False, "Contact number must contain at least 10 digits and may include +, spaces, hyphens, or dots."
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
