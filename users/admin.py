from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('telegram_username',)
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('telegram_username', 'email', 'first_name', 'last_name')
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'telegram_username', 'is_staff']
    list_filter = BaseUserAdmin.list_filter + ('created_at',)
    search_fields = ['username', 'email', 'telegram_username', 'first_name', 'last_name']
