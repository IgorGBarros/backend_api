from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

admin.site.register(CustomUser, CustomUserAdmin)