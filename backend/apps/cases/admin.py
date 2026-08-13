from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Case, Document, InternalNote, ClientCommunication, AuditLog


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """Custom admin for Cases with Navy/Gold styling"""
    
    # List view configuration
    list_display = [
        'case_number',
        'client_link',
        'loss_amount_display',
        'status_colored',
        'scam_category',
        'submitted_at',
        'assigned_agent',
    ]
    
    list_filter = [
        'status',
        'scam_category',
        'transaction_method',
        'submitted_at',
        'assigned_agent',
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
        'fee_calculation_display',
    ]
    
    fieldsets = (
        ('Case Identification', {
            'fields': ('case_number', 'client', 'assigned_agent', 'status')
        }),
        ('Scam Details', {
            'fields': ('scam_category', 'narrative')
        }),
        ('Financial Information', {
            'fields': ('loss_amount', 'currency', 'recovery_amount', 'fee_amount', 'fee_percentage', 'fee_calculation_display')
        }),
        ('Transaction Details', {
            'fields': ('transaction_method', 'transaction_data', 'first_transaction_date', 'last_transaction_date')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at', 'recovery_completed_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_recovered', 'mark_as_unrecoverable']
    
    def client_link(self, obj):
        """Link to client in admin"""
        url = reverse('admin:accounts_client_change', args=[obj.client.id])
        return format_html('<a href="{}" style="color: #D4AF37;">{}</a>', url, obj.client.get_full_name())
    client_link.short_description = 'Client'
    
    def loss_amount_display(self, obj):
        """Display loss amount with currency"""
        return format_html('<strong>${:,.2f}</strong>', obj.loss_amount)
    loss_amount_display.short_description = 'Loss Amount'
    
    def status_colored(self, obj):
        """Color-coded status badges"""
        colors = {
            'PENDING_REVIEW': '#FFA500',  # Orange
            'UNDER_INVESTIGATION': '#1E90FF',  # Dodger Blue
            'EXCHANGE_CONTACTED': '#9370DB',  # Medium Purple
            'RECOVERY_IN_PROGRESS': '#FF6B6B',  # Coral
            'RECOVERED': '#2ECC71',  # Emerald Green
            'CLOSED': '#95A5A6',  # Gray
            'UNRECOVERABLE': '#E74C3C',  # Red
        }
        color = colors.get(obj.status, '#FFFFFF')
        return format_html(
            '<span style="background-color: {}; color: #0A1628; padding: 4px 12px; border-radius: 4px; font-weight: 600; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    
    def fee_calculation_display(self, obj):
        """Display fee calculation"""
        if obj.recovery_amount:
            fee = obj.recovery_amount * 0.10
            return format_html(
                '<div style="background: #1E2A45; padding: 10px; border-radius: 4px; border-left: 4px solid #D4AF37;">'
                '<strong style="color: #D4AF37;">Recovery Amount:</strong> ${:,.2f}<br>'
                '<strong style="color: #D4AF37;">10% Fee:</strong> ${:,.2f}<br>'
                '<strong style="color: #2ECC71;">Client Receives:</strong> ${:,.2f}'
                '</div>',
                obj.recovery_amount,
                fee,
                obj.recovery_amount - fee
            )
        return "No recovery amount set yet."
    fee_calculation_display.short_description = 'Fee Calculator'
    
    def mark_as_recovered(self, request, queryset):
        """Admin action: Mark selected cases as recovered"""
        for case in queryset:
            case.status = 'RECOVERED'
            case.recovery_completed_at = timezone.now()
            if case.recovery_amount:
                case.calculate_fee()
            case.save()
        self.message_user(request, f"Successfully marked {queryset.count()} case(s) as recovered.")
    mark_as_recovered.short_description = "Mark as Recovered"
    
    def mark_as_unrecoverable(self, request, queryset):
        """Admin action: Mark selected cases as unrecoverable"""
        queryset.update(status='UNRECOVERABLE')
        self.message_user(request, f"Successfully marked {queryset.count()} case(s) as unrecoverable.")
    mark_as_unrecoverable.short_description = "Mark as Unrecoverable"
    
    # Inline admin for related models
    class DocumentInline(admin.TabularInline):
        model = Document
        extra = 0
        fields = ['document_type', 'file_name', 'file_url', 'uploaded_at']
        readonly_fields = ['uploaded_at']
    
    class InternalNoteInline(admin.TabularInline):
        model = InternalNote
        extra = 1
        fields = ['author', 'content', 'created_at']
        readonly_fields = ['created_at']
    
    class AuditLogInline(admin.TabularInline):
        model = AuditLog
        extra = 0
        fields = ['user', 'previous_status', 'new_status', 'note', 'timestamp']
        readonly_fields = ['timestamp']
        can_delete = False
    
    inlines = [DocumentInline, InternalNoteInline, AuditLogInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'case_link', 'document_type', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['file_name', 'case__case_number']
    readonly_fields = ['uploaded_at']
    
    def case_link(self, obj):
        url = reverse('admin:cases_case_change', args=[obj.case.id])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = 'Case'


@admin.register(InternalNote)
class InternalNoteAdmin(admin.ModelAdmin):
    list_display = ['case_link', 'author', 'created_at', 'content_preview']
    list_filter = ['author', 'created_at']
    search_fields = ['case__case_number', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    def case_link(self, obj):
        url = reverse('admin:cases_case_change', args=[obj.case.id])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = 'Case'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Note Preview'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['case_link', 'user', 'previous_status', 'new_status', 'timestamp']
    list_filter = ['new_status', 'timestamp', 'user']
    search_fields = ['case__case_number']
    readonly_fields = ['timestamp']
    
    def case_link(self, obj):
        url = reverse('admin:cases_case_change', args=[obj.case.id])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = 'Case'


@admin.register(ClientCommunication)
class ClientCommunicationAdmin(admin.ModelAdmin):
    list_display = ['case_link', 'subject', 'method', 'sent_at', 'sent_by']
    list_filter = ['method', 'sent_at']
    search_fields = ['case__case_number', 'subject', 'message']
    readonly_fields = ['sent_at']
    
    def case_link(self, obj):
        url = reverse('admin:cases_case_change', args=[obj.case.id])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = 'Case'