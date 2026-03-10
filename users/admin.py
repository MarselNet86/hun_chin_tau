from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, UserAnimeHistory, UserBookmark


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserAnimeHistory)
class UserAnimeHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'episode', 'watched_at']
    list_filter = ['watched_at', 'anime']
    search_fields = ['user__username', 'anime__title_ru']
    readonly_fields = ['watched_at']


@admin.register(UserBookmark)
class UserBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'status', 'updated_at']
    list_filter = ['status', 'updated_at']
    search_fields = ['user__username', 'anime__title_ru']
    readonly_fields = ['created_at', 'updated_at']
