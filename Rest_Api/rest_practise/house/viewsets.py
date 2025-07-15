from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# Assuming your models and serializers are correctly imported
from .models import House
from .serializers import HouseSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsHouseManagerOrNone

class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    # The get_permissions method will override this for specific actions
    permission_classes = [IsHouseManagerOrNone] 
    serializer_class = HouseSerializer

    @action(detail=True, methods=['post'], name='Join', permission_classes=[])
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            current_user_profile = request.user.profile

            # 1. Check if the user is already a member of THIS specific house (via ManyToManyField)
            if current_user_profile in house.members.all():
                return Response({"detail": "You are already a member of this house."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 2. Check if the user is associated with ANY other primary house (via ForeignKey/OneToOneField like user.profile.house)
            # This check applies if a user is meant to be in only one 'primary' house at a time.
            if hasattr(current_user_profile, 'house') and \
               current_user_profile.house is not None and \
               current_user_profile.house != house: # Ensure it's a *different* house
                 return Response({"detail": "You are already a member of another house. Leave that house first."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 3. If none of the above conditions are met, the user can join this house.
            # Add user to the house's ManyToManyField for members
            house.members.add(current_user_profile)
            
            # If Profile has a ForeignKey/OneToOneField to House (e.g., current_user_profile.house), update it
            if hasattr(current_user_profile, 'house'):
                current_user_profile.house = house
            
            current_user_profile.save() # Save the profile if its 'house' field was updated

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            # Log the actual exception for debugging in development
            print(f"Error in join action: {e}") 
            return Response({"detail": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'], name='Leave', permission_classes=[])
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if user_profile in house.members.all():
                house.members.remove(user_profile)
                # If Profile has a ForeignKey/OneToOneField to House, clear it when leaving
                if hasattr(user_profile, 'house') and user_profile.house == house:
                    user_profile.house = None 
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "You are not a member of this house."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in leave action: {e}")
            return Response({"detail": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['join', 'leave']:
            # Require authentication for joining/leaving a house
            self.permission_classes = [IsAuthenticated] 
        # For 'list', 'retrieve', etc., it will use the default [IsHouseManagerOrNone]
        return super().get_permissions()