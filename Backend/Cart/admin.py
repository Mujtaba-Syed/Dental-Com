from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline admin for cart items"""
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'updated_at']
    fields = ['product', 'quantity', 'added_at', 'updated_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin for Cart model"""
    list_display = ['id', 'user', 'get_total_items', 'get_total_price', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        """Display total items in cart"""
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    def get_total_price(self, obj):
        """Display total price of cart"""
        return f"${obj.get_total_price():.2f}"
    get_total_price.short_description = 'Total Price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin for CartItem model"""
    list_display = ['id', 'cart', 'product', 'quantity', 'get_item_total', 'added_at', 'updated_at']
    list_filter = ['added_at', 'updated_at']
    search_fields = ['cart__user__username', 'product__name']
    readonly_fields = ['added_at', 'updated_at']
    
    def get_item_total(self, obj):
        """Display total price for this item"""
        return f"${obj.get_total_price():.2f}"
    get_item_total.short_description = 'Item Total'
