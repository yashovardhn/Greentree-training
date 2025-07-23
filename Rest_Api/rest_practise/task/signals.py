from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import TaskList, Task, Attachment

def update_house_points(sender, instance, created, **kwargs):
    if created:
        # Logic to update house points when a new task or task list is created
        house = instance.house
        house.points += 10  # Example logic, adjust as needed
        house.save()