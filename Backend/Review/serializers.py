from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Review
from Product.serializers import ProductSerializer

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model in reviews"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model with full CRUD operations"""
    
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    rating_display = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'product', 'product_id', 'user', 'rating', 'rating_display',
            'title', 'comment', 'is_archived', 'is_verified_purchase',
            'is_helpful', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'is_helpful']
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value
    
    def validate_title(self, value):
        """Validate title is not empty and has reasonable length"""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value.strip()
    
    def validate_comment(self, value):
        """Validate comment is not empty and has reasonable length"""
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long.")
        return value.strip()
    
    def create(self, validated_data):
        """Create a new review"""
        # Extract user info and product_id from validated_data
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        product_id = validated_data.pop('product_id', None)
        
        if not username or not email:
            raise serializers.ValidationError("Username and email are required.")
        
        if not product_id:
            raise serializers.ValidationError("Product ID is required.")
        
        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': username.split()[0] if ' ' in username else username,
                'last_name': username.split()[-1] if ' ' in username and len(username.split()) > 1 else '',
            }
        )
        
        # If user already exists but email is different, update it
        if not created and user.email != email:
            user.email = email
            user.save(update_fields=['email'])
        
        # Check if user already reviewed this product
        if Review.objects.filter(product_id=product_id, user=user, is_archived=False).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        # Create the review with only valid Review model fields
        review = Review.objects.create(
            product_id=product_id,
            user=user,
            rating=validated_data.get('rating'),
            title=validated_data.get('title'),
            comment=validated_data.get('comment'),
            is_verified_purchase=validated_data.get('is_verified_purchase', False)
        )
        return review
    
    def update(self, instance, validated_data):
        """Update an existing review"""
        # Only allow updating if review is not archived
        if instance.is_archived:
            raise serializers.ValidationError("Cannot update an archived review.")
        
        # Update the review
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class ReviewCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating reviews with user info in body"""
    
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = ['product_id', 'rating', 'title', 'comment', 'is_verified_purchase', 'username', 'email']
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value
    
    def validate_title(self, value):
        """Validate title is not empty and has reasonable length"""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value.strip()
    
    def validate_comment(self, value):
        """Validate comment is not empty and has reasonable length"""
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long.")
        return value.strip()
    
    def validate_username(self, value):
        """Validate username - will create user if doesn't exist"""
        return value
    
    def validate_email(self, value):
        """Validate email format"""
        return value
    
    def create(self, validated_data):
        """Create a new review"""
        # Extract user info and product_id from validated_data
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        product_id = validated_data.pop('product_id', None)
        
        if not username or not email:
            raise serializers.ValidationError("Username and email are required.")
        
        if not product_id:
            raise serializers.ValidationError("Product ID is required.")
        
        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': username.split()[0] if ' ' in username else username,
                'last_name': username.split()[-1] if ' ' in username and len(username.split()) > 1 else '',
            }
        )
        
        # If user already exists but email is different, update it
        if not created and user.email != email:
            user.email = email
            user.save(update_fields=['email'])
        
        # Check if user already reviewed this product
        if Review.objects.filter(product_id=product_id, user=user, is_archived=False).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        # Create the review with only valid Review model fields
        review = Review.objects.create(
            product_id=product_id,
            user=user,
            rating=validated_data.get('rating'),
            title=validated_data.get('title'),
            comment=validated_data.get('comment'),
            is_verified_purchase=validated_data.get('is_verified_purchase', False)
        )
        return review

class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating reviews"""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'is_verified_purchase']
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value
    
    def validate_title(self, value):
        """Validate title is not empty and has reasonable length"""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value.strip()
    
    def validate_comment(self, value):
        """Validate comment is not empty and has reasonable length"""
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long.")
        return value.strip()

class ReviewListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing reviews"""
    
    user = UserSerializer(read_only=True)
    rating_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rating', 'rating_display', 'title', 'comment',
            'is_verified_purchase', 'is_helpful', 'created_at'
        ]
