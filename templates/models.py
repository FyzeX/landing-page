from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import os

User = get_user_model()


def template_upload_path(instance, filename):
    """Generate upload path for template files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('templates', 'files', filename)


def template_thumbnail_path(instance, filename):
    """Generate upload path for template thumbnails"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('templates', 'thumbnails', filename)


class Category(models.Model):
    """
    Category model for organizing bot templates
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('templates:category', kwargs={'slug': self.slug})


class Template(models.Model):
    """
    Bot template model with all necessary information
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(
        max_length=300, 
        help_text="Brief description for catalog cards"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='templates'
    )
    file = models.FileField(
        upload_to=template_upload_path,
        help_text="ZIP file containing bot template"
    )
    thumbnail = models.ImageField(
        upload_to=template_thumbnail_path,
        blank=True,
        null=True,
        help_text="Thumbnail image for the template"
    )
    features = models.JSONField(
        default=list,
        help_text="List of template features"
    )
    demo_available = models.BooleanField(
        default=False,
        help_text="Whether demo bot can be generated"
    )
    demo_bot_token = models.CharField(
        max_length=200,
        blank=True,
        help_text="Bot token for demo generation"
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    download_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('templates:detail', kwargs={'slug': self.slug})
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    @property
    def review_count(self):
        """Get total number of reviews"""
        return self.reviews.count()


class Review(models.Model):
    """
    Review model for template feedback
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    template = models.ForeignKey(
        Template, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'template']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.template.title} ({self.rating}/5)"
