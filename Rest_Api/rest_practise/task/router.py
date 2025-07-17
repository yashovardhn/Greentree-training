from rest_framework import routers
from .viewsets import TaskListViewSet

APP_NAME = 'task'
router = routers.DefaultRouter()
router.register('tasklists', TaskListViewSet, basename='tasklist')