# Purpose: Root URL configuration for GLTive platform
"""GLTive root URL configuration."""
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("api/", include(("api.urls", "api"), namespace="api")),
]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            path("__debug__/", include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
