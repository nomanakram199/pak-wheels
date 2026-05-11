from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'phone', 'is_staff')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('full_name', 'phone', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('full_name', 'phone', 'profile_picture')}),
    )
