from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import TaskList, Task, Attachment, COMPLETE, NOT_COMPLETE

@receiver(post_save, sender=TaskList)
def update_house_points(sender, instance, created, **kwargs):
    if created:
        # Logic to update house points when a new task or task list is created
        house = instance.house
        if instance.status == COMPLETE:
            house.points += 10
        elif instance.status == NOT_COMPLETE:
            if house.points > 10:
                house.points -= 10
        house.save()

@receiver(post_save, sender=Task)
def update_task_list_status(sender, instance, created, **kwargs):
    # Logic to update task list status when a new task is created
    task_list = instance.task_list
    is_complete = True
    for task in task_list.tasks.all():
        if task.status != COMPLETE:
            is_complete = False
            break
    task_list.status = COMPLETE if is_complete else NOT_COMPLETE
    task_list.save()