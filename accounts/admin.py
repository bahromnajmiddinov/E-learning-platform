from django.contrib import admin

from .models import CustomUser, Balance


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_active']


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'points']
