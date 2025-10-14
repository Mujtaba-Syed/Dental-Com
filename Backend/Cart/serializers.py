from rest_framework import serializers
from .models import Cart, CartItem
from Product.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images"""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']


class CartProductSerializer(serializers.ModelSerializer):
    """Serializer for product details in cart"""
    images = ProductImageSerializer(many=True, read_only=True)
    current_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'sale_price', 'on_sale', 
                  'current_price', 'images', 'category']
    
    def get_current_price(self, obj):
        """Get the current selling price (sale price if on sale, otherwise regular price)"""
        return obj.get_sale_price()


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    product = CartProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 
                  'added_at', 'updated_at']
        read_only_fields = ['id', 'added_at', 'updated_at']
    
    def get_total_price(self, obj):
        """Calculate total price for this cart item"""
        return obj.get_total_price()
    
    def validate_quantity(self, value):
        """Validate that quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value


class CartSerializer(serializers.ModelSerializer):
    """Serializer for cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'total_items', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_total_price(self, obj):
        """Calculate total price of all items in cart"""
        return obj.get_total_price()
    
    def get_total_items(self, obj):
        """Get total number of items in cart"""
        return obj.get_total_items()


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
    
    def validate_product_id(self, value):
        """Validate that product exists and is active"""
        try:
            product = Product.objects.get(id=value)
            if not product.is_active:
                raise serializers.ValidationError("This product is not available.")
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating cart item quantity"""
    quantity = serializers.IntegerField(min_value=1)

