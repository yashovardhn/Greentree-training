"""
Price calculation utilities for products.
"""
from decimal import Decimal
from typing import List, Dict, Optional


def calculate_tax(price: Decimal, tax_rate: Decimal) -> Decimal:
    """
    Calculate tax for a given price and tax rate.
    
    Args:
        price: Base price as Decimal
        tax_rate: Tax rate as Decimal (e.g., 0.15 for 15%)
        
    Returns:
        Tax amount as Decimal
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
        
    return (price * tax_rate).quantize(Decimal('0.01'))


def apply_discount(price: Decimal, discount_percent: Decimal) -> Decimal:
    """
    Apply discount to a price.
    
    Args:
        price: Original price as Decimal
        discount_percent: Discount percentage as Decimal (e.g., 0.1 for 10%)
        
    Returns:
        Discounted price as Decimal
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 1:
        raise ValueError("Discount percentage must be between 0 and 1")
        
    discount_amount = (price * discount_percent).quantize(Decimal('0.01'))
    return max(Decimal('0'), price - discount_amount)


def calculate_total_price(
    base_price: Decimal,
    quantity: int = 1,
    tax_rate: Optional[Decimal] = None,
    discount_percent: Optional[Decimal] = None
) -> Dict[str, Decimal]:
    """
    Calculate the total price including tax and discount.
    
    Args:
        base_price: Price of a single item as Decimal
        quantity: Number of items (default: 1)
        tax_rate: Optional tax rate as Decimal (e.g., 0.15 for 15%)
        discount_percent: Optional discount percentage as Decimal (e.g., 0.1 for 10%)
        
    Returns:
        Dictionary containing:
        - subtotal: Price before tax and discount
        - discount: Total discount amount
        - tax: Total tax amount
        - total: Final price after all calculations
    """
    if base_price < 0:
        raise ValueError("Base price cannot be negative")
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
        
    tax_rate = tax_rate if tax_rate is not None else Decimal('0')
    discount_percent = discount_percent if discount_percent is not None else Decimal('0')
    
    subtotal = base_price * quantity
    
    # Apply discount if provided
    if discount_percent > 0:
        discount_amount = (subtotal * discount_percent).quantize(Decimal('0.01'))
        discounted_subtotal = max(Decimal('0'), subtotal - discount_amount)
    else:
        discount_amount = Decimal('0')
        discounted_subtotal = subtotal
    
    # Calculate tax on the discounted subtotal
    if tax_rate > 0:
        tax_amount = calculate_tax(discounted_subtotal, tax_rate)
    else:
        tax_amount = Decimal('0')
    
    total = discounted_subtotal + tax_amount
    
    return {
        'subtotal': subtotal.quantize(Decimal('0.01')),
        'discount': discount_amount.quantize(Decimal('0.01')),
        'tax': tax_amount.quantize(Decimal('0.01')),
        'total': total.quantize(Decimal('0.01'))
    }
