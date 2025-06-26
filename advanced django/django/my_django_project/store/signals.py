from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def log_new_user(sender, instance, created, **kwargs):
    """
    Log when a new user is created.
    """
    if created:
        logger.info(f"New user created: {instance.username} (ID: {instance.id})")
        # You can also log additional information like:
        # logger.info(f"Email: {instance.email}")
        # logger.info(f"Date joined: {instance.date_joined}")
