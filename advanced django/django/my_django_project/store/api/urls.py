from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')

app_name = 'books_api'

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
