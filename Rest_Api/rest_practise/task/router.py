from rest_framework import routers
from .viewsets import TaskListViewSet, TaskViewSet, AttachmentViewSet

APP_NAME = 'task'
router = routers.DefaultRouter()
router.register('tasklists', TaskListViewSet, basename='tasklist')
router.register('tasks', TaskViewSet, basename='task')
router.register('attachments', AttachmentViewSet, basename='attachment')
