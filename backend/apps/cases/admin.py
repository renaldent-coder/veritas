from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Case, Document, InternalNote, ClientCommunication, AuditLog


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = [
        'case_number',
        'client_link',
        'loss_amount_display',
        'status_colored',
        'scam_category',
        'submitted_at',
        # 'assigned_agent',  # Temporarily removed
    ]
    
    list_filter = [
        'status',
        'scam_category',
        'transaction_method',
        'submitted_at',
    ]
    
    search_fields = [
        'case_number',
        'client__email',
        'client__first_name',
        'client__last_name',
        'narrative',
    ]
    
    readonly_fields = [
        'case_number',
        'submitted_at',
        'updated_at',
    ]
    
    def client_link(self, obj):
        url = reverse('admin:accounts_client_change', args=[obj.client.id])
        return format_html('<a href="{}" style="color: #D4AF37;">{}</a>', url, obj.client.get_full_name())
    client_link.short_description = 'Client'
    
    def loss_amount_display(self, obj):
        return format_html('<strong>${:,.2f}</strong>', obj.loss_amount)
    loss_amount_display.short_description = 'Loss Amount'
    
    def status_colored(self, obj):
        colors = {
            'PENDING_REVIEW': '#FFA500',
            'UNDER_INVESTIGATION': '#1E90FF',
            'EXCHANGE_CONTACTED': '#9370DB',
            'RECOVERY_IN_PROGRESS': '#FF6B6B',
            'RECOVERED': '#2ECC71',
            'CLOSED': '#95A5A6',
            'UNRECOVERABLE': '#E74C3C',
        }
        color = colors.get(obj.status, '#FFFFFF')
        return format_html(
            '<span style="background-color: {}; color: #0A1628; padding: 4px 12px; border-radius: 4px; font-weight: 600; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'