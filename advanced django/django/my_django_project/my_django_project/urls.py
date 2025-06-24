from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from store.views import CustomTokenObtainPairView, RegisterView, UserProfileDetail, UserProfileList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.api.urls')),  # Include our API URLs
    
    # Authentication endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    
    # User profile endpoints
    path('api/profile/', UserProfileDetail.as_view(), name='profile-detail'),
    path('api/profiles/', UserProfileList.as_view(), name='profile-list'),
]