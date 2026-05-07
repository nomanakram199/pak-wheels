from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
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
    queryset = CarListing.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CarListingCreateSerializer
        return CarListingSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class CarListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarListing.objects.all()
    serializer_class = CarListingSerializer
    permission_classes = [IsOwnerOrReadOnly]


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