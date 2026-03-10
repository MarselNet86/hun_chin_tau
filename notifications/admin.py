from django.contrib import admin
from .models import AnimeSubscription, Notification, NotificationSetting


@admin.register(AnimeSubscription)
class AnimeSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'anime__title_ru']
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'anime', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Отметить как прочитанные'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = 'Отметить как непрочитанные'


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_new_episode', 'push_new_episode']
    search_fields = ['user__username']
