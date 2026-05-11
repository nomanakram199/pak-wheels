from rest_framework import serializers
from pak_wheels.cars.models import CarBrand, CarModel
from pak_wheels.cars.serializers import CarBrandSerializer, CarModelSerializer
from .models import CarListing, CarImage


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('id', 'image', 'is_primary', 'created')
        read_only_fields = ('id', 'created')

class CarListingSerializer(serializers.ModelSerializer):
    """For listing details — includes nested images and seller info."""
    images = CarImageSerializer(many=True, read_only=True)
    brand = CarBrandSerializer(read_only=True)
    model = CarModelSerializer(read_only=True)
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
    brand = serializers.PrimaryKeyRelatedField(queryset=CarBrand.objects.filter(is_active=True))
    model = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.filter(is_active=True))
    class Meta:
        model = CarListing
        fields = ('title', 'brand', 'model', 'year', 'price', 'city', 'description')


    def validate(self, data):
        brand = data.get('brand')
        model = data.get('model')

        if not brand or not model:
            return data
            
        if model.brand_id != brand.id:
            raise serializers.ValidationError({
                'model': 'Selected model does not belong to the selected brand.'
            })
        return data
