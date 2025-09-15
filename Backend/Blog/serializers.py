from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, BlogCategory, BlogTag


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for BlogCategory model"""
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']


class BlogTagSerializer(serializers.ModelSerializer):
    """Serializer for BlogTag model"""
    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost list view (simplified)"""
    author = UserSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'description', 'image', 'meta_title',
            'meta_description', 'author', 'status', 'featured', 'view_count', 'number_of_likes',
            'created_at', 'updated_at', 'published_at', 'category', 'tags'
        ]
        read_only_fields = ['id', 'slug', 'author', 'view_count', 'number_of_likes', 'created_at', 'updated_at']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost detail view (full content)"""
    author = UserSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    keywords_list = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'description', 'content', 'image',
            'meta_title', 'meta_description', 'meta_keywords', 'keywords_list',
            'author', 'status', 'featured', 'view_count', 'number_of_likes', 'created_at',
            'updated_at', 'published_at', 'category', 'tags'
        ]
        read_only_fields = ['id', 'slug', 'author', 'view_count', 'created_at', 'updated_at']
    
    def get_keywords_list(self, obj):
        """Return meta keywords as a list"""
        return obj.get_keywords_list()


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating BlogPost"""
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'description', 'content', 'image', 'meta_title',
            'meta_description', 'meta_keywords', 'status', 'featured',
            'category_id', 'tag_ids'
        ]
    
    def validate_meta_title(self, value):
        """Validate meta title length"""
        if value and len(value) > 60:
            raise serializers.ValidationError("Meta title should not exceed 60 characters.")
        return value
    
    def validate_meta_description(self, value):
        """Validate meta description length"""
        if value and len(value) > 160:
            raise serializers.ValidationError("Meta description should not exceed 160 characters.")
        return value
    
    def validate_meta_keywords(self, value):
        """Validate meta keywords format"""
        if value:
            keywords = [keyword.strip() for keyword in value.split(',') if keyword.strip()]
            if len(keywords) > 10:
                raise serializers.ValidationError("Maximum 10 keywords allowed.")
        return value
    
    def create(self, validated_data):
        """Create a new blog post"""
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        
        # Set author to the current user or admin if not authenticated
        if self.context['request'].user.is_authenticated:
            validated_data['author'] = self.context['request'].user
        else:
            # Get or create admin user as default author
            from django.contrib.auth.models import User
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            validated_data['author'] = admin_user
        
        # Create the blog post
        blog_post = BlogPost.objects.create(**validated_data)
        
        # Set category if provided
        if category_id:
            try:
                category = BlogCategory.objects.get(id=category_id)
                blog_post.category = category
                blog_post.save()
            except BlogCategory.DoesNotExist:
                pass
        
        # Set tags if provided
        if tag_ids:
            tags = BlogTag.objects.filter(id__in=tag_ids)
            blog_post.tags.set(tags)
        
        return blog_post
    
    def update(self, instance, validated_data):
        """Update an existing blog post"""
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', None)
        
        # Update the blog post
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update author if not authenticated (set to admin)
        if not self.context['request'].user.is_authenticated:
            from django.contrib.auth.models import User
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            instance.author = admin_user
        
        # Update category if provided
        if category_id is not None:
            if category_id:
                try:
                    category = BlogCategory.objects.get(id=category_id)
                    instance.category = category
                except BlogCategory.DoesNotExist:
                    pass
            else:
                instance.category = None
        
        # Update tags if provided
        if tag_ids is not None:
            if tag_ids:
                tags = BlogTag.objects.filter(id__in=tag_ids)
                instance.tags.set(tags)
            else:
                instance.tags.clear()
        
        instance.save()
        return instance


class BlogPostSearchSerializer(serializers.Serializer):
    """Serializer for blog post search functionality"""
    query = serializers.CharField(max_length=255, help_text="Search query")
    category = serializers.CharField(max_length=100, required=False, help_text="Filter by category slug")
    tag = serializers.CharField(max_length=50, required=False, help_text="Filter by tag slug")
    status = serializers.ChoiceField(choices=BlogPost.STATUS_CHOICES, required=False, help_text="Filter by status")
    featured = serializers.BooleanField(required=False, help_text="Filter featured posts")
    author = serializers.IntegerField(required=False, help_text="Filter by author ID")
