from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category','on_sale')
        }),
        ('Pricing', {
            'fields': ('price','sale_price','sale_start','sale_end')
        }),
        ('Status', {
            'fields': ('is_active','is_featured','is_new','is_best_seller','is_top_rated')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id','product', 'is_primary', 'alt_text', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
