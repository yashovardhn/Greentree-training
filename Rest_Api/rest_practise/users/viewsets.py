from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer  
from .permissions import IsUserOwnerOrGetAndPostOnly  

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [IsUserOwnerOrGetAndPostOnly] 
    queryset = User.objects.all()
    serializer_class = UserSerializer # Adjust the import path as necessary
    # Use the custom permission class

    
