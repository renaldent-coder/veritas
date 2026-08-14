from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Client(AbstractUser):
    # UUID as primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Additional fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    telegram_handle = models.CharField(max_length=100, blank=True, null=True)
    
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
        return self.email  # 👈 Simplified
    
    class Meta:
        db_table = 'clients'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'