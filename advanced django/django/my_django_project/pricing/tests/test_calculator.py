
from decimal import Decimal
import pytest
from ..calculator import calculate_tax, apply_discount, calculate_total_price
from ..exceptions import InvalidPriceError


class TestCalculateTax:
    """Tests for the calculate_tax function."""

    def test_calculate_tax_positive(self):
        """Test tax calculation with positive values."""
        assert calculate_tax(Decimal('100.00'), Decimal('0.15')) == Decimal('15.00')
        assert calculate_tax(Decimal('50.00'), Decimal('0.10')) == Decimal('5.00')
        assert calculate_tax(Decimal('0.01'), Decimal('0.20')) == Decimal('0.00')  # Rounded down

    def test_calculate_tax_zero_rate(self):
        """Test tax calculation with zero tax rate."""
        assert calculate_tax(Decimal('100.00'), Decimal('0')) == Decimal('0.00')

    def test_calculate_tax_negative_price(self):
        """Test tax calculation with negative price raises error."""
        with pytest.raises(ValueError):
            calculate_tax(Decimal('-100.00'), Decimal('0.15'))

    def test_calculate_tax_negative_rate(self):
        """Test tax calculation with negative tax rate raises error."""
        with pytest.raises(ValueError):
            calculate_tax(Decimal('100.00'), Decimal('-0.15'))


class TestApplyDiscount:
    """Tests for the apply_discount function."""

    def test_apply_discount_positive(self):
        """Test discount application with valid values."""
        assert apply_discount(Decimal('100.00'), Decimal('0.10')) == Decimal('90.00')
        assert apply_discount(Decimal('50.00'), Decimal('0.20')) == Decimal('40.00')
        assert apply_discount(Decimal('10.00'), Decimal('1.00')) == Decimal('0.00')  # 100% discount

    def test_apply_discount_zero_discount(self):
        """Test discount application with zero discount."""
        assert apply_discount(Decimal('100.00'), Decimal('0')) == Decimal('100.00')

    def test_apply_discount_negative_price(self):
        """Test discount application with negative price raises error."""
        with pytest.raises(ValueError):
            apply_discount(Decimal('-100.00'), Decimal('0.10'))

    def test_apply_discount_invalid_percent(self):
        """Test discount application with invalid percentage raises error."""
        with pytest.raises(ValueError):
            apply_discount(Decimal('100.00'), Decimal('-0.10'))
        with pytest.raises(ValueError):
            apply_discount(Decimal('100.00'), Decimal('1.10'))


class TestCalculateTotalPrice:
    """Tests for the calculate_total_price function."""

    def test_calculate_total_price_no_tax_no_discount(self):
        """Test total price calculation with no tax and no discount."""
        result = calculate_total_price(Decimal('100.00'), 2)
        assert result['subtotal'] == Decimal('200.00')
        assert result['discount'] == Decimal('0.00')
        assert result['tax'] == Decimal('0.00')
        assert result['total'] == Decimal('200.00')

    def test_calculate_total_price_with_tax(self):
        """Test total price calculation with tax."""
        result = calculate_total_price(
            base_price=Decimal('100.00'),
            quantity=2,
            tax_rate=Decimal('0.10')
        )
        assert result['subtotal'] == Decimal('200.00')
        assert result['discount'] == Decimal('0.00')
        assert result['tax'] == Decimal('20.00')
        assert result['total'] == Decimal('220.00')

    def test_calculate_total_price_with_discount(self):
        """Test total price calculation with discount."""
        result = calculate_total_price(
            base_price=Decimal('100.00'),
            quantity=2,
            discount_percent=Decimal('0.10')
        )
        assert result['subtotal'] == Decimal('200.00')
        assert result['discount'] == Decimal('20.00')
        assert result['tax'] == Decimal('0.00')
        assert result['total'] == Decimal('180.00')

    def test_calculate_total_price_with_tax_and_discount(self):
        """Test total price calculation with both tax and discount."""
        result = calculate_total_price(
            base_price=Decimal('100.00'),
            quantity=2,
            tax_rate=Decimal('0.10'),
            discount_percent=Decimal('0.10')
        )
        assert result['subtotal'] == Decimal('200.00')
        assert result['discount'] == Decimal('20.00')
        assert result['tax'] == Decimal('18.00')  # 10% of (200 - 20)
        assert result['total'] == Decimal('198.00')  # 200 - 20 + 18

    def test_calculate_total_price_edge_cases(self):
        """Test edge cases in total price calculation."""
        # Zero quantity
        result = calculate_total_price(Decimal('100.00'), 0)
        assert result['subtotal'] == Decimal('0.00')
        assert result['total'] == Decimal('0.00')
        
        # Zero price
        result = calculate_total_price(Decimal('0.00'), 2)
        assert result['subtotal'] == Decimal('0.00')
        assert result['total'] == Decimal('0.00')
        
        # 100% discount
        result = calculate_total_price(
            base_price=Decimal('100.00'),
            quantity=1,
            discount_percent=Decimal('1.00')
        )
        assert result['subtotal'] == Decimal('100.00')
        assert result['discount'] == Decimal('100.00')
        assert result['total'] == Decimal('0.00')

    def test_calculate_total_price_negative_values(self):
        """Test total price calculation with invalid values."""
        with pytest.raises(ValueError):
            calculate_total_price(Decimal('-100.00'), 1)
            
        with pytest.raises(ValueError):
            calculate_total_price(Decimal('100.00'), -1)
