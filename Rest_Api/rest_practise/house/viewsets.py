from rest_framework.viewsets import ModelViewSet
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
    

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()