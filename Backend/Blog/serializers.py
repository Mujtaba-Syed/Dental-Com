from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, BlogCategory, BlogTag


class UserSerializer(serializers.Serializer):
    """Custom serializer for User model to avoid DRF introspection issues"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, read_only=True)
    first_name = serializers.CharField(max_length=150, read_only=True)
    last_name = serializers.CharField(max_length=150, read_only=True)
    email = serializers.EmailField(read_only=True)


class BlogCategorySerializer(serializers.Serializer):
    """Custom serializer for BlogCategory model to avoid DRF introspection issues"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)
    slug = serializers.SlugField(max_length=100, read_only=True)
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class BlogTagSerializer(serializers.Serializer):
    """Custom serializer for BlogTag model to avoid DRF introspection issues"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50, read_only=True)
    slug = serializers.SlugField(max_length=50, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class BlogPostListSerializer(serializers.Serializer):
    """Custom serializer for BlogPost list view to avoid DRF introspection issues"""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=200, read_only=True)
    description = serializers.CharField()
    image = serializers.ImageField(read_only=True)
    meta_title = serializers.CharField(max_length=60, read_only=True)
    meta_description = serializers.CharField(max_length=160, read_only=True)
    author = UserSerializer(read_only=True)
    status = serializers.CharField(max_length=10, read_only=True)
    featured = serializers.BooleanField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    number_of_likes = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    published_at = serializers.DateTimeField(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags = serializers.SerializerMethodField()
    
    def get_tags(self, obj):
        """Get tags as a list of serialized tag data"""
        return BlogTagSerializer(obj.tags.all(), many=True).data


class BlogPostDetailSerializer(serializers.Serializer):
    """Custom serializer for BlogPost detail view to avoid DRF introspection issues"""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=200, read_only=True)
    description = serializers.CharField()
    content = serializers.CharField()
    image = serializers.ImageField(read_only=True)
    meta_title = serializers.CharField(max_length=60, read_only=True)
    meta_description = serializers.CharField(max_length=160, read_only=True)
    meta_keywords = serializers.CharField(max_length=255, read_only=True)
    keywords_list = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    status = serializers.CharField(max_length=10, read_only=True)
    featured = serializers.BooleanField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    number_of_likes = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    published_at = serializers.DateTimeField(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags = serializers.SerializerMethodField()
    
    def get_tags(self, obj):
        """Get tags as a list of serialized tag data"""
        return BlogTagSerializer(obj.tags.all(), many=True).data
    
    def get_keywords_list(self, obj):
        """Return meta keywords as a list"""
        return obj.get_keywords_list()


class BlogPostCreateUpdateSerializer(serializers.Serializer):
    """Custom serializer for creating and updating BlogPost to avoid DRF introspection issues"""
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    content = serializers.CharField()
    image = serializers.ImageField(required=False, allow_null=True)
    meta_title = serializers.CharField(max_length=60, required=False, allow_blank=True)
    meta_description = serializers.CharField(max_length=160, required=False, allow_blank=True)
    meta_keywords = serializers.CharField(max_length=255, required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=BlogPost.STATUS_CHOICES, default='draft')
    featured = serializers.BooleanField(default=False)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    
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
