from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, permissions
from .serializers import UserSerializer, ProfileSerializer 
from .permissions import IsUserOwnerOrGetAndPostOnly, IsProfileOwnerOrReadOnly
from .models import Profile  


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    - List: Admin only
    - Create: Anyone (for registration)
    - Retrieve/Update/Delete: Owner or admin only
    """
    queryset = User.objects.all()
    permission_classes = [IsUserOwnerOrGetAndPostOnly]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        elif self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.none()
    
    def get_permissions(self):
        if self.action == 'create':
            # Allow anyone to create a user (registration)
            return [permissions.AllowAny()]
        return super().get_permissions()

class ProfileViewSet(viewsets.GenericViewSet, 
                      mixins.RetrieveModelMixin, 
                      mixins.UpdateModelMixin, 
                      mixins.ListModelMixin, 
                      mixins.CreateModelMixin, 
                      mixins.DestroyModelMixin):
    """
    A viewset for viewing and editing profiles.
    - List: Admin only
    - Create: Not allowed (handled by user creation)
    - Retrieve: Owner or admin
    - Update/Delete: Owner or admin only
    """
    queryset = Profile.objects.all() 
    permission_classes = [IsProfileOwnerOrReadOnly, permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Profiles should be created through user creation
        raise MethodNotAllowed('POST', detail='Cannot create profile directly. Create a user instead.')
