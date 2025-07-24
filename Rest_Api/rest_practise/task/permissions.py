from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    """
    Allow all authenticated users with a profile to view task lists,
    but only allow modifications if they belong to a house.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not hasattr(user, 'profile'):
            return False

        # Allow all SAFE_METHODS like GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow editing if the user belongs to a house
        return user.profile.house is not None

    def has_object_permission(self, request, view, obj):
        # Viewing allowed if SAFE_METHODS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow edits by the creator
        return request.user.profile == obj.created_by


class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    """
    SAFE_METHODS: Allow all authenticated users to view
    Write access: Only users in the same house as the task's task_list
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile')
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            hasattr(request.user, 'profile') and
            obj.task_list.house == request.user.profile.house
        )


class IsAllowedToEditAttachmentElseNone(BasePermission):
    """
    Allow viewing Attachments for users in the same house.
    Allow editing only for the creator of the Task.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.house is not None
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.task.task_list.house == request.user.profile.house
        return obj.task.created_by == request.user.profile
