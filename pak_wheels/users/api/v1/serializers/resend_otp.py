from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return value
