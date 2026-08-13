from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class Client(AbstractUser):
    """
    Custom User model for Veritas Asset Recovery clients.
    Extends Django's AbstractUser with additional fields.
    """
    # UUID as primary key for security (don't expose sequential IDs)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Additional fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    telegram_handle = models.CharField(max_length=100, blank=True, null=True)
    
    # Tracking
    date_joined = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Legal agreements
    agreed_to_terms = models.BooleanField(default=False)
    agreed_to_nda = models.BooleanField(default=False)
    agreed_to_fee_structure = models.BooleanField(default=False)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    verification_token_created = models.DateTimeField(blank=True, null=True)
    
    # Password reset
    reset_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token_created = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    class Meta:
        db_table = 'clients'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'