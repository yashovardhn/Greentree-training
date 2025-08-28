from rest_framework import viewsets, mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .permissions import (
    IsAllowedToEditTaskListElseNone,
    IsAllowedToEditTaskElseNone,
    IsAllowedToEditAttachmentElseNone
)
from .serializers import (
    TaskSerializer,
    AttachmentSerializer,
    TaskListSerializer
)
from .models import TaskList, Task, Attachment


class TaskListViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAllowedToEditTaskListElseNone]
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'status']
    filterset_fields = ['status']

    def get_queryset(self):
        queryset = super().get_queryset()
        user_profile = self.request.user.profile
        updated_queryset = queryset.filter(created_by=self.request.user)
        return Task.objects.filter(task_list__house=user_profile.house)

    @action(detail=True, methods=['post'], url_path='complete')
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.status = True  # Make sure `status` is a BooleanField
        task.save()
        return Response({'status': 'Task marked as complete'}, status=status.HTTP_200_OK)



class AttachmentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAllowedToEditAttachmentElseNone]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
