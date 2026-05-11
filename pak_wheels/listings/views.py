from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import ProtectedError
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import CarListing, CarImage
from .serializers import (
    CarListingSerializer,
    CarListingCreateSerializer,
    CarImageSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only the seller can edit/delete their own listing."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller == request.user



class CarListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/listings/?brand=<id>&model=<id>&city=<name>
    POST /api/listings/
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarListingCreateSerializer
        return CarListingSerializer

    def get_queryset(self):
        queryset = CarListing.objects.select_related(
            'brand', 'model', 'seller'
        ).prefetch_related('images')

        # Filter by brand
        brand_id = self.request.query_params.get('brand')
        if brand_id:
            try:
                queryset = queryset.filter(brand_id=int(brand_id))
            except ValueError:
                raise ValidationError({'brand': 'Invalid brand ID'})
        # Filter by model
        model_id = self.request.query_params.get('model')
        if model_id:
            try:
                queryset = queryset.filter(model_id=int(model_id))
            except ValueError:
                raise ValidationError({'model': 'Invalid model ID'})

        # Filter by city
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class CarListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarListingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return CarListingCreateSerializer
        return CarListingSerializer

    def get_queryset(self):
        return CarListing.objects.select_related(
            'brand', 'model', 'seller'
        ).prefetch_related('images')

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'error': 'Cannot delete this resource because it is protected.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MyListingsView(generics.ListAPIView):
    serializer_class = CarListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CarListing.objects.filter(seller=self.request.user)

class CarImageUploadView(generics.CreateAPIView):
    serializer_class = CarImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        listing_id = self.kwargs["listing_id"]

        listing = get_object_or_404(CarListing, id=listing_id)

        if listing.seller != self.request.user:
            raise PermissionDenied("You don't own this listing")

        serializer.save(listing=listing)

class CarImageDeleteView(generics.DestroyAPIView):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.listing.seller != self.request.user:
            raise PermissionDenied("You don't own this listing")
        instance.delete()
