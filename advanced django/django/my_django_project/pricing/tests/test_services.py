"""
Tests for the pricing services module.
"""
from datetime import timedelta
from decimal import Decimal

import pytest
from django.test import TestCase
from django.utils import timezone

from ..models import TaxRate, Discount
from ..services import PricingService


class PricingServiceTestCase(TestCase):
    """Test cases for the PricingService class."""
    
    def setUp(self):
        """Set up test data."""
        # Create test tax rates
        self.tax_rate_us = TaxRate.objects.create(
            name="US Standard",
            rate=Decimal('0.10'),
            country_code='US',
            state_code=''
        )
        
        self.tax_rate_ca = TaxRate.objects.create(
            name="Canada Standard",
            rate=Decimal('0.13'),
            country_code='CA',
            state_code='ON'
        )
        
        # Create test discounts
        now = timezone.now()
        self.active_discount = Discount.objects.create(
            name="Summer Sale",
            code="SUMMER20",
            percentage=Decimal('0.20'),
            valid_from=now - timedelta(days=1),
            valid_to=now + timedelta(days=30)
        )
        
        self.expired_discount = Discount.objects.create(
            name="Expired Sale",
            code="EXPIRED20",
            percentage=Decimal('0.20'),
            valid_from=now - timedelta(days=30),
            valid_to=now - timedelta(days=1)
        )
    
    def test_get_tax_rate_found(self):
        """Test getting tax rate for a country."""
        rate = PricingService.get_tax_rate('US')
        self.assertEqual(rate, Decimal('0.10'))
    
    def test_get_tax_rate_not_found(self):
        """Test getting tax rate for a non-existent country."""
        rate = PricingService.get_tax_rate('XX')
        self.assertEqual(rate, Decimal('0'))
    
    def test_get_discount_found(self):
        """Test getting an active discount by code."""
        discount = PricingService.get_discount("SUMMER20")
        self.assertIsNotNone(discount)
        self.assertEqual(discount['code'], "SUMMER20")
        self.assertEqual(discount['percentage'], Decimal('0.20'))
    
    def test_get_discount_expired(self):
        """Test getting an expired discount by code."""
        discount = PricingService.get_discount("EXPIRED20")
        self.assertIsNone(discount)
    
    def test_get_discount_not_found(self):
        """Test getting a non-existent discount by code."""
        discount = PricingService.get_discount("NONEXISTENT")
        self.assertIsNone(discount)
    
    def test_calculate_order_total_no_tax_no_discount(self):
        """Test order total calculation with no tax and no discount."""
        order_items = [
            {'price': '25.99', 'quantity': 2},
            {'price': '15.50', 'quantity': 1}
        ]
        
        result = PricingService.calculate_order_total(
            items=order_items
        )
        
        self.assertEqual(result['subtotal'], Decimal('67.48'))  # 25.99*2 + 15.50
        self.assertEqual(result['discount'], Decimal('0.00'))
        self.assertEqual(result['tax'], Decimal('0.00'))
        self.assertEqual(result['total'], Decimal('67.48'))
    
    def test_calculate_order_total_with_tax(self):
        """Test order total calculation with tax."""
        order_items = [
            {'price': '25.99', 'quantity': 2},
            {'price': '15.50', 'quantity': 1}
        ]
        
        result = PricingService.calculate_order_total(
            items=order_items,
            country_code='US',
            state_code='CA'
        )
        
        self.assertEqual(result['subtotal'], Decimal('67.48'))
        self.assertEqual(result['discount'], Decimal('0.00'))
        self.assertEqual(result['tax'], Decimal('6.75'))  # 10% of 67.48
        self.assertEqual(result['total'], Decimal('74.23'))  # 67.48 + 6.75
    
    def test_calculate_order_total_with_discount(self):
        """Test order total calculation with discount."""
        order_items = [
            {'price': '25.99', 'quantity': 2},
            {'price': '15.50', 'quantity': 1}
        ]
        
        result = PricingService.calculate_order_total(
            items=order_items,
            discount_code='SUMMER20'
        )
        
        self.assertEqual(result['subtotal'], Decimal('67.48'))
        self.assertEqual(result['discount'], Decimal('13.50'))  # 20% of 67.48
        self.assertEqual(result['tax'], Decimal('0.00'))
        self.assertEqual(result['total'], Decimal('53.98'))  # 67.48 - 13.50
    
    def test_calculate_order_total_with_tax_and_discount(self):
        """Test order total calculation with both tax and discount."""
        order_items = [
            {'price': '25.99', 'quantity': 2},
            {'price': '15.50', 'quantity': 1}
        ]
        
        result = PricingService.calculate_order_total(
            items=order_items,
            country_code='US',
            state_code='CA',
            discount_code='SUMMER20'
        )
        
        self.assertEqual(result['subtotal'], Decimal('67.48'))
        self.assertEqual(result['discount'], Decimal('13.50'))  # 20% of 67.48
        self.assertEqual(result['tax'], Decimal('5.40'))  # 10% of (67.48 - 13.50)
        self.assertEqual(result['total'], Decimal('59.38'))  # 67.48 - 13.50 + 5.40
    
    def test_calculate_order_total_empty_items(self):
        """Test order total calculation with empty items list."""
        result = PricingService.calculate_order_total(items=[])
        self.assertEqual(result['subtotal'], Decimal('0.00'))
        self.assertEqual(result['total'], Decimal('0.00'))
    
    def test_calculate_order_total_invalid_items(self):
        """Test order total calculation with invalid items."""
        with self.assertRaises(ValueError):
            PricingService.calculate_order_total(
                items=[{'price': '-10.00', 'quantity': 1}]
            )
        
        with self.assertRaises(ValueError):
            PricingService.calculate_order_total(
                items=[{'price': '10.00', 'quantity': -1}]
            )
