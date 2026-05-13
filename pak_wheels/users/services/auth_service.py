from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
import random
import string
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthService:

    @staticmethod
    def signup(email, password, first_name, last_name, phone_number, city):
        """Create new user with OTP verification. Returns: (user, otp)"""
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            city=city,
            is_verified=False
        )

        otp = AuthService.generate_otp()
        user.otp = otp
        user.otp_expires_at = timezone.now() + timedelta(minutes=5)
        user.save()

        return user, otp

    @staticmethod
    def generate_tokens(user):
        """Generate JWT tokens for verified user. Returns: (access_token, refresh_token)"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token), str(refresh)

    @staticmethod
    def verify_otp(email, otp):
        """Verify OTP and mark user as verified. Returns: user or None"""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if not user.otp or user.otp != otp:
            return None

        if user.otp_expires_at < timezone.now():
            return None

        user.is_verified = True
        user.otp = None
        user.otp_expires_at = None
        user.save()

        return user

    @staticmethod
    def resend_otp(email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        otp = AuthService.generate_otp()
        user.otp = otp
        user.otp_expires_at = timezone.now() + timedelta(minutes=5)
        user.save()

        return user, otp

    @staticmethod
    def generate_otp():
        """Generate 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))

    @staticmethod
    def send_otp_email(email, otp):
        """Send OTP via email (mock for dev). Later: integrate SendGrid, AWS SES."""
        print(f"📧 OTP Email to {email}: {otp}")
