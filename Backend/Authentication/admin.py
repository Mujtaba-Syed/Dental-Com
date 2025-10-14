from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_guest', 'google_id', 'is_active', 'created_at']
    list_filter = ['is_guest', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'google_id', 'guest_session_id']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('is_guest', 'google_id', 'profile_picture', 'guest_session_id')
        }),
    )
