from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.db.models import Count
from .models import CarBrand, CarModel
from .serializers import (
    CarBrandSerializer,
    CarBrandDetailSerializer,
    CarModelSerializer,
)


class CarBrandListView(generics.ListAPIView):
    """
    GET /api/cars/brands/
    List all brands (public).
    """
    def get_queryset(self):
        return CarBrand.objects.annotate(models_count=Count('models'))
    serializer_class = CarBrandSerializer
    permission_classes = [permissions.AllowAny]


class CarBrandDetailView(generics.RetrieveAPIView):
    """
    GET /api/cars/brands/<id>/
    Get brand details with all its models nested.
    """
    def get_queryset(self):
        return CarBrand.objects.prefetch_related('models')
    serializer_class = CarBrandDetailSerializer
    permission_classes = [permissions.AllowAny]


class CarModelListView(generics.ListAPIView):
    """
    GET /api/cars/models/?brand=<brand_id>
    List all models, optionally filtered by brand.
    This is what powers cascading dropdowns!
    """
    serializer_class = CarModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = CarModel.objects.select_related('brand').order_by('name')
        brand_id = self.request.query_params.get('brand')
        if brand_id:
            try:
                queryset = queryset.filter(brand_id=int(brand_id))
            except ValueError:
                raise ValidationError({'brand': 'Invalid brand ID'})
        return queryset
