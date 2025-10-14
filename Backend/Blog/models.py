from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse


class BlogPost(models.Model):
    """Blog post model with SEO optimization features"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic fields
    title = models.CharField(max_length=200, help_text="Blog post title")
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="URL-friendly version of title")
    description = models.TextField(help_text="Short description/excerpt of the blog post")
    content = models.TextField(help_text="Full blog post content")
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True, help_text="Featured image for the blog post")
    
    # SEO fields
    meta_title = models.CharField(
        max_length=60, 
        blank=True, 
        help_text="SEO title (max 60 characters for optimal search results)"
    )
    meta_description = models.CharField(
        max_length=160, 
        blank=True, 
        help_text="SEO meta description (max 160 characters for optimal search results)"
    )
    meta_keywords = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Comma-separated keywords for SEO (e.g., 'dental, health, care')"
    )
    
    # Additional fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey('BlogCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
    tags = models.ManyToManyField('BlogTag', blank=True, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text="Mark as featured post")
    view_count = models.PositiveIntegerField(default=0, help_text="Number of times this post has been viewed")
    number_of_likes = models.PositiveIntegerField(default=0, help_text="Number of times this post has been liked")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generate meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title[:60]
        
        if not self.meta_description:
            self.meta_description = self.description[:160]
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})
    
    def get_keywords_list(self):
        """Return meta keywords as a list"""
        if self.meta_keywords:
            return [keyword.strip() for keyword in self.meta_keywords.split(',') if keyword.strip()]
        return []
    
    def increment_view_count(self):
        """Increment the view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def increment_like_count(self):
        """Increment the like count"""
        self.number_of_likes += 1
        self.save(update_fields=['number_of_likes'])


class BlogCategory(models.Model):
    """Category model for blog posts"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogTag(models.Model):
    """Tag model for blog posts"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blog Tags'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
