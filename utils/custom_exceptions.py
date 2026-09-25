class AppError(Exception):
    """Base exception for project-level errors."""


class ValidationError(AppError):
    """Raised when user input is invalid."""


class PaymentError(AppError):
    """Raised when a payment flow fails."""


class InsufficientBalanceError(PaymentError):
    """Raised when a user does not have enough Hotbite balance."""


class EmptyCartError(AppError):
    """Raised when a cart is empty during checkout."""


class DataAccessError(AppError):
    """Raised when a database operation fails."""
