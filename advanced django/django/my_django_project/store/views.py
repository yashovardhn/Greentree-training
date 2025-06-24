from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer, CustomTokenObtainPairSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user profile.
    Only the owner can access or update their profile.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        # Return the user making the request
        return self.request.user

class UserProfileList(generics.ListAPIView):
    """
    List all user profiles (admin only).
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view that uses our custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
