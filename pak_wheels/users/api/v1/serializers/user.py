from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Response-only serializer for user data (no write logic)."""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'city', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified']
