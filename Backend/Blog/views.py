from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import BlogPost, BlogCategory, BlogTag
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer, BlogPostCreateUpdateSerializer,
    BlogCategorySerializer, BlogTagSerializer, BlogPostSearchSerializer
)


class AllowPostWithoutAuth(IsAuthenticatedOrReadOnly):
    """
    Custom permission that allows all requests without authentication
    """
    def has_permission(self, request, view):
        # Allow all methods without authentication
        return True


class BlogPostListCreateView(generics.ListCreateAPIView):
    """
    GET: List all blog posts
    POST: Create a new blog post
    """
    queryset = BlogPost.objects.select_related('author', 'category').prefetch_related('tags')
    permission_classes = [AllowPostWithoutAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'featured', 'author', 'category']
    search_fields = ['title', 'description', 'content', 'meta_keywords']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'view_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogPostCreateUpdateSerializer
        return BlogPostListSerializer
    
    def get_queryset(self):
        """Filter published posts for non-authenticated users and exclude archived posts"""
        queryset = super().get_queryset()
        # Exclude archived posts for all users
        queryset = queryset.exclude(status='archived')
        
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset


class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific blog post
    PUT/PATCH: Update a blog post
    DELETE: Archive a blog post (soft delete)
    """
    queryset = BlogPost.objects.select_related('author', 'category').prefetch_related('tags')
    lookup_field = 'id'
    permission_classes = [AllowPostWithoutAuth]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BlogPostCreateUpdateSerializer
        return BlogPostDetailSerializer
    
    def get_queryset(self):
        """Filter published posts for non-authenticated users and exclude archived posts"""
        queryset = super().get_queryset()
        # Exclude archived posts for all users
        queryset = queryset.exclude(status='archived')
        
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when retrieving a blog post"""
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete - change status to archived instead of deleting"""
        instance = self.get_object()
        
        # Update author to admin if not authenticated
        if not request.user.is_authenticated:
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
        
        instance.status = 'archived'
        instance.save(update_fields=['status', 'author'])
        return Response({'message': 'Blog post archived successfully'}, status=status.HTTP_200_OK)


class BlogPostSearchView(APIView):
    """
    POST: Search blog posts with advanced filters
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        serializer = BlogPostSearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data.get('query', '')
            category = serializer.validated_data.get('category')
            tag = serializer.validated_data.get('tag')
            status_filter = serializer.validated_data.get('status')
            featured = serializer.validated_data.get('featured')
            author = serializer.validated_data.get('author')
            
            # Build queryset
            queryset = BlogPost.objects.select_related('author', 'category').prefetch_related('tags')
            
            # Filter by status for non-authenticated users
            if not request.user.is_authenticated:
                queryset = queryset.filter(status='published')
            
            # Apply filters
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(content__icontains=query) |
                    Q(meta_keywords__icontains=query)
                )
            
            if category:
                queryset = queryset.filter(category__slug=category)
            
            if tag:
                queryset = queryset.filter(tags__slug=tag)
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            if featured is not None:
                queryset = queryset.filter(featured=featured)
            
            if author:
                queryset = queryset.filter(author_id=author)
            
            # Order by creation date
            queryset = queryset.order_by('-created_at')
            
            # Serialize results
            serializer = BlogPostListSerializer(queryset, many=True)
            return Response({
                'results': serializer.data,
                'count': queryset.count()
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeaturedBlogPostsView(generics.ListAPIView):
    """
    GET: List featured blog posts
    """
    queryset = BlogPost.objects.filter(featured=True, status='published').select_related('author', 'category').prefetch_related('tags')
    serializer_class = BlogPostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]






@api_view(['POST'])
@permission_classes([AllowPostWithoutAuth])
def increment_view_count(request, id):
    """
    Increment view count for a specific blog post
    """
    try:
        blog_post = get_object_or_404(BlogPost, id=id)
        
        if not request.user.is_authenticated:
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
            blog_post.author = admin_user
            blog_post.save(update_fields=['author'])
        
        blog_post.increment_view_count()
        return Response({'message': 'View count incremented successfully'})
    except BlogPost.DoesNotExist:
        return Response({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowPostWithoutAuth])
def increment_like_count(request, id):
    """
    Increment like count for a specific blog post
    """
    try:
        blog_post = get_object_or_404(BlogPost, id=id)
        if not request.user.is_authenticated:
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
            blog_post.author = admin_user
            blog_post.save(update_fields=['author'])
        blog_post.increment_like_count()
        return Response({'message': 'Like count incremented successfully'})
    except BlogPost.DoesNotExist:
        return Response({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowPostWithoutAuth])
def decrement_like_count(request, id):
    """
    Decrement like count for a specific blog post
    """
    try:
        blog_post = get_object_or_404(BlogPost, id=id)
        if not request.user.is_authenticated:
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
            blog_post.author = admin_user
            blog_post.save(update_fields=['author'])
        if blog_post.number_of_likes > 0:
            blog_post.number_of_likes -= 1
            blog_post.save(update_fields=['number_of_likes'])
        return Response({'message': 'Like count decremented successfully'})
    except BlogPost.DoesNotExist:
        return Response({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)
