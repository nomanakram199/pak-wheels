from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    city = serializers.CharField(max_length=100, required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def validate_phone_number(self, value):
        pattern = r'^((\+92)|0)?3[0-9]{9}$|^\+923[0-9]{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid Pakistan phone number")
        return value

    def validate(self, attrs):
        return attrs
