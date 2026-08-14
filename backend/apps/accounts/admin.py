from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import Client


@admin.register(Client)
class ClientAdmin(UserAdmin):
    list_display = [
        'email',
        'full_name',
        'country',
        'date_joined',
        'is_active',
        'email_verified',
        # 'case_count',  # Temporarily removed
    ]
    
    list_filter = [
        'is_active',
        'email_verified',
        'country',
        'date_joined',
    ]
    
    search_fields = [
        'email',
        'first_name',
        'last_name',
        'username',
        'phone_number',
    ]
    
    readonly_fields = [
        'id',
        'date_joined',
        'last_active',
    ]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone_number', 'country', 'telegram_handle')
        }),
        ('Account Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified', 'date_joined', 'last_active')
        }),
        ('Legal Agreements', {
            'fields': ('agreed_to_terms', 'agreed_to_nda', 'agreed_to_fee_structure')
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Create Client', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )
    
    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = 'Full Name'