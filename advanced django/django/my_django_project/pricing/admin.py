
from django.contrib import admin
from django.utils import timezone

from .models import TaxRate, Discount


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    """Admin configuration for TaxRate model."""
    list_display = ('name', 'rate_percentage', 'country_code', 'state_code', 'is_active')
    list_filter = ('is_active', 'country_code')
    search_fields = ('name', 'country_code', 'state_code')
    
    def rate_percentage(self, obj):
        """Format rate as percentage."""
        return f"{obj.rate * 100}%"
    rate_percentage.short_description = 'Rate'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Admin configuration for Discount model."""
    list_display = (
        'name', 'code', 'percentage_display', 
        'valid_from', 'valid_to', 'is_active', 'is_currently_valid'
    )
    list_filter = ('is_active', 'valid_from', 'valid_to')
    search_fields = ('name', 'code')
    date_hierarchy = 'valid_from'
    
    def percentage_display(self, obj):
        """Format percentage for display."""
        return f"{obj.percentage * 100}%"
    percentage_display.short_description = 'Discount'
    
    def is_currently_valid(self, obj):
        """Check if discount is currently valid."""
        now = timezone.now()
        return obj.valid_from <= now <= obj.valid_to
    is_currently_valid.boolean = True
    is_currently_valid.short_description = 'Currently Valid'
