from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.contrib.auth.models import User

from .models import Review
from .serializers import (
    ReviewSerializer, 
    ReviewCreateSerializer, 
    ReviewUpdateSerializer, 
    ReviewListSerializer
)
from Product.models import Product


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET: List all reviews for a specific product
    POST: Create a new review for a product
    """
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewListSerializer
    
    def get_queryset(self):
        """Filter reviews by product and exclude archived ones"""
        product_id = self.kwargs.get('product_id')
        queryset = Review.objects.filter(
            product_id=product_id,
            is_archived=False
        ).select_related('user', 'product')
        
        # Optional filtering by rating
        rating = self.request.query_params.get('rating', None)
        if rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    queryset = queryset.filter(rating=rating)
            except ValueError:
                pass
        
        # Optional filtering by verified purchase
        verified = self.request.query_params.get('verified', None)
        if verified and verified.lower() == 'true':
            queryset = queryset.filter(is_verified_purchase=True)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Get all reviews for a product with additional statistics"""
        queryset = self.get_queryset()
        
        # Get product information
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate review statistics
        total_reviews = queryset.count()
        avg_rating = queryset.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        rating_distribution = queryset.values('rating').annotate(count=Count('rating')).order_by('rating')
        
        # Serialize reviews
        serializer = self.get_serializer(queryset, many=True)
        
        response_data = {
            'product': {
                'id': product.id,
                'name': product.name,
                'slug': product.slug
            },
            'statistics': {
                'total_reviews': total_reviews,
                'average_rating': round(avg_rating, 2),
                'rating_distribution': list(rating_distribution)
            },
            'reviews': serializer.data
        }
        
        return Response(response_data)
    
    def create(self, request, *args, **kwargs):
        """Create a new review for a product"""
        # Check if product exists
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            # Return full review data
            full_serializer = ReviewSerializer(review, context={'request': request})
            return Response(full_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific review
    PUT/PATCH: Update a specific review
    DELETE: Soft delete a review (set is_archived=True)
    """
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReviewUpdateSerializer
        return ReviewSerializer
    
    def get_queryset(self):
        """Get reviews for the product"""
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(
            product_id=product_id,
            is_archived=False
        ).select_related('user', 'product')
    
    def get_object(self):
        """Get the review object"""
        review_id = self.kwargs.get('review_id')
        product_id = self.kwargs.get('product_id')
        
        return get_object_or_404(
            Review,
            id=review_id,
            product_id=product_id,
            is_archived=False
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific review"""
        review = self.get_object()
        serializer = self.get_serializer(review)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update a specific review"""
        # Get username and email from request body
        username = request.data.get('username')
        email = request.data.get('email')
        
        if not username or not email:
            return Response(
                {'error': 'Username and email are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        review = self.get_object()
        
        # Check if username and email match the review's user
        if review.user.username != username or review.user.email != email:
            return Response(
                {'error': 'Invalid username or email. You can only update your own reviews'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(review, data=request.data, partial=kwargs.get('partial', False))
        
        if serializer.is_valid():
            serializer.save()
            # Return full review data
            full_serializer = ReviewSerializer(review, context={'request': request})
            return Response(full_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete a review by setting is_archived=True"""
        # Get username and email from request body
        username = request.data.get('username')
        email = request.data.get('email')
        
        if not username or not email:
            return Response(
                {'error': 'Username and email are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        review = self.get_object()
        
        # Check if username and email match the review's user
        if review.user.username != username or review.user.email != email:
            return Response(
                {'error': 'Invalid username or email. You can only delete your own reviews'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        review.soft_delete()
        
        return Response(
            {'message': 'Review has been archived successfully'}, 
            status=status.HTTP_200_OK
        )


class UserReviewListView(generics.ListAPIView):
    """
    GET: List all reviews by the authenticated user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewListSerializer
    
    def get_queryset(self):
        """Get all reviews by the authenticated user"""
        return Review.objects.filter(
            user=self.request.user,
            is_archived=False
        ).select_related('product').order_by('-created_at')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_review_helpful(request, product_id, review_id):
    """
    Mark a review as helpful
    """
    try:
        review = Review.objects.get(
            id=review_id,
            product_id=product_id,
            is_archived=False
        )
        
        # Increment helpful count
        review.is_helpful += 1
        review.save(update_fields=['is_helpful'])
        
        return Response({
            'message': 'Review marked as helpful',
            'helpful_count': review.is_helpful
        }, status=status.HTTP_200_OK)
        
    except Review.DoesNotExist:
        return Response(
            {'error': 'Review not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def product_review_stats(request, product_id):
    """
    Get review statistics for a product
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    reviews = Review.objects.filter(product=product, is_archived=False)
    
    stats = {
        'product': {
            'id': product.id,
            'name': product.name,
            'slug': product.slug
        },
        'total_reviews': reviews.count(),
        'average_rating': reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
        'rating_distribution': list(reviews.values('rating').annotate(count=Count('rating')).order_by('rating')),
        'verified_purchases': reviews.filter(is_verified_purchase=True).count(),
        'recent_reviews': ReviewListSerializer(
            reviews.order_by('-created_at')[:5], 
            many=True
        ).data
    }
    
    return Response(stats)
