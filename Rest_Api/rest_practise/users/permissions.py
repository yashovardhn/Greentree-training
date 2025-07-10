from rest_framework import permissions

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    '''Custom permission to only allow owners of an object to edit it.'''
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            # Allow the owner of the object to edit it
            return obj == request.user
        return False
    
class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    '''Custom permissions for ProfileViewset to only allow owners of a profile to edit it.'''
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            # Allow the owner of the profile to edit it
            return request.user.profile == obj
        return False
