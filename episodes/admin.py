from django.contrib import admin
from django import forms
from django.utils.html import format_html
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


class PlayerSourceInline(admin.StackedInline):
    model = PlayerSource
    extra = 1
    fields = ['player_type', 'url', 'iframe_url', 'video_file', 'video_url', 'quality', 'is_default']
    form = PlayerSourceForm
    verbose_name = 'Источник видео'
    verbose_name_plural = 'Источники видео'


class SubtitleInline(admin.TabularInline):
    model = Subtitle
    extra = 0
    verbose_name = 'Субтитры'
    verbose_name_plural = 'Субтитры'


class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 1
    fields = ['number', 'title', 'quality', 'duration', 'released_at']
    verbose_name = 'Эпизод'
    verbose_name_plural = 'Эпизоды'

    class Media:
        css = {
            'all': ('admin/css/episodes-inline.css',)
        }


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['anime', 'number', 'get_title', 'episodes_count']
    list_filter = ['anime']
    search_fields = ['anime__title_ru', 'title']
    inlines = [EpisodeInline]
    verbose_name = 'Сезон'
    verbose_name_plural = 'Сезоны'

    fieldsets = (
        ('Основное', {
            'fields': ('anime', 'number', 'title'),
            'description': 'Укажите аниме, номер сезона и название (если есть)'
        }),
    )

    def get_title(self, obj):
        return obj.title if obj.title else '—'
    get_title.short_description = 'Название'

    def episodes_count(self, obj):
        return obj.episodes.count()
    episodes_count.short_description = 'Эпизодов'


@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'website']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Озвучка'
    verbose_name_plural = 'Озвучки'

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'description', 'website'),
            'description': 'Добавьте информацию об озвучке'
        }),
    )


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['get_anime_title', 'season_link', 'number', 'title', 'quality_badge', 'released_at', 'views_count']
    list_filter = ['season__anime', 'season', 'quality', 'has_subtitles']
    search_fields = ['title', 'season__anime__title_ru', 'season__anime__title_en']
    filter_horizontal = ['voice_actors']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PlayerSourceInline, SubtitleInline]
    list_per_page = 20
    verbose_name = 'Эпизод'
    verbose_name_plural = 'Эпизоды'

    fieldsets = (
        ('📺 Основное', {
            'fields': ('season', 'number', 'title', 'description'),
            'description': 'Основная информация об эпизоде'
        }),
        ('⚙️ Технические', {
            'fields': ('quality', 'duration', 'has_subtitles', 'subtitle_languages'),
            'description': 'Качество видео и субтитры'
        }),
        ('🎙️ Озвучка', {
            'fields': ('voice_actors',),
            'description': 'Выберите озвучку из списка'
        }),
        ('📅 Даты и статистика', {
            'fields': ('released_at', 'views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Дата выхода и статистика просмотров'
        }),
    )

    def get_anime_title(self, obj):
        return obj.season.anime.title_ru
    get_anime_title.short_description = 'Аниме'
    get_anime_title.admin_order_field = 'season__anime__title_ru'

    def season_link(self, obj):
        return format_html(
            '<a href="/admin/episodes/season/{}/change/">Сезон {}</a>',
            obj.season.id,
            obj.season.number
        )
    season_link.short_description = 'Сезон'

    def quality_badge(self, obj):
        colors = {
            '360p': '#888',
            '480p': '#555',
            '720p': '#4ade80',
            '1080p': '#22c55e',
            '4K': '#eab308'
        }
        color = colors.get(obj.quality, '#888')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:11px;">{}</span>',
            color,
            obj.quality
        )
    quality_badge.short_description = 'Качество'


@admin.register(PlayerSource)
class PlayerSourceAdmin(admin.ModelAdmin):
    list_display = ['episode_link', 'player_type_badge', 'quality', 'is_default', 'has_video_badge']
    list_filter = ['player_type', 'quality', 'is_default']
    search_fields = ['episode__title', 'episode__season__anime__title_ru']
    list_editable = ['is_default']
    form = PlayerSourceForm
    verbose_name = 'Источник плеера'
    verbose_name_plural = 'Источники плеера'

    fieldsets = (
        ('📺 Основное', {
            'fields': ('episode', 'player_type', 'quality', 'is_default'),
            'description': 'Выберите тип источника и настройте параметры'
        }),
        ('🔗 Iframe источник (для Anitype, Kodik и др.)', {
            'fields': ('url', 'iframe_url'),
            'description': 'Заполните для iframe плееров (внешние источники)',
            'classes': ('iframe-source',)
        }),
        ('🎬 Прямое видео (для Plyr)', {
            'fields': ('video_file', 'video_url'),
            'description': 'Загрузите видеофайл или укажите прямую ссылку на видео',
            'classes': ('video-source',)
        }),
    )

    def episode_link(self, obj):
        return format_html(
            '<a href="/admin/episodes/episode/{}/change/">{}</a>',
            obj.episode.id,
            obj.episode
        )
    episode_link.short_description = 'Эпизод'

    def player_type_badge(self, obj):
        colors = {
            'video': '#4ade80',
            'anitype': '#60a5fa',
            'kodik': '#f472b6',
            'alloha': '#a78bfa',
            'custom': '#fbbf24'
        }
        color = colors.get(obj.player_type, '#888')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:11px;">{}</span>',
            color,
            obj.get_player_type_display()
        )
    player_type_badge.short_description = 'Тип'

    def has_video_badge(self, obj):
        if obj.player_type == 'video':
            has_video = bool(obj.video_file or obj.video_url)
        else:
            has_video = bool(obj.iframe_url or obj.url)

        if has_video:
            return format_html('<span style="color:{};">✓ Да</span>', '#4ade80')
        return format_html('<span style="color:{};">✗ Нет</span>', '#ef4444')
    has_video_badge.short_description = 'Видео'


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ['episode_link', 'language', 'is_default', 'file_link']
    list_filter = ['language', 'is_default']
    search_fields = ['episode__title', 'episode__season__anime__title_ru']
    list_editable = ['is_default']
    verbose_name = 'Субтитры'
    verbose_name_plural = 'Субтитры'

    def episode_link(self, obj):
        return format_html(
            '<a href="/admin/episodes/episode/{}/change/">{}</a>',
            obj.episode.id,
            obj.episode
        )
    episode_link.short_description = 'Эпизод'

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Скачать</a>', obj.file.url)
        return format_html('<span>—</span>')
    file_link.short_description = 'Файл'
