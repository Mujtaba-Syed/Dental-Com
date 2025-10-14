from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from Product.models import Product

# Create your models here.

class Review(models.Model):
    """Model for product reviews with soft delete functionality"""
    
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    # Basic fields
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200, help_text="Review title")
    comment = models.TextField(help_text="Detailed review comment")
    
    # Status fields
    is_archived = models.BooleanField(default=False, help_text="Soft delete flag")
    is_verified_purchase = models.BooleanField(default=False, help_text="Whether user purchased this product")
    is_helpful = models.PositiveIntegerField(default=0, help_text="Number of helpful votes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        # Ensure one review per user per product
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} stars)"
    
    def soft_delete(self):
        """Soft delete the review by setting is_archived to True"""
        self.is_archived = True
        self.save(update_fields=['is_archived'])
    
    def restore(self):
        """Restore the review by setting is_archived to False"""
        self.is_archived = False
        self.save(update_fields=['is_archived'])
    
    @property
    def rating_display(self):
        """Return rating as star display"""
        if self.rating is None:
            return '☆' * 5  # Show empty stars if no rating yet
        return '★' * self.rating + '☆' * (5 - self.rating)
    
    @property
    def is_active(self):
        """Check if review is active (not archived)"""
        return not self.is_archived


class ReviewImage(models.Model):
    """Model for review images"""
    review = models.ForeignKey(Review, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='reviews/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Review Image'
        verbose_name_plural = 'Review Images'

    def __str__(self):
        return f"{self.review.user.username} - {self.review.product.name} - Image {self.id}"