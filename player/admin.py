from django.contrib import admin
from .models import WatchHistory, WatchProgress, WatchMoment, UserNote


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_anime_title', 'episode', 'completed', 'watched_at']
    list_filter = ['completed', 'watched_at']
    search_fields = ['user__username', 'episode__season__anime__title_ru']
    readonly_fields = ['watched_at']
    
    def get_anime_title(self, obj):
        return obj.episode.season.anime.title_ru
    get_anime_title.short_description = 'Аниме'


@admin.register(WatchProgress)
class WatchProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_anime_title', 'episode', 'current_time', 'duration', 'percentage', 'last_watched']
    list_filter = ['last_watched']
    search_fields = ['user__username', 'episode__season__anime__title_ru']
    readonly_fields = ['last_watched']
    
    def get_anime_title(self, obj):
        return obj.episode.season.anime.title_ru
    get_anime_title.short_description = 'Аниме'


@admin.register(WatchMoment)
class WatchMomentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_anime_title', 'episode', 'timestamp', 'moment_type', 'created_at']
    list_filter = ['moment_type', 'created_at']
    search_fields = ['user__username', 'episode__title', 'episode__season__anime__title_ru']
    readonly_fields = ['created_at']
    
    def get_anime_title(self, obj):
        return obj.episode.season.anime.title_ru
    get_anime_title.short_description = 'Аниме'


@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_anime_title', 'episode', 'timestamp', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content', 'episode__season__anime__title_ru']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_anime_title(self, obj):
        return obj.episode.season.anime.title_ru
    get_anime_title.short_description = 'Аниме'
