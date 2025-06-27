
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Discount


@receiver(pre_save, sender=Discount)
def validate_discount_dates(sender, instance, **kwargs):
    """Ensure discount end date is after start date."""
    if instance.valid_to <= instance.valid_from:
        raise ValueError("Discount end date must be after start date")
