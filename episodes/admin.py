from django.contrib import admin
from django import forms
from .models import Season, VoiceActor, Episode, PlayerSource, Subtitle


class PlayerSourceForm(forms.ModelForm):
    class Meta:
        model = PlayerSource
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем/скрываем поля в зависимости от типа плеера
        if self.instance.pk and self.instance.player_type != 'video':
            self.fields['video_file'].required = False
            self.fields['video_url'].required = False


class PlayerSourceInline(admin.TabularInline):
    model = PlayerSource
    extra = 1
    fields = ['player_type', 'url', 'iframe_url', 'video_file', 'video_url', 'quality', 'is_default']
    form = PlayerSourceForm


class SubtitleInline(admin.TabularInline):
    model = Subtitle
    extra = 0


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
    inlines = [PlayerSourceInline, SubtitleInline]
    list_per_page = 20

    def get_anime_title(self, obj):
        return obj.season.anime.title_ru
    get_anime_title.short_description = 'Аниме'
    get_anime_title.admin_order_field = 'season__anime__title_ru'
    
    fieldsets = (
        ('Основное', {
            'fields': ('season', 'number', 'title', 'description')
        }),
        ('Технические', {
            'fields': ('quality', 'duration', 'has_subtitles', 'subtitle_languages')
        }),
        ('Озвучка', {
            'fields': ('voice_actors',)
        }),
        ('Даты', {
            'fields': ('released_at', 'views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PlayerSource)
class PlayerSourceAdmin(admin.ModelAdmin):
    list_display = ['episode', 'player_type', 'quality', 'is_default', 'has_video']
    list_filter = ['player_type', 'quality', 'is_default']
    search_fields = ['episode__title', 'episode__season__anime__title_ru']
    list_editable = ['is_default']
    form = PlayerSourceForm
    
    fieldsets = (
        ('Основное', {
            'fields': ('episode', 'player_type', 'quality', 'is_default')
        }),
        ('Iframe источник (для Anitype, Kodik и др.)', {
            'fields': ('url', 'iframe_url'),
            'description': 'Заполните для iframe плееров'
        }),
        ('Прямое видео (для Plyr)', {
            'fields': ('video_file', 'video_url'),
            'description': 'Загрузите видеофайл или укажите прямую ссылку на видео'
        }),
    )
    
    def has_video(self, obj):
        if obj.player_type == 'video':
            return bool(obj.video_file or obj.video_url)
        return bool(obj.iframe_url or obj.url)
    has_video.boolean = True
    has_video.short_description = 'Есть видео'


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ['episode', 'language', 'is_default']
    list_filter = ['language', 'is_default']
    search_fields = ['episode__title', 'episode__season__anime__title_ru']
    list_editable = ['is_default']
