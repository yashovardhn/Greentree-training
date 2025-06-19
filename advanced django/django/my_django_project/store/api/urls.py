from django.urls import path
from . import views

app_name = 'books_api'

urlpatterns = [
    path('books/', views.BookListCreateView.as_view(), name='book-list'),
]
