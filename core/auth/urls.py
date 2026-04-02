# Purpose: Authentication API routing
from django.urls import path
from core.auth.views import LoginView, RefreshView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
