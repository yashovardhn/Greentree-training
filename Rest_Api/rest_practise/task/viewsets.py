from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from .permissions import IsAllowedToEditTaskListElseNone

from .models import TaskList, Task, Attachment
from .serializers import TaskListSerializer

class TaskListViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAllowedToEditTaskListElseNone]

    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsAdminUser]
    #     return super().get_permissions()

    # @action(detail=True, methods=['get'], name='Get Tasks Count')
    # def tasks_count(self, request, pk=None):
    #     task_list = self.get_object()
    #     tasks_count = task_list.tasks.count()
    #     return Response({'tasks_count': tasks_count}, status=status.HTTP_200_OK)
    
