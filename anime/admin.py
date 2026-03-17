from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Studio, Tag, Anime


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры'

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'description'),
            'description': 'Добавьте жанр для аниме'
        }),
    )


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'founded_year', 'website']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Студия'
    verbose_name_plural = 'Студии'

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'founded_year', 'description', 'website'),
            'description': 'Информация о студии'
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug'),
            'description': 'Добавьте тег для аниме'
        }),
    )


class SeasonInline(admin.TabularInline):
    """Inline для сезонов аниме"""
    from episodes.models import Season
    model = Season
    extra = 1
    fields = ['number', 'title', 'episodes_count']
    verbose_name = 'Сезон'
    verbose_name_plural = 'Сезоны'
    can_delete = False

    def episodes_count(self, obj):
        return obj.episodes.count() if obj.pk else 0
    episodes_count.short_description = 'Эпизодов'


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'year_badge', 'status_badge', 'score_badge', 'episodes_count', 'views_count', 'quick_link']
    list_filter = ['status', 'rating', 'year', 'genres', 'studios']
    search_fields = ['title_ru', 'title_en', 'title_original']
    prepopulated_fields = {'slug': ('title_ru',)}
    filter_horizontal = ['genres', 'tags', 'studios']
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'favorites_count']
    inlines = [SeasonInline]
    verbose_name = 'Аниме'
    verbose_name_plural = 'Аниме'
    list_per_page = 15

    fieldsets = (
        ('📺 Основное', {
            'fields': ('title_ru', 'title_en', 'title_original', 'slug', 'description'),
            'description': 'Основная информация об аниме: названия и описание'
        }),
        ('🖼️ Медиа', {
            'fields': ('poster',),
            'description': 'Загрузите постер'
        }),
        ('🏷️ Классификация', {
            'fields': ('genres', 'tags', 'studios', 'rating'),
            'description': 'Жанры, теги, студии и возрастной рейтинг'
        }),
        ('ℹ️ Информация', {
            'fields': ('status', 'episodes_count', 'duration', 'year', 'released_at'),
            'description': 'Статус, количество эпизодов, длительность и дата выхода'
        }),
        ('📊 Статистика', {
            'fields': ('score', 'views_count', 'favorites_count'),
            'classes': ('collapse',),
            'description': 'Оценка, просмотры и добавления в закладки'
        }),
        ('📅 Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Даты создания и обновления'
        }),
    )

    def year_badge(self, obj):
        return format_html(
            '<span style="background:#e5e7eb;color:#000;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:11px;">{}</span>',
            obj.year or '—'
        )
    year_badge.short_description = 'Год'

    def status_badge(self, obj):
        colors = {
            'ongoing': '#4ade80',
            'completed': '#60a5fa',
            'announced': '#fbbf24',
            'hiatus': '#f472b6'
        }
        color = colors.get(obj.status, '#888')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

    def score_badge(self, obj):
        score = float(obj.score) if obj.score else 0
        if score >= 8:
            color = '#4ade80'
        elif score >= 6:
            color = '#fbbf24'
        elif score >= 4:
            color = '#f97316'
        else:
            color = '#ef4444'

        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:11px;">★ {}</span>',
            color,
            obj.score or 'N/A'
        )
    score_badge.short_description = 'Оценка'

    def quick_link(self, obj):
        return format_html(
            '<a href="/anime/{}/" target="_blank" style="color:#2563eb;">Открыть на сайте</a>',
            obj.slug
        )
    quick_link.short_description = 'На сайте'
