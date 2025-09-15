from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, BlogCategory, BlogTag


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'author', 'status', 'featured', 'view_count', 
        'created_at', 'published_at', 'seo_preview'
    ]
    list_filter = ['status', 'featured', 'created_at', 'published_at', 'author']
    search_fields = ['title', 'description', 'content', 'meta_keywords']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'seo_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'content', 'image', 'author')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'seo_preview'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'published_at'),
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['tags']
    
    def seo_preview(self, obj):
        """Display SEO preview in admin"""
        if not obj.pk:
            return "Save the post to see SEO preview"
        
        meta_title = obj.meta_title or obj.title
        meta_description = obj.meta_description or obj.description
        
        return format_html(
            '<div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0;">'
            '<h3 style="color: #1a0dab; margin: 0 0 5px 0; font-size: 18px;">{}</h3>'
            '<p style="color: #006621; margin: 0 0 5px 0; font-size: 14px;">{}</p>'
            '<p style="color: #545454; margin: 0; font-size: 13px;">Keywords: {}</p>'
            '</div>',
            meta_title[:60] + ('...' if len(meta_title) > 60 else ''),
            meta_description[:160] + ('...' if len(meta_description) > 160 else ''),
            obj.meta_keywords or 'None'
        )
    
    seo_preview.short_description = "SEO Preview"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category').prefetch_related('tags')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)
