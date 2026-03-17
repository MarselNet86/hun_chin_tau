from django.db import models
from django.utils.text import slugify


class SlugMixin(models.Model):
    """Mixin для автоматической генерации slug"""
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(getattr(self, 'name', getattr(self, 'title_ru', '')))
        super().save(*args, **kwargs)


class Genre(SlugMixin):
    """Жанры аниме"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Studio(SlugMixin):
    """Студии, создающие аниме"""
    name = models.CharField(max_length=200, unique=True)
    founded_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(SlugMixin):
    """Теги для аниме"""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Anime(models.Model):
    """Основная модель аниме"""
    STATUS_CHOICES = [
        ('ongoing', 'Онгоинг'),
        ('completed', 'Завершено'),
        ('announced', 'Анонсировано'),
        ('hiatus', 'На паузе'),
    ]

    RATING_CHOICES = [
        ('g', 'G - Для любого возраста'),
        ('pg', 'PG - Детям 6+'),
        ('pg13', 'PG-13 - Подросткам 13+'),
        ('r17', 'R-17 - 17+'),
        ('r', 'R - 18+'),
        ('rx', 'RX - Хентай'),
    ]

    title_ru = models.CharField(max_length=300, verbose_name='Название (русское)')
    title_en = models.CharField(max_length=300, blank=True, verbose_name='Название (английское)')
    title_original = models.CharField(max_length=300, blank=True, verbose_name='Оригинальное название')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    poster = models.ImageField(upload_to='anime/posters/', blank=True, null=True, verbose_name='Постер')
    cover = models.ImageField(upload_to='anime/covers/', blank=True, null=True, verbose_name='Обложка')

    genres = models.ManyToManyField(Genre, related_name='anime', blank=True, verbose_name='Жанры')
    tags = models.ManyToManyField(Tag, related_name='anime', blank=True, verbose_name='Теги')
    studios = models.ManyToManyField(Studio, related_name='anime', blank=True, verbose_name='Студии')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing', verbose_name='Статус')
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default='pg13', verbose_name='Рейтинг')
    score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Оценка')
    episodes_count = models.PositiveIntegerField(default=0, verbose_name='Количество эпизодов')
    duration = models.PositiveIntegerField(default=0, help_text='Длительность эпизода в минутах', verbose_name='Длительность эпизода')

    year = models.IntegerField(null=True, blank=True, verbose_name='Год выхода')
    released_at = models.DateField(null=True, blank=True, verbose_name='Дата выхода')

    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    favorites_count = models.PositiveIntegerField(default=0, verbose_name='В закладках')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'
        ordering = ['-year', '-title_ru']
        indexes = [
            models.Index(fields=['-year', '-title_ru']),
            models.Index(fields=['status']),
            models.Index(fields=['-score']),
            models.Index(fields=['-views_count']),
        ]

    def __str__(self):
        return self.title_ru

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_ru)
        super().save(*args, **kwargs)
