from rest_framework import permissions

class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.house is not None
        )
    def has_object_permission(self, request, view, obj):
        return request.user.profile == obj.created_by  # Also fixed to `request.user`

    
class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own tasks.
    If the user is an admin, they can edit any task.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.house is not None
        )
    
    def has_object_permission(self, request, view, obj):
        return request.user.profile.house == obj.task_list.house 
    
class IsAllowedToEditAttachmentElseNone(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own attachments.
    If the user is an admin, they can edit any attachment.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.house is not None
        )
    
    def has_object_permission(self, request, view, obj):
        return request.user.profile.house == obj.task.task_list.house