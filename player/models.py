from django.conf import settings
from django.db import models


class WatchHistory(models.Model):
    """История просмотра эпизодов пользователем"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_history', verbose_name='Пользователь')
    episode = models.ForeignKey('episodes.Episode', on_delete=models.CASCADE, related_name='watch_history', verbose_name='Эпизод')
    watched_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')
    completed = models.BooleanField(default=False, verbose_name='Просмотрено до конца')

    class Meta:
        verbose_name = 'История просмотра'
        verbose_name_plural = 'История просмотров'
        ordering = ['-watched_at']
        unique_together = ['user', 'episode']
        indexes = [
            models.Index(fields=['user', '-watched_at']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.episode}'

    def get_anime(self):
        return self.episode.season.anime


class WatchProgress(models.Model):
    """Прогресс просмотра эпизода"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_progress', verbose_name='Пользователь')
    episode = models.ForeignKey('episodes.Episode', on_delete=models.CASCADE, related_name='watch_progress', verbose_name='Эпизод')
    current_time = models.PositiveIntegerField(default=0, help_text='Текущая позиция в секундах', verbose_name='Текущее время')
    duration = models.PositiveIntegerField(default=0, help_text='Общая длительность в секундах', verbose_name='Длительность')
    last_watched = models.DateTimeField(auto_now=True, verbose_name='Последний просмотр')

    class Meta:
        verbose_name = 'Прогресс просмотра'
        verbose_name_plural = 'Прогресс просмотров'
        ordering = ['-last_watched']
        unique_together = ['user', 'episode']
        indexes = [
            models.Index(fields=['user', '-last_watched']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.episode} ({self.current_time}s / {self.duration}s)'

    def get_anime(self):
        return self.episode.season.anime

    @property
    def percentage(self):
        if self.duration == 0:
            return 0
        return round((self.current_time / self.duration) * 100, 2)

    @property
    def is_completed(self):
        return self.current_time >= self.duration * 0.9  # 90% считается завершённым


class WatchMoment(models.Model):
    """Моменты (таймкоды) в эпизодах"""
    MOMENT_TYPE_CHOICES = [
        ('funny', 'Смешной момент'),
        ('epic', 'Эпичный момент'),
        ('important', 'Важный момент'),
        ('opening', 'Открывашка'),
        ('ending', 'Заставка'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_moments', verbose_name='Пользователь')
    episode = models.ForeignKey('episodes.Episode', on_delete=models.CASCADE, related_name='moments', verbose_name='Эпизод')
    timestamp = models.PositiveIntegerField(help_text='Время момента в секундах', verbose_name='Время момента')
    moment_type = models.CharField(max_length=20, choices=MOMENT_TYPE_CHOICES, default='other', verbose_name='Тип момента')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Момент'
        verbose_name_plural = 'Моменты'
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['episode', 'timestamp']),
        ]

    def __str__(self):
        return f'{self.episode} - {self.timestamp}s ({self.get_moment_type_display()})'

    def get_anime(self):
        return self.episode.season.anime


class UserNote(models.Model):
    """Заметки пользователя к эпизодам"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes', verbose_name='Пользователь')
    episode = models.ForeignKey('episodes.Episode', on_delete=models.CASCADE, related_name='notes', verbose_name='Эпизод')
    timestamp = models.PositiveIntegerField(null=True, blank=True, help_text='Время заметки в секундах', verbose_name='Время заметки')
    content = models.TextField(verbose_name='Текст заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.episode}'

    def get_anime(self):
        return self.episode.season.anime
