from django.contrib import admin
from .models import Genre, Studio, Tag, Anime


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'founded_year']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'year', 'status', 'score', 'episodes_count', 'views_count']
    list_filter = ['status', 'rating', 'year', 'genres', 'studios']
    search_fields = ['title_ru', 'title_en', 'title_original']
    prepopulated_fields = {'slug': ('title_ru',)}
    filter_horizontal = ['genres', 'tags', 'studios']
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'favorites_count']
    fieldsets = (
        ('Основное', {
            'fields': ('title_ru', 'title_en', 'title_original', 'slug', 'description')
        }),
        ('Медиа', {
            'fields': ('poster', 'cover'),
        }),
        ('Классификация', {
            'fields': ('genres', 'tags', 'studios', 'rating')
        }),
        ('Информация', {
            'fields': ('status', 'episodes_count', 'duration', 'year', 'released_at')
        }),
        ('Статистика', {
            'fields': ('score', 'views_count', 'favorites_count'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
