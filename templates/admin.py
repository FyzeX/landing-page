from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Template, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'template_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def template_count(self, obj):
        return obj.templates.count()
    template_count.short_description = 'Templates'


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'price', 'active', 
        'demo_available', 'download_count', 'created_at'
    ]
    list_filter = [
        'active', 'demo_available', 'category', 
        'created_at', 'updated_at'
    ]
    search_fields = ['title', 'description', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['download_count', 'created_at', 'updated_at', 'thumbnail_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'short_description', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'active')
        }),
        ('Files & Media', {
            'fields': ('file', 'thumbnail', 'thumbnail_preview')
        }),
        ('Features & Demo', {
            'fields': ('features', 'demo_available', 'demo_bot_token')
        }),
        ('Statistics', {
            'fields': ('download_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.thumbnail.url
            )
        return "No thumbnail"
    thumbnail_preview.short_description = 'Thumbnail Preview'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'template', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'template__title', 'comment']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'template')
