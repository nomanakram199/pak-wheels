from django.contrib import admin
from .models import CarBrand, CarModel

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'created')
    list_filter = ('brand',)
    search_fields = ('name', 'brand__name')
