from django.contrib import admin
from .models import Season, VoiceActor, Episode, PlayerSource, Subtitle


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = ['number', 'title', 'quality', 'released_at']


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['anime', 'number', 'title']
    list_filter = ['anime']
    search_fields = ['anime__title_ru', 'title']
    inlines = [EpisodeInline]


@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['get_anime_title', 'season', 'number', 'title', 'quality', 'released_at', 'views_count']
    list_filter = ['season__anime', 'quality', 'has_subtitles']
    search_fields = ['title', 'season__anime__title_ru']
    filter_horizontal = ['voice_actors']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_anime_title(self, obj):
        return obj.season.anime.title_ru
    get_anime_title.short_description = 'Аниме'
    get_anime_title.admin_order_field = 'season__anime__title_ru'


@admin.register(PlayerSource)
class PlayerSourceAdmin(admin.ModelAdmin):
    list_display = ['episode', 'player_type', 'quality', 'is_default']
    list_filter = ['player_type', 'quality', 'is_default']
    search_fields = ['episode__title', 'episode__season__anime__title_ru']


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ['episode', 'language', 'is_default']
    list_filter = ['language', 'is_default']
    search_fields = ['episode__title', 'episode__season__anime__title_ru']
