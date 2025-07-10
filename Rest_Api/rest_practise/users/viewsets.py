from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, ProfileSerializer 
from .permissions import IsUserOwnerOrGetAndPostOnly  
from .models import Profile  

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [IsUserOwnerOrGetAndPostOnly] 
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    # Use the custom permission class

class ProfileViewSet(viewsets.ModelViewSet):
    # """
    # A viewset for viewing and editing user profile instances.
    # """
    # permission_classes = [IsUserOwnerOrGetAndPostOnly] 
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
