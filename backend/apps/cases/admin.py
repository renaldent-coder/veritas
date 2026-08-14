from django.contrib import admin
from .models import Case, Document, InternalNote, ClientCommunication, AuditLog

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'client', 'loss_amount', 'status', 'submitted_at']
    search_fields = ['case_number', 'client__email']
    list_filter = ['status']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'case', 'uploaded_at']

@admin.register(InternalNote)
class InternalNoteAdmin(admin.ModelAdmin):
    list_display = ['case', 'author', 'created_at']

@admin.register(ClientCommunication)
class ClientCommunicationAdmin(admin.ModelAdmin):
    list_display = ['case', 'subject', 'sent_at']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['case', 'user', 'new_status', 'timestamp']