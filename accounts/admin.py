from django.contrib import admin
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'message_snippet')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')

    def message_snippet(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_snippet.short_description = 'Message Preview'

    ordering = ('-created_at',)
    fields = ('name', 'email', 'message', 'created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

admin.site.register(ContactMessage, ContactMessageAdmin)
