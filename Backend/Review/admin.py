from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model"""
    
    list_display = [
        'id', 'user', 'product_link', 'rating_display', 'title', 
        'is_archived', 'is_verified_purchase', 'is_helpful', 'created_at'
    ]
    list_filter = [
        'rating', 'is_archived', 'is_verified_purchase', 
        'created_at', 'updated_at', 'product__category'
    ]
    search_fields = [
        'user__username', 'user__email', 'product__name', 
        'title', 'comment'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'rating_display', 
        'is_helpful', 'is_active'
    ]
    list_per_page = 25
    list_editable = ['is_archived', 'is_verified_purchase']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'product', 'user', 'rating', 'rating_display')
        }),
        ('Review Content', {
            'fields': ('title', 'comment')
        }),
        ('Status & Verification', {
            'fields': ('is_archived', 'is_verified_purchase', 'is_helpful', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def product_link(self, obj):
        """Create a link to the product admin page"""
        if obj.product:
            url = reverse('admin:Product_product_change', args=[obj.product.id])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return '-'
    product_link.short_description = 'Product'
    product_link.admin_order_field = 'product__name'
    
    def rating_display(self, obj):
        """Display rating as stars"""
        return format_html(
            '<span style="color: #ffc107;">{}</span>',
            obj.rating_display
        )
    rating_display.short_description = 'Rating'
    rating_display.admin_order_field = 'rating'
    
    def is_active(self, obj):
        """Display if review is active"""
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        else:
            return format_html('<span style="color: red;">✗ Archived</span>')
    is_active.short_description = 'Status'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user', 'product')
    
    def soft_delete_selected(self, request, queryset):
        """Custom action to soft delete selected reviews"""
        updated = queryset.update(is_archived=True)
        self.message_user(
            request, 
            f'{updated} review(s) were successfully archived.'
        )
    soft_delete_selected.short_description = "Archive selected reviews"
    
    def restore_selected(self, request, queryset):
        """Custom action to restore selected reviews"""
        updated = queryset.update(is_archived=False)
        self.message_user(
            request, 
            f'{updated} review(s) were successfully restored.'
        )
    restore_selected.short_description = "Restore selected reviews"
    
    actions = [soft_delete_selected, restore_selected]
    
    def has_delete_permission(self, request, obj=None):
        """Prevent hard deletion in admin"""
        return False
    
    def get_actions(self, request):
        """Remove the default delete action"""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# Customize admin site headers
admin.site.site_header = "DentalCom Admin"
admin.site.site_title = "DentalCom Admin Portal"
admin.site.index_title = "Welcome to DentalCom Administration"
