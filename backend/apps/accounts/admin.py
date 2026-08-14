from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['is_active']