from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserAnimeHistory(models.Model):
    """История просмотров пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='anime_history')
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)
    episode = models.ForeignKey('episodes.Episode', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'История просмотра'
        verbose_name_plural = 'История просмотров'
        ordering = ['-watched_at']
        unique_together = ['user', 'anime']

    def __str__(self):
        return f'{self.user.username} - {self.anime.title}'


class UserBookmark(models.Model):
    """Закладки пользователя"""
    STATUS_CHOICES = [
        ('watching', 'Смотрю'),
        ('completed', 'Просмотрено'),
        ('planned', 'В планах'),
        ('dropped', 'Брошено'),
        ('on_hold', 'Отложено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
        ordering = ['-updated_at']
        unique_together = ['user', 'anime']

    def __str__(self):
        return f'{self.user.username} - {self.anime.title} ({self.status})'
