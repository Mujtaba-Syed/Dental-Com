from rest_framework import serializers
from .models import Service, ServiceImage

class ServiceImageSerializer(serializers.ModelSerializer):
    """ServiceImage serializer"""
    
    class Meta:
        model = ServiceImage
        fields = ['id', 'image', 'alt_text', 'order', 'created_at']

class ServiceSerializer(serializers.ModelSerializer):
    """Service serializer for GET API with images"""
    images = ServiceImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'


