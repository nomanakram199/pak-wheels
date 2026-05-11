from django.contrib import admin
from .models import CarListing, CarImage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'brand', 'model', 'year', 'price', 'city', 'created')
    list_filter = ('brand', 'model', 'city', 'created')
    search_fields = ('title', 'description', 'city', 'seller__full_name')
    inlines = [CarImageInline]

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image', 'is_primary', 'created')
