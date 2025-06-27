"""
Utility functions for the pricing module.
"""
from decimal import Decimal, ROUND_HALF_UP

def format_currency(amount: Decimal, currency: str = 'USD') -> str:
    """
    Format a decimal amount as a currency string.
    
    Args:
        amount: The amount to format
        currency: ISO currency code (default: 'USD')
        
    Returns:
        Formatted currency string
    """
    # In a real application, you might use django.contrib.humanize or Babel
    symbol = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
    }.get(currency.upper(), currency.upper() + ' ')
    
    # Round to 2 decimal places
    rounded = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Format with thousands separator and 2 decimal places
    if currency.upper() == 'JPY':
        # No decimal places for JPY
        formatted = f"{symbol}{rounded:,.0f}"
    else:
        formatted = f"{symbol}{rounded:,.2f}"
    
    return formatted

def parse_decimal(value) -> Decimal:
    """
    Safely convert a value to Decimal.
    
    Args:
        value: Value to convert (str, int, float, or Decimal)
        
    Returns:
        Decimal value
        
    Raises:
        ValueError: If the value cannot be converted to Decimal
    """
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except (TypeError, ValueError) as e:
        raise ValueError(f"Could not convert {value} to Decimal") from e
