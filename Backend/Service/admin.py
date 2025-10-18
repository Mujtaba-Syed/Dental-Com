import logging
from django.contrib import admin
from django.db import transaction
from .models import Service, ServiceImage

logger = logging.getLogger(__name__)

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fields = ['image', 'alt_text', 'order']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'is_featured', 'is_new', 'created_at']
    list_filter = ['is_active', 'is_featured', 'is_new', 'created_at']
    search_fields = ['name', 'description', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active', 'is_featured', 'is_new']
    inlines = [ServiceImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Status & Features', {
            'fields': ('is_active', 'is_featured', 'is_new')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['service', 'image', 'order', 'created_at']
    list_filter = ['created_at', 'service']
    search_fields = ['service__name', 'alt_text']
    list_editable = ['order']
