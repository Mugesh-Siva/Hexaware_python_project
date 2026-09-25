import re


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
