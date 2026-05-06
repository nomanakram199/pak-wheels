from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializer(self.user).data
        data['user'] = serializer
        return data

class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'full_name', 'phone', 'city']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            city=validated_data.get('city', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'full_name', 'phone', 'city')
        read_only_fields = ('id', 'email')