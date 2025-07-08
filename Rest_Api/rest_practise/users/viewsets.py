from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer  

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer # Adjust the import path as necessary

    
