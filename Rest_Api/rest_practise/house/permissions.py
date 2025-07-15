from rest_framework import permissions

class IsHouseManagerOrNone(permissions.BasePermission):
    """
    Custom permission to:
    - Allow read-only access (GET, HEAD, OPTIONS) for all users (authenticated or anonymous).
    - Allow write access (POST, PUT, PATCH, DELETE) only for authenticated users
      whose associated Profile has 'is_manager' set to True.
    - For object-level permissions (PUT, PATCH, DELETE on a specific instance),
      further restrict write access to only the managers of that specific house.
    """

    def has_permission(self, request, view):
        # Allow read-only access for any request (GET, HEAD, OPTIONS).
        # SAFE_METHODS are methods that do not change the state of the resource.
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write requests (POST, PUT, PATCH, DELETE):
        # 1. User must be authenticated.
        # 2. User must have a 'profile' attribute.
        # 3. The 'profile' must have 'is_manager' set to True.
        # This checks if the user *globally* has manager capabilities to perform
        # actions like creating a house or listing all houses (if restricted).
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and # Ensure profile exists
            request.user.profile.is_manager      # Access is_manager through profile
        )

    def has_object_permission(self, request, view, obj):
        # Allow read-only access to the object for any user.
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write requests (PUT, PATCH, DELETE) on a specific object:
        # The user must be authenticated, have a profile, and their profile
        # must be one of the managers associated with THIS specific 'obj' (House).
        # 'obj.manager' is a ManyToManyField, so we check if the profile is in its queryset.
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and # Ensure profile exists
            request.user.profile in obj.manager.all() # Check if profile is among the house's managers
        )