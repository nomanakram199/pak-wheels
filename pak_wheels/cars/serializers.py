from rest_framework import serializers
from .models import CarBrand, CarModel


class CarModelSerializer(serializers.ModelSerializer):
    """Model serializer for model list endpoints."""
    class Meta:
        model = CarModel
        fields = ('id', 'name', 'brand', 'is_active')

class CarModelNestedSerializer(serializers.ModelSerializer):
    """Model serializer for nesting inside a brand (brand is implied)."""
    class Meta:
        model = CarModel
        fields = ('id', 'name', 'is_active')


class CarBrandSerializer(serializers.ModelSerializer):
    """Brand list view — no nested models (lightweight)."""
    models_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CarBrand
        fields = ('id', 'name', 'slug', 'logo', 'models_count', 'is_active')


class CarBrandDetailSerializer(serializers.ModelSerializer):
    """Brand detail view — includes all models (for dropdown)."""
    models = CarModelNestedSerializer(many=True, read_only=True)

    class Meta:
        model = CarBrand
        fields = ('id', 'name', 'slug', 'logo', 'models')
