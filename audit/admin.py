from django.contrib import admin
from .models import AuditLog
from unfold.admin import ModelAdmin

@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ('user', 'model_name', 'action','changes','timestamp')
    search_fields = ('user__email', 'model_name', 'action')
    list_filter = ('action', 'timestamp')
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
