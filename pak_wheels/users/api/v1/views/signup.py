from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ..serializers.signup import SignupSerializer
from ..serializers.user import UserSerializer
from pak_wheels.users.services.auth_service import AuthService


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user, otp = AuthService.signup(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                phone_number=serializer.validated_data['phone_number'],
                city=serializer.validated_data['city']
            )

            AuthService.send_otp_email(user.email, otp)

            return Response({
                "success": True,
                "data": {
                    "user": UserSerializer(user).data,
                    "message": "Signup successful. Check your email for OTP."
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
