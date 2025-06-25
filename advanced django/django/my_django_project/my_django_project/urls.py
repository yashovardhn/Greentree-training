from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenRefreshView
from store.views import CustomTokenObtainPairView, RegisterView, UserProfileDetail, UserProfileList
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Schema view for API documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Store API",
      default_version='v1',
      description="API documentation for the Store application",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='api-docs'),
    
    # API endpoints
    path('api/', include('store.api.urls')),  # Include our API URLs
    
    # Authentication endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    
    # User profile endpoints
    path('api/profile/', UserProfileDetail.as_view(), name='profile-detail'),
    path('api/profiles/', UserProfileList.as_view(), name='profile-list'),
]