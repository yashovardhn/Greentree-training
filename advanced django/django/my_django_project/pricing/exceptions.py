"""
Exceptions for the pricing module.
"""
from django.core.exceptions import ValidationError


class PricingError(ValidationError):
    """Base exception for pricing-related errors."""
    pass


class InvalidPriceError(PricingError):
    """Raised when an invalid price is provided."""
    pass


class InvalidTaxRateError(PricingError):
    """Raised when an invalid tax rate is provided."""
    pass


class InvalidDiscountError(PricingError):
    """Raised when an invalid discount is provided."""
    pass


class DiscountExpiredError(InvalidDiscountError):
    """Raised when a discount has expired."""
    pass
