# Purpose: Wrapped REST framework JWT endpoints providing platform-standard JSON envelopes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from core.auth.serializers import CustomTokenObtainPairSerializer, LogoutSerializer


class LoginView(TokenObtainPairView):
    """
    Authenticates a user and returns enveloped access and refresh tokens.
    """
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response({
            "success": True,
            "message": "login_successful",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):
    """
    Takes a refresh token and returns a new enveloped access token.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response({
            "success": True,
            "message": "token_refreshed",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Blacklists the provided refresh token.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "success": True,
                "message": "logout_successful"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "error": {
                    "code": "invalid_token",
                    "message": str(e)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
