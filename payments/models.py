from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Payment(models.Model):
    """
    Payment model for tracking payment transactions
    """
    PAYMENT_METHOD_CHOICES = [
        ('telegram', 'Telegram Payments'),
        ('crypto_btc', 'Bitcoin'),
        ('crypto_eth', 'Ethereum'),
        ('crypto_usdt', 'USDT'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        'orders.Order', 
        on_delete=models.CASCADE, 
        related_name='payment'
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES
    )
    transaction_id = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="External transaction ID"
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    gateway_response = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="Response from payment gateway"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount} {self.currency}"
    
    @property
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'completed'
