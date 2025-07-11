from rest_framework import permissions

class IsHouseManagerOrNone(permissions.BasePermission):
    """
    Custom permission to only allow managers of a house to edit it.
    Non-managers can view the house details.
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in permissions.SAFE_METHODS:
            if request.method in permissions.SAFE_METHODS:
                return True
            if not request.user.is_anonymous:
                # Allow write access only for authenticated users
                return True
            return False
        
        # Allow write access only for authenticated users who are managers
        return request.user and request.user.is_authenticated and request.user.is_manager

    def has_object_permission(self, request, view, obj):
        # Allow write access only if the user is the manager of the house
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile == obj.manager