"""
Pricing services for handling complex pricing operations.
"""
from decimal import Decimal
from typing import List, Dict, Optional
from django.utils import timezone
from .calculator import calculate_total_price
from .models import TaxRate, Discount


class PricingService:
    """
    Service class for handling pricing operations.
    """
    
    @staticmethod
    def get_tax_rate(country_code: str, state_code: str = None) -> Decimal:
        """
        Get the applicable tax rate for a location.
        
        Args:
            country_code: ISO country code
            state_code: Optional state/province code
            
        Returns:
            Tax rate as Decimal
        """
        # In a real application, you would query the TaxRate model
        # based on the location. This is a simplified version.
        try:
            tax_rate = TaxRate.objects.filter(
                is_active=True,
                country_code=country_code,
                state_code=state_code if state_code else ''
            ).order_by('-created_at').first()
            
            if tax_rate:
                return tax_rate.rate
                
            # Default to 0% tax if no specific rate found
            return Decimal('0')
            
        except TaxRate.DoesNotExist:
            return Decimal('0')
    
    @staticmethod
    def get_discount(discount_code: str = None) -> Optional[Dict]:
        """
        Get discount details by code if it's valid.
        
        Args:
            discount_code: Optional discount code
            
        Returns:
            Dictionary with discount details or None if not found/valid
        """
        if not discount_code:
            return None
            
        try:
            discount = Discount.objects.get(
                code=discount_code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            return {
                'id': discount.id,
                'name': discount.name,
                'code': discount.code,
                'percentage': discount.percentage
            }
        except Discount.DoesNotExist:
            return None
    
    @classmethod
    def calculate_order_total(
        cls,
        items: List[Dict],
        country_code: str = None,
        state_code: str = None,
        discount_code: str = None
    ) -> Dict:
        """
        Calculate the total price for an order with multiple items.
        
        Args:
            items: List of dictionaries containing 'price' and 'quantity'
            country_code: ISO country code for tax calculation
            state_code: Optional state/province code for tax calculation
            discount_code: Optional discount code
            
        Returns:
            Dictionary with order summary
        """
        # Get tax rate if location is provided
        tax_rate = (
            cls.get_tax_rate(country_code, state_code)
            if country_code else Decimal('0')
        )
        
        # Get discount if code is provided
        discount = cls.get_discount(discount_code)
        discount_percent = discount['percentage'] if discount else Decimal('0')
        
        # Calculate totals for each item
        order_subtotal = Decimal('0')
        order_discount = Decimal('0')
        order_items = []
        
        for item in items:
            price = Decimal(str(item['price']))
            quantity = int(item['quantity'])
            
            # Calculate item total
            result = calculate_total_price(
                base_price=price,
                quantity=quantity,
                tax_rate=tax_rate,
                discount_percent=discount_percent
            )
            
            order_subtotal += result['subtotal']
            order_discount += result['discount']
            
            order_items.append({
                'price': price,
                'quantity': quantity,
                'item_subtotal': result['subtotal'],
                'item_discount': result['discount'],
                'item_tax': result['tax'],
                'item_total': result['total']
            })
        
        # Calculate order-level totals
        order_tax = sum(item['item_tax'] for item in order_items)
        order_total = order_subtotal - order_discount + order_tax
        
        return {
            'items': order_items,
            'subtotal': order_subtotal.quantize(Decimal('0.01')),
            'discount': order_discount.quantize(Decimal('0.01')),
            'tax': order_tax.quantize(Decimal('0.01')),
            'total': order_total.quantize(Decimal('0.01')),
            'tax_rate': tax_rate,
            'discount_applied': bool(discount),
            'discount_details': discount
        }
