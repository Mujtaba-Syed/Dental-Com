from django.db import models
from django.conf import settings
from Product.models import Product

# Create your models here.

class Cart(models.Model):
    """
    Shopping cart model
    Each user has one cart
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f"Cart of {self.user}"
    
    def get_total_price(self):
        """Calculate total price of all items in cart"""
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Cart item model
    Represents a product in the cart with quantity
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart"
    
    def get_total_price(self):
        """Calculate total price for this cart item"""
        return self.product.get_sale_price() * self.quantity
