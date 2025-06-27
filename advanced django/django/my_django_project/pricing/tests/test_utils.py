"""
Tests for the pricing utils module.
"""
from decimal import Decimal

from django.test import TestCase

from ..utils import format_currency, parse_decimal


class FormatCurrencyTestCase(TestCase):
    """Test cases for the format_currency function."""
    
    def test_format_currency_usd(self):
        """Test formatting USD currency."""
        self.assertEqual(format_currency(Decimal('1234.56'), 'USD'), "$1,234.56")
        self.assertEqual(format_currency(Decimal('0.99'), 'USD'), "$0.99")
        self.assertEqual(format_currency(Decimal('1000000'), 'USD'), "$1,000,000.00")
    
    def test_format_currency_eur(self):
        """Test formatting EUR currency."""
        self.assertEqual(format_currency(Decimal('1234.56'), 'EUR'), "€1,234.56")
    
    def test_format_currency_jpy(self):
        """Test formatting JPY currency (no decimal places)."""
        self.assertEqual(format_currency(Decimal('1234'), 'JPY'), "¥1,234")
        self.assertEqual(format_currency(Decimal('1234.56'), 'JPY'), "¥1,235")  # Rounded
    
    def test_format_currency_unknown(self):
        """Test formatting with unknown currency code."""
        self.assertEqual(format_currency(Decimal('100'), 'XYZ'), "XYZ 100.00")


class ParseDecimalTestCase(TestCase):
    """Test cases for the parse_decimal function."""
    
    def test_parse_decimal_from_decimal(self):
        """Test parsing from Decimal."""
        self.assertEqual(parse_decimal(Decimal('123.45')), Decimal('123.45'))
    
    def test_parse_decimal_from_int(self):
        """Test parsing from int."""
        self.assertEqual(parse_decimal(100), Decimal('100'))
    
    def test_parse_decimal_from_float(self):
        """Test parsing from float."""
        self.assertEqual(parse_decimal(123.45), Decimal('123.45'))
    
    def test_parse_decimal_from_string(self):
        """Test parsing from string."""
        self.assertEqual(parse_decimal('123.45'), Decimal('123.45'))
        self.assertEqual(parse_decimal('1,234.56'), Decimal('1234.56'))
    
    def test_parse_decimal_invalid(self):
        """Test parsing invalid values."""
        with self.assertRaises(ValueError):
            parse_decimal('abc')
        
        with self.assertRaises(ValueError):
            parse_decimal(None)
