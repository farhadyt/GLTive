# Purpose: Versioned API URL routing for the GLTive platform
"""
GLTive API URL Configuration
All module APIs are namespaced under /api/v1/.
"""
from django.urls import include, path


# TODO: Include module-level URL configs as they are implemented
# Example:
#   path("v1/stock/", include("modules.stock.api.urls")),

urlpatterns = [
    # API v1 namespace — module routes will be added here
    path("v1/auth/", include("core.auth.urls")),
]
