from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Case(models.Model):
    """
    Main Case model for Veritas Asset Recovery.
    Stores all client case information.
    """
    # Primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Relationships
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cases')
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_cases'
    )
    
    # Case details
    STATUS_CHOICES = [
        ('PENDING_REVIEW', 'Pending Review'),
        ('UNDER_INVESTIGATION', 'Under Investigation'),
        ('EXCHANGE_CONTACTED', 'Exchange Contacted'),
        ('RECOVERY_IN_PROGRESS', 'Recovery in Progress'),
        ('RECOVERED', 'Recovered - Fee Due'),
        ('CLOSED', 'Closed'),
        ('UNRECOVERABLE', 'Unrecoverable'),
    ]
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING_REVIEW')
    
    SCAM_CATEGORY_CHOICES = [
        ('FAKE_INVESTMENT', 'Fake Investment Platform'),
        ('ROMANCE', 'Romance Scam'),
        ('IMPERSONATION', 'Impersonation of Authority'),
        ('PHISHING', 'Phishing'),
        ('FAKE_JOB', 'Fake Job Offer'),
        ('CRYPTO_RUGPULL', 'Crypto Rugpull'),
        ('BANK_WIRE_FRAUD', 'Bank Wire Fraud'),
        ('OTHER', 'Other'),
    ]
    
    scam_category = models.CharField(max_length=30, choices=SCAM_CATEGORY_CHOICES)
    
    # Financial details
    loss_amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    recovery_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    fee_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # 10%
    
    # Transaction details (stored as JSON for flexibility)
    transaction_method = models.CharField(max_length=20, choices=[
        ('CRYPTO', 'Cryptocurrency'),
        ('BANK_WIRE', 'Bank Wire'),
        ('CREDIT_CARD', 'Credit Card'),
        ('GIFT_CARD', 'Gift Cards'),
        ('OTHER', 'Other'),
    ])
    transaction_data = models.JSONField(default=dict)  # Stores wallet addresses, IBANs, TxIDs, etc.
    
    # Dates
    first_transaction_date = models.DateField()
    last_transaction_date = models.DateField()
    
    # Narrative
    narrative = models.TextField(max_length=1000)
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recovery_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Case #{self.case_number} - {self.client.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            # Generate case number: VR-YYYY-MM-XXXX
            year = timezone.now().year
            month = timezone.now().month
            import random
            random_id = str(random.randint(1000, 9999))
            self.case_number = f"VR-{year}-{month:02d}-{random_id}"
        super().save(*args, **kwargs)
    
    def calculate_fee(self):
        """Calculate 10% fee on recovery amount"""
        if self.recovery_amount:
            self.fee_amount = self.recovery_amount * (self.fee_percentage / 100)
            self.save()
        return self.fee_amount
    
    class Meta:
        db_table = 'cases'
        ordering = ['-submitted_at']
        verbose_name = 'Case'
        verbose_name_plural = 'Cases'


class Document(models.Model):
    """
    Documents uploaded by clients (screenshots, bank statements, etc.)
    Stored in Cloudflare R2.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='documents')
    
    DOCUMENT_TYPE_CHOICES = [
        ('SCREENSHOT', 'Screenshot'),
        ('BANK_STATEMENT', 'Bank Statement'),
        ('EMAIL', 'Email Headers'),
        ('CHAT_LOG', 'Chat Log'),
        ('TRANSACTION_LOG', 'Transaction Log'),
        ('OTHER', 'Other'),
    ]
    
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()  # URL to file in Cloudflare R2
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.file_name} - Case #{self.case.case_number}"
    
    class Meta:
        db_table = 'documents'
        ordering = ['-uploaded_at']


class InternalNote(models.Model):
    """
    Internal notes for recovery team. Clients DO NOT see these.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Action log (for audit)
    action_type = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Note on Case #{self.case.case_number} by {self.author.get_full_name()}"
    
    class Meta:
        db_table = 'internal_notes'
        ordering = ['-created_at']


class ClientCommunication(models.Model):
    """
    Log of all communications sent to clients.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='communications')
    
    subject = models.CharField(max_length=255)
    message = models.TextField()
    
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Communication method
    method = models.CharField(max_length=20, choices=[
        ('EMAIL', 'Email'),
        ('TELEGRAM', 'Telegram'),
        ('PHONE', 'Phone'),
    ], default='EMAIL')
    
    def __str__(self):
        return f"Communication on Case #{self.case.case_number}"
    
    class Meta:
        db_table = 'client_communications'
        ordering = ['-sent_at']


class AuditLog(models.Model):
    """
    Audit trail for all case status changes.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='audit_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    previous_status = models.CharField(max_length=30, null=True, blank=True)
    new_status = models.CharField(max_length=30)
    note = models.TextField(blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"Audit: Case #{self.case.case_number} - {self.previous_status} → {self.new_status}"
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']