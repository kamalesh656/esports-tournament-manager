from django.contrib import admin
from django.urls import path, include
from tournaments.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('teams.urls')),
    path('api/', include('tournaments.urls')),
    path('api/health/', health_check, name='health-check'),
]