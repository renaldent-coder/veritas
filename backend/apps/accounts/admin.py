from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import Client


@admin.register(Client)
class ClientAdmin(UserAdmin):
    """Custom admin for Client model with Navy/Gold styling"""
    
    list_display = [
        'email',
        'full_name',
        'country',
        'date_joined',
        'is_active',
        'email_verified',
        #'case_count',
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
        'case_count_display',
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
        ('Verification', {
            'fields': ('verification_token', 'verification_token_created', 'reset_token', 'reset_token_created'),
            'classes': ('collapse',)
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
    
    def case_count(self, obj):
        count = obj.cases.count()
        url = reverse('admin:cases_case_changelist') + f'?client__id__exact={obj.id}'
        return format_html('<a href="{}" style="color: #D4AF37;">{} case(s)</a>', url, count)
    case_count.short_description = 'Cases'
    
    def case_count_display(self, obj):
        return obj.cases.count()
    case_count_display.short_description = 'Total Cases'