from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from tournaments.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('teams.urls')),
    path('api/', include('tournaments.urls')),
    path('api/health/', health_check, name='health-check'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]