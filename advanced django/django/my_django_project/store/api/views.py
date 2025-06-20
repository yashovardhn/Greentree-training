from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(detail=False, methods=['get'])
    def list_books(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'count': len(serializer.data),
            'data': serializer.data
        })
