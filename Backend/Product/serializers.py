from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'category',
            'is_active', 'created_at', 'updated_at', 'images', 'primary_image'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None

class ProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'category',
            'is_active', 'created_at', 'primary_image'
        ]
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return {
                'id': primary_image.id,
                'image': primary_image.image.url,
                'alt_text': primary_image.alt_text
            }
        return None

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'category',
            'is_active', 'images'
        ]
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        
        return product
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        
        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update images if provided
        if images_data:
            # Clear existing images
            instance.images.all().delete()
            # Add new images
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)
        
        return instance
