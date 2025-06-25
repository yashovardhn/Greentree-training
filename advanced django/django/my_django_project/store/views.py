from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserProfileSerializer, CustomTokenObtainPairSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    """
    get:
    Retrieve the authenticated user's profile.
    
    put:
    Update the authenticated user's profile.
    
    patch:
    Partially update the authenticated user's profile.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile.",
        responses={
            200: UserProfileSerializer(),
            401: "Unauthorized",
            403: "Forbidden"
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    @swagger_auto_schema(
        operation_description="Update the authenticated user's profile.",
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer(),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden"
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Partially update the authenticated user's profile.",
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer(),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden"
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        # Return the user making the request
        return self.request.user

class UserProfileList(generics.ListAPIView):
    """
    get:
    List all user profiles.
    
    This endpoint is only accessible to admin users.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @swagger_auto_schema(
        operation_description="List all user profiles (admin only).",
        responses={
            200: UserProfileSerializer(many=True),
            401: "Unauthorized",
            403: "Forbidden"
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    post:
    Obtain JWT token pair (access and refresh).
    
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    @swagger_auto_schema(
        operation_description="Obtain JWT token pair (access and refresh).",
        request_body=CustomTokenObtainPairSerializer,
        responses={
            200: openapi.Response(
                description="Authentication successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Invalid credentials",
            401: "Authentication failed"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RegisterView(generics.CreateAPIView):
    """
    post:
    Register a new user.
    
    Creates a new user with the provided username, email, and password.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Register a new user account.",
        request_body=UserProfileSerializer,
        responses={
            201: UserProfileSerializer(),
            400: "Invalid data"
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
