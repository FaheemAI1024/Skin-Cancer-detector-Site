from django.contrib import admin
from .models import Chat ,SkinCondition, HealthTopic, HealthArticle
from django.utils.html import format_html

class ChatAdmin(admin.ModelAdmin):
    # Define columns to display in the list view
    list_display = ('user', 'text', 'message_type', 'created_at')
    
    # Add filters to help quickly find incoming/outgoing messages
    list_filter = ('message_type', 'created_at')
    
    # Allow searching by message content and username (foreign key to user)
    search_fields = ('text', 'user__username')  # Search by message and user
    
    # Ordering by creation date (newest first)
    ordering = ('-created_at',)
    
    # Fields to show in the edit form
    fields = ('user', 'text', 'message_type', 'created_at')
    
    # Make created_at read-only so it can't be edited
    readonly_fields = ('created_at',)
    
    # Add custom action for bulk delete
    actions = ['delete_selected_chats']

    def delete_selected_chats(self, request, queryset):
        """Custom action to delete selected chats."""
        queryset.delete()
    delete_selected_chats.short_description = "Delete selected chats"

# Register the model with the custom admin interface
admin.site.register(Chat, ChatAdmin)


@admin.register(SkinCondition)
class SkinConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'condition_type', 'detected_at', 'image_preview')
    list_filter = ('condition_type', 'detected_at')
    search_fields = ('name', 'description')
    readonly_fields = ('detected_at', 'image_preview')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'condition_type')
        }),
        ('Image and Detection', {
            'fields': ('image', 'image_preview', 'detected_at')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 150px;"/>', obj.image.url)
        return "No image"

    image_preview.short_description = "Preview"


@admin.register(HealthTopic)
class HealthTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'image_preview')
    list_filter = ('category', 'published_at')
    search_fields = ('title', 'content')
    readonly_fields = ('published_at', 'image_preview')

    fieldsets = (
        ('Topic Information', {
            'fields': ('title', 'category', 'content')
        }),
        ('Image and Metadata', {
            'fields': ('image', 'image_preview', 'published_at')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 150px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = "Preview"

class HealthArticleAdmin(admin.ModelAdmin):
    # List the fields to be displayed in the list view of the admin
    list_display = ('title', 'category',  'image_tag', 'short_content')
    search_fields = ('title', 'content', 'category')
    
    # Add a thumbnail image to the list view
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{0}" width="50" height="50" style="object-fit: cover;"/>'.format(obj.image.url))
        return 'No image'

    image_tag.short_description = 'Image'
    
    # Add a short preview of the content
    def short_content(self, obj):
        return f"{obj.content[:100]}..."
    
    short_content.short_description = 'Content Preview'

    
    # Add a custom filter to allow easy search of articles based on their published status
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optional: Modify queryset to filter articles based on the current user
        return queryset
    
    # Display the content nicely
    def content_preview(self, obj):
        return format_html('<p>{}</p>', obj.content[:150])  # Truncate the content to preview only
    content_preview.short_description = 'Content Preview'

# Register the model with the custom admin interface
admin.site.register(HealthArticle, HealthArticleAdmin)