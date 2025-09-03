from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extended user model with additional fields for Telegram Market Bot
    """
    telegram_username = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Telegram username without @"
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email or self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
