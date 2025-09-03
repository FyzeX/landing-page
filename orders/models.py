from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MinValueValidator
import uuid
import secrets

User = get_user_model()


class Order(models.Model):
    """
    Order model for tracking template purchases
    """
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('pending', 'Payment Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    template = models.ForeignKey(
        'templates.Template', 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='created'
    )
    download_token = models.CharField(
        max_length=64, 
        unique=True, 
        blank=True, 
        null=True
    )
    download_count = models.PositiveIntegerField(default=0)
    max_downloads = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.template.title}"
    
    def save(self, *args, **kwargs):
        if not self.download_token and self.status == 'completed':
            self.download_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'pk': self.pk})
    
    @property
    def can_download(self):
        """Check if user can still download the template"""
        return (
            self.status == 'completed' and 
            self.download_count < self.max_downloads and
            self.download_token
        )
    
    def increment_download_count(self):
        """Increment download count"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
