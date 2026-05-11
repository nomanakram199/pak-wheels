from django.urls import path
from .views import (
    CarListCreateView,
    CarListingDetailView,
    MyListingsView,
    CarImageUploadView,
    CarImageDeleteView,
)

urlpatterns = [
    # List and Create Car Ads
    path('', CarListCreateView.as_view(), name='car-list-create'),
    
    # User's own listings
    path('me/', MyListingsView.as_view(), name='my-listings'),
    
    # Detail, Update, Delete specific listing
    path('<int:pk>/', CarListingDetailView.as_view(), name='car-detail'),
    
    # Images
    path('<int:listing_id>/images/', CarImageUploadView.as_view(), name='image-upload'),
    path('images/<int:pk>/', CarImageDeleteView.as_view(), name='image-delete'),
]
