from django.contrib import admin
from .models import Collection, SearchQuery, AnimeFilterPreset


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'collection_type', 'is_active', 'priority', 'created_at']
    list_filter = ['collection_type', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['animes', 'filter_genres']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'description', 'cover')
        }),
        ('Тип и настройки', {
            'fields': ('collection_type', 'is_active', 'priority')
        }),
        ('Фильтры (для авто-подборок)', {
            'fields': ('filter_genres', 'filter_min_score', 'filter_year_from', 'filter_year_to'),
            'classes': ('collapse',)
        }),
        ('Аниме (для ручных подборок)', {
            'fields': ('animes',),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'user', 'results_count', 'searched_at']
    list_filter = ['searched_at']
    search_fields = ['query', 'user__username']
    readonly_fields = ['searched_at']


@admin.register(AnimeFilterPreset)
class AnimeFilterPresetAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'is_public', 'sort_by', 'created_at']
    list_filter = ['is_public', 'status', 'sort_by']
    search_fields = ['name', 'created_by__username']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['genres']
