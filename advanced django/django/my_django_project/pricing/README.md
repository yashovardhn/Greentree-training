# Pricing Module

A reusable Django app for handling product pricing calculations including taxes and discounts.

## Features

- Calculate prices with tax and discount support
- Support for different tax rates based on location
- Discount code system with validity periods
- Currency formatting utilities
- Comprehensive exception handling

## Installation

1. Add 'pricing' to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'pricing',
]
```

2. Run migrations:

```bash
python manage.py makemigrations pricing
python manage.py migrate
```

## Usage

### Basic Price Calculation

```python
from decimal import Decimal
from pricing.calculator import calculate_total_price

# Calculate price with 10% tax and 15% discount
result = calculate_total_price(
    base_price=Decimal('100.00'),
    quantity=2,
    tax_rate=Decimal('0.10'),
    discount_percent=Decimal('0.15')
)

print(f"Subtotal: ${result['subtotal']}")
print(f"Discount: ${result['discount']}")
print(f"Tax: ${result['tax']}")
print(f"Total: ${result['total']}")
```

### Using the Pricing Service

```python
from pricing.services import PricingService

# Example order with multiple items
order_items = [
    {'price': '25.99', 'quantity': 2},  # 2 items at $25.99 each
    {'price': '15.50', 'quantity': 1},  # 1 item at $15.50
]

# Calculate order total with US tax and a discount code
result = PricingService.calculate_order_total(
    items=order_items,
    country_code='US',
    state_code='CA',
    discount_code='SUMMER20'
)

print(f"Order Total: ${result['total']}")
```

## Models

### TaxRate

Represents a tax rate that can be applied to products.

### Discount

Represents a discount that can be applied to orders.

## API Reference

### calculator.py

- `calculate_tax(price, tax_rate)` - Calculate tax for a given price and tax rate
- `apply_discount(price, discount_percent)` - Apply discount to a price
- `calculate_total_price(base_price, quantity, tax_rate, discount_percent)` - Calculate total price with tax and discount

### services.py

- `PricingService` - Service class for handling pricing operations
  - `get_tax_rate(country_code, state_code)` - Get tax rate for a location
  - `get_discount(discount_code)` - Get discount details by code
  - `calculate_order_total(items, country_code, state_code, discount_code)` - Calculate total for an order

## Testing

Run the test suite with:

```bash
python manage.py test pricing
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT
