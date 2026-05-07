from rest_framework import serializers
from .models import CarListing, CarImage


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('id', 'image', 'is_primary', 'created')
        read_only_fields = ('id', 'created')

class CarListingSerializer(serializers.ModelSerializer):
    """For listing details — includes nested images and seller info."""
    images = CarImageSerializer(many=True, read_only=True)
    seller_name = serializers.CharField(source='seller.full_name', read_only=True)
    seller_phone = serializers.CharField(source='seller.phone', read_only=True)
    class Meta:
        model = CarListing
        fields = (
            'id', 'seller', 'seller_name', 'seller_phone',
            'title', 'brand', 'model', 'year', 'price', 'city',
            'description', 'images', 'created', 'modified'
        )
        read_only_fields = ('id', 'seller', 'created', 'modified')

class CarListingCreateSerializer(serializers.ModelSerializer):
    """For creating/updating a listing — simpler payload."""
    class Meta:
        model = CarListing
        fields = ('id', 'title', 'brand', 'model', 'year', 'price', 'city', 'description')