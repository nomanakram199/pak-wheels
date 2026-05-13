from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ..serializers.verify_otp import VerifyOTPSerializer
from pak_wheels.users.services.auth_service import AuthService


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        user = AuthService.verify_otp(user.email, serializer.validated_data['otp'])

        if not user:
            return Response({
                "success": False,
                "error": "OTP verification failed"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "data": {
                "message": "Email verified successfully"
            }
        }, status=status.HTTP_200_OK)
