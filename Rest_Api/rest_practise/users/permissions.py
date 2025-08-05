from rest_framework import permissions


class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Anyone to create a user (handled in viewset)
    - Any authenticated user to view user lists (filtered in viewset)
    - Only the user themselves (or admin) to edit/delete their account
    """
    
    def has_permission(self, request, view):
        # Allow all GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Allow POST (user registration) - this is handled in the viewset
        if request.method == 'POST':
            return True
            
        # For other methods, require authentication
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow read-only methods for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Allow write permissions only for the user themselves or admin
        return obj == request.user or request.user.is_staff


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permissions for ProfileViewset to only allow:
    - Read access to any authenticated user
    - Write access only to the profile owner or admin
    """
    
    def has_permission(self, request, view):
        # Only allow authenticated users
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Allow all authenticated users to list profiles (filtered in viewset)
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Only allow profile creation through user creation
        if request.method == 'POST':
            return False
            
        return True
    
    def has_object_permission(self, request, view, obj):
        # Allow read access to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Allow write access only to the profile owner or admin
        return obj.user == request.user or request.user.is_staff
