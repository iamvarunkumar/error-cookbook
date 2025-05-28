from django.contrib import admin, messages # Add messages
from .models import Category, ErrorEntry, Comment, Bookmark

# ... (CategoryAdmin, CommentAdmin, BookmarkAdmin remain the same) ...
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    readonly_fields = ('slug',)
    search_fields = ['name']

@admin.register(ErrorEntry) # MODIFIED for Sprint 6
class ErrorEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'is_public', 'updated_at', 'slug') # Added status, is_public
    list_filter = ('status', 'is_public', 'category', 'updated_at', 'author') # Added status, is_public
    search_fields = ('title', 'description', 'error_code', 'author__username')
    readonly_fields = ('slug', 'created_at', 'updated_at') # Added created_at, updated_at as often useful
    autocomplete_fields = ['author', 'category']
    # Make fields editable in list view for quick changes
    # list_editable = ('status', 'is_public') # Careful with this, direct edits can bypass custom save logic

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'error_code', 'category', 'author')
        }),
        ('Content', {
            'fields': ('description', 'cause_overview', 'solution_overview')
        }),
        ('Moderation', { # New section
            'fields': ('status', 'is_public', 'moderator_notes'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Keep it collapsed by default
        }),
    )
    actions = ['approve_selected_errors', 'reject_selected_errors', 'mark_as_pending'] # New admin actions

    @admin.action(description='Mark selected errors as Approved and Public')
    def approve_selected_errors(self, request, queryset):
        updated_count = queryset.update(status=ErrorEntry.STATUS_APPROVED, is_public=True)
        self.message_user(request, f'{updated_count} error(s) were successfully approved and made public.', messages.SUCCESS)

    @admin.action(description='Mark selected errors as Rejected')
    def reject_selected_errors(self, request, queryset):
        updated_count = queryset.update(status=ErrorEntry.STATUS_REJECTED, is_public=False)
        self.message_user(request, f'{updated_count} error(s) were successfully rejected.', messages.WARNING)

    @admin.action(description='Mark selected errors as Pending Review')
    def mark_as_pending(self, request, queryset):
        updated_count = queryset.update(status=ErrorEntry.STATUS_PENDING, is_public=False)
        self.message_user(request, f'{updated_count} error(s) were marked as pending review.', messages.INFO)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'error_entry_title', 'body_preview', 'created_at', 'updated_at')
    # ... (rest of CommentAdmin as in Sprint 5)
    list_filter = ('created_at', 'author')
    search_fields = ('body', 'author__username', 'error_entry__title')
    readonly_fields = ('created_at', 'updated_at')

    def error_entry_title(self, obj):
        return obj.error_entry.title
    error_entry_title.short_description = 'Error Entry'

    def body_preview(self, obj):
        return (obj.body[:75] + '...') if len(obj.body) > 75 else obj.body
    body_preview.short_description = 'Comment Preview'

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'error_entry_title', 'created_at')
    # ... (rest of BookmarkAdmin as in Sprint 5)
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'error_entry__title')
    readonly_fields = ('created_at',)

    def error_entry_title(self, obj):
        return obj.error_entry.title
    error_entry_title.short_description = 'Bookmarked Error'