from services.customerServices.balanceService import deduct_hotbite_balance, get_hotbite_balance
from utils.custom_exceptions import InsufficientBalanceError, PaymentError, ValidationError
from utils.validators import validate_card_number, validate_cvv, validate_expiry_date


def process_card_payment(amount, card_number, expiry_date, cvv):
    try:
        amount_value = float(amount)
        if amount_value <= 0:
            raise ValidationError("Payment amount must be greater than 0.")

        valid, message = validate_card_number(card_number)
        if not valid:
            raise ValidationError(message)

        valid, message = validate_expiry_date(expiry_date)
        if not valid:
            raise ValidationError(message)

        valid, message = validate_cvv(cvv)
        if not valid:
            raise ValidationError(message)

        return {
            "success": True,
            "message": "Dummy card payment approved. Payment details were not saved.",
            "amount": amount_value,
        }
    except (ValidationError, ValueError) as exc:
        return {"success": False, "message": str(exc)}
    except Exception as exc:
        return {"success": False, "message": f"Error while processing card payment: {exc}"}


def process_cash_payment(amount):
    try:
        amount_value = float(amount)
        if amount_value <= 0:
            raise ValidationError("Cash amount must be greater than 0.")

        return {
            "success": True,
            "message": "Cash payment selected. Please pay at the time of delivery.",
            "amount": amount_value,
        }
    except (ValidationError, ValueError) as exc:
        return {"success": False, "message": str(exc)}
    except Exception as exc:
        return {"success": False, "message": f"Error while processing cash payment: {exc}"}


def process_hotbite_payment(user_id, amount):
    try:
        amount_value = float(amount)
        if amount_value <= 0:
            raise ValidationError("Amount must be greater than 0.")

        balance = get_hotbite_balance(user_id)
        if balance < amount_value:
            raise InsufficientBalanceError("Insufficient Hotbite balance. Please add balance first.")

        result = deduct_hotbite_balance(user_id, amount_value)
        if not result["success"]:
            raise PaymentError(result["message"])

        return {
            "success": True,
            "message": "Hotbite payment successful.",
            "amount": amount_value,
        }
    except (InsufficientBalanceError, ValidationError, PaymentError) as exc:
        return {"success": False, "message": str(exc)}
    except Exception as exc:
        return {"success": False, "message": f"Error while processing Hotbite payment: {exc}"}
