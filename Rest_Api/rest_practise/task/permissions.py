from rest_framework import permissions

class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own task lists.
    If the user is an admin, they can edit any task list.
    """
    
    def has_permission(self, request, view):
        if request.METHOD in permissions.SAFE_METHODS:
            return True
        if not request.user.is_ananymous:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.profile == obj.created_by
    
class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own tasks.
    If the user is an admin, they can edit any task.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_ananymous:
            return request.user.profile.house != None
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.profile.house == obj.task_list.house 