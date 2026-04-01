# Purpose: Root URL configuration for GLTive platform
"""GLTive root URL configuration."""
from django.urls import include, path

urlpatterns = [
    path("api/", include(("api.urls", "api"), namespace="api")),
]
