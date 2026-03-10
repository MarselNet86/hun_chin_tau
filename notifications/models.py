from django.conf import settings
from django.db import models


class AnimeSubscription(models.Model):
    """Подписка пользователя на аниме"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anime_subscriptions', verbose_name='Пользователь')
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE, related_name='subscribers', verbose_name='Аниме')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписка на аниме'
        verbose_name_plural = 'Подписки на аниме'
        ordering = ['-created_at']
        unique_together = ['user', 'anime']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.anime.title}'


class Notification(models.Model):
    """Уведомления для пользователей"""
    NOTIFICATION_TYPE_CHOICES = [
        ('new_episode', 'Новый эпизод'),
        ('anime_announcement', 'Анонс аниме'),
        ('system', 'Системное'),
        ('subscription', 'Подписка'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Текст уведомления')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES, default='other', verbose_name='Тип')
    
    # Связь с аниме (опционально)
    anime = models.ForeignKey('anime.Anime', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications', verbose_name='Аниме')
    episode = models.ForeignKey('episodes.Episode', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications', verbose_name='Эпизод')
    
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.title}'


class NotificationSetting(models.Model):
    """Настройки уведомлений пользователя"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_settings', verbose_name='Пользователь')
    
    email_new_episode = models.BooleanField(default=True, verbose_name='Email: Новый эпизод')
    email_anime_announcement = models.BooleanField(default=True, verbose_name='Email: Анонс аниме')
    email_system = models.BooleanField(default=True, verbose_name='Email: Системные')
    
    push_new_episode = models.BooleanField(default=True, verbose_name='Push: Новый эпизод')
    push_anime_announcement = models.BooleanField(default=True, verbose_name='Push: Анонс аниме')
    push_system = models.BooleanField(default=True, verbose_name='Push: Системные')

    class Meta:
        verbose_name = 'Настройка уведомлений'
        verbose_name_plural = 'Настройки уведомлений'

    def __str__(self):
        return f'Настройки уведомлений {self.user.username}'
