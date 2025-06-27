
from django.apps import AppConfig


class PricingConfig(AppConfig):
    """Configuration for the pricing app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pricing'
    verbose_name = 'Pricing Module'
    
    def ready(self):
        """Run when the app is ready."""
        # Import signals here to avoid AppRegistryNotReady issues
        # and to ensure they're only loaded once.
        from . import signals  # noqa: F401
