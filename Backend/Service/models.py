from django.db import models
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    alt_text = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Service Image'
        verbose_name_plural = 'Service Images'

    def __str__(self):
        return f"{self.service.name} - Image {self.id}"
    