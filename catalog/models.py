from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Collection(models.Model):
    """Подборки аниме (тематические коллекции)"""
    TYPE_CHOICES = [
        ('manual', 'Ручная'),
        ('auto', 'Автоматическая'),
        ('trending', 'Сейчас смотрят'),
        ('popular', 'Популярное'),
        ('top_rated', 'Лучшие по рейтингу'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название подборки')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    cover = models.ImageField(upload_to='collections/', blank=True, null=True, verbose_name='Обложка')
    
    collection_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='manual', verbose_name='Тип')
    
    # Для автоматических подборок
    filter_genres = models.ManyToManyField('anime.Genre', blank=True, related_name='collections', verbose_name='Жанры')
    filter_min_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Мин. рейтинг')
    filter_year_from = models.IntegerField(null=True, blank=True, verbose_name='Год от')
    filter_year_to = models.IntegerField(null=True, blank=True, verbose_name='Год до')
    
    # Для ручных подборок
    animes = models.ManyToManyField('anime.Anime', blank=True, related_name='collections', verbose_name='Аниме')
    
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    priority = models.PositiveIntegerField(default=0, help_text='Приоритет отображения', verbose_name='Приоритет')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Создатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['collection_type', 'is_active']),
            models.Index(fields=['-priority', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SearchQuery(models.Model):
    """История поисковых запросов (для аналитики)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='search_queries', verbose_name='Пользователь')
    query = models.CharField(max_length=300, verbose_name='Поисковый запрос')
    results_count = models.PositiveIntegerField(default=0, verbose_name='Количество результатов')
    searched_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата поиска')

    class Meta:
        verbose_name = 'Поисковый запрос'
        verbose_name_plural = 'Поисковые запросы'
        ordering = ['-searched_at']
        indexes = [
            models.Index(fields=['-searched_at']),
            models.Index(fields=['query']),
        ]

    def __str__(self):
        return f'{self.query} ({self.searched_at})'


class AnimeFilterPreset(models.Model):
    """Пресеты фильтров для быстрого доступа"""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True)
    
    # Фильтры
    genres = models.ManyToManyField('anime.Genre', blank=True, related_name='filter_presets', verbose_name='Жанры')
    status = models.CharField(max_length=20, blank=True, choices=[
        ('ongoing', 'Онгоинг'),
        ('completed', 'Завершено'),
        ('announced', 'Анонсировано'),
        ('hiatus', 'На паузе'),
    ], verbose_name='Статус')
    
    min_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Мин. рейтинг')
    year_from = models.IntegerField(null=True, blank=True, verbose_name='Год от')
    year_to = models.IntegerField(null=True, blank=True, verbose_name='Год до')
    
    # Сортировка
    sort_by = models.CharField(max_length=30, default='-year', choices=[
        ('-year', 'По году (новые)'),
        ('year', 'По году (старые)'),
        ('-score', 'По рейтингу'),
        ('-views_count', 'По просмотрам'),
        ('-title_ru', 'По названию (А-Я)'),
        ('title_ru', 'По названию (Я-А)'),
        ('-released_at', 'По дате выхода'),
    ], verbose_name='Сортировка')
    
    is_public = models.BooleanField(default=False, verbose_name='Публичный')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='filter_presets', verbose_name='Создатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пресет фильтра'
        verbose_name_plural = 'Пресеты фильтров'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
