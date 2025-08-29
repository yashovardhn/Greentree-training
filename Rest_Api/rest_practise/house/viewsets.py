from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend # type: ignore

from .models import House
from .serializers import HouseSerializer
from .permissions import IsHouseManagerOrNone

class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsHouseManagerOrNone]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['points', 'completed_tasks_count', 'not_completed_tasks_count']
    filterset_fields = ['members']

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action in ['create']:
    #         permission_classes = [IsAdminUser]
    #     elif self.action in ['update', 'partial_update', 'destroy', 'remove_member']:
    #         # Only house manager can update/delete the house or remove members
    #         permission_classes = [IsAuthenticated, IsHouseManagerOrNone]
    #     elif self.action in ['join', 'leave']:
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         # Default to read-only for list and retrieve actions
    #         permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #     return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], name='Join')
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile

            if user_profile in house.members.all():
                return Response(
                    {"detail": "You are already a member of this house."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user_profile.house and user_profile.house != house:
                return Response(
                    {"detail": "You are already a member of another house. Leave that house first."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            house.members.add(user_profile)
            user_profile.house = house
            user_profile.save()

            return Response({"detail": "Successfully joined the house."}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in join action: {e}")
            return Response({"detail": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], name='Leave')
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile

            if user_profile in house.members.all():
                house.members.remove(user_profile)
                if user_profile.house == house:
                    user_profile.house = None
                    user_profile.save()

                return Response({"detail": "Successfully left the house."}, status=status.HTTP_200_OK)

            return Response(
                {"detail": "You are not a member of this house."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print(f"Error in leave action: {e}")
            return Response({"detail": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], name='Remove Member')
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            user_id = request.data.get('user_id')

            if not user_id:
                return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, id=user_id)
            user_profile = user.profile

            if user_profile in house.members.all():
                house.members.remove(user_profile)
                if user_profile.house == house:
                    user_profile.house = None
                    user_profile.save()

                return Response({"detail": "User removed from house."}, status=status.HTTP_200_OK)

            return Response(
                {"detail": "User is not a member of this house."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print(f"Error in remove_member action: {e}")
            return Response({"detail": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
