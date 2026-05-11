from django.urls import path
from .views import (
    CarBrandListView,
    CarBrandDetailView,
    CarModelListView,
)

urlpatterns = [
    path('brands/', CarBrandListView.as_view(), name='brand-list'),
    path('brands/<int:pk>/', CarBrandDetailView.as_view(), name='brand-detail'),
    path('models/', CarModelListView.as_view(), name='model-list'),
]