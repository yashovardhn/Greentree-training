from rest_framework import routers
from .viewsets import TaskListViewSet, TaskViewSet, AttachmentViewSet

APP_NAME = 'task'
router = routers.DefaultRouter()
router.register('tasklists', TaskListViewSet)
router.register(r'tasks', TaskViewSet, basename='task')
router.register('attachments', AttachmentViewSet)
