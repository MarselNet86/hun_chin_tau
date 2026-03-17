from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, UserBookmark


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserBookmark)
class UserBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_anime_title', 'status', 'updated_at']
    list_filter = ['status', 'updated_at']
    search_fields = ['user__username', 'anime__title_ru']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20

    def get_anime_title(self, obj):
        return obj.anime.title_ru
    get_anime_title.short_description = 'Аниме'
