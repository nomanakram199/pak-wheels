from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ..serializers.login import LoginSerializer
from ..serializers.user import UserSerializer
from pak_wheels.users.services.auth_service import AuthService


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        access_token, refresh_token = AuthService.generate_tokens(user)

        return Response({
            "success": True,
            "data": {
                "user": UserSerializer(user).data,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }, status=status.HTTP_200_OK)
