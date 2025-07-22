from rest_framework import permissions

class IsHouseManagerOrNone(permissions.BasePermission):
    """
    Custom permission to:
    - Allow read-only access (GET, HEAD, OPTIONS) for all users (authenticated or anonymous).
    - Allow write access (POST, PUT, PATCH, DELETE) only for authenticated users
    whose associated Profile has 'is_manager' set to True.
    - For object-level permissions (PUT, PATCH, DELETE on a specific instance),
    further restrict write access to only the manager of that specific house.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.is_manager
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile == obj.manager
        )
