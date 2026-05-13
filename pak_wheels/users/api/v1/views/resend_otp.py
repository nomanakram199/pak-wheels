from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ..serializers.resend_otp import ResendOTPSerializer
from pak_wheels.users.services.auth_service import AuthService


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user, otp = AuthService.resend_otp(email)

        AuthService.send_otp_email(user.email, otp)

        return Response({
            "success": True,
            "data": {
                "message": "New OTP sent to your email"
            }
        }, status=status.HTTP_200_OK)
