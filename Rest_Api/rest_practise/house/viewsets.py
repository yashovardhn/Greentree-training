from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import House
from .serializers import HouseSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsHouseManagerOrNone




class HouseViewSet(ModelViewSet):
    """
    A viewset for viewing and editing house instances.
    """
    queryset = House.objects.all()
    permission_classes = [IsHouseManagerOrNone]
    serializer_class = HouseSerializer

    @action(detail=True, methods=['post'], name='Join', permission_classes=[])
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            user = request.user.profile
            if user_profile.house is None:
                user_profile.house = house
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif user_profile in house.members.all():
                return Response({"detail": "You are already a member of this house."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "You are already a member of another house."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'], name='Leave', permission_classes=[])
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if user_profile.house == house:
                user_profile.house = None
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif user_profile in house.members.all():
                house.members.remove(user_profile)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "You are not a member of this house."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()