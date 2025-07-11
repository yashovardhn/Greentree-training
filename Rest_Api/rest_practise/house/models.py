from django.db import models
import os
import uuid
from django.utils.deconstruct import deconstructible

@deconstructible
class GenerateHouseImagePath(object):

    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/houses/{instance.id}/images'
        name = f'main.{ext}'
        return os.path.join(path, name)
    
house_image_path = GenerateHouseImagePath('media/houses/images')
class House(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to= house_image_path, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    manager = models.OneToOneField('users.Profile', on_delete=models.SET_NULL, blank=True, null=True, related_name='house_manager')
    members = models.ManyToManyField('users.Profile', related_name='houses', blank=True)
    points = models.IntegerField(default=0)
    completed_task_count = models.IntegerField(default=0)
    not_completed_task_count = models.IntegerField(default=0)



    def __str__(self):
        return f' - {self.name} House'
# Create your models here.
