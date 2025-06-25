from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method, swagger_auto_schema
from datetime import date

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data.
    
    This serializer handles the serialization and deserialization of user profile data,
    including creating new users and updating existing ones.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'bio', 'birth_date', 'profile_picture', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
                'min_length': 8,
                'help_text': 'Password must be at least 8 characters long.'
            },
            'email': {
                'required': True,
                'allow_blank': False,
                'help_text': 'Email address is required.'
            },
            'username': {
                'min_length': 4,
                'help_text': 'Username must be at least 4 characters long.'
            },
            'birth_date': {
                'help_text': 'Date in YYYY-MM-DD format.'
            }
        }

    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        """
        # Remove password from validated_data before creating the user
        password = validated_data.pop('password', None)
        
        # Create user with remaining validated data
        user = User.objects.create_user(
            **validated_data
        )
        
        # Set password if provided
        if password:
            user.set_password(password)
            user.save()
            
        return user
        
    def update(self, instance, validated_data):
        """
        Update and return an existing user instance with validated data.
        """
        # Handle password separately
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that includes additional user information in the response.
    
    This extends the default TokenObtainPairSerializer to include the user's
    id, username, and email in the token response.
    """
    def validate(self, attrs):
        """
        Validate user credentials and return token with user data.
        
        Args:
            attrs: Dictionary containing username and password
            
        Returns:
            Dictionary containing tokens and user data
            
        Raises:
            AuthenticationFailed: If credentials are invalid
        """
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        return data
