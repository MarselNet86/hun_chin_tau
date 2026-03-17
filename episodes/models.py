from django.db import models
from anime.models import SlugMixin


class Season(models.Model):
    """Сезон аниме"""
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE, related_name='seasons', verbose_name='Аниме')
    number = models.PositiveIntegerField(default=1, verbose_name='Номер сезона')
    title = models.CharField(max_length=200, blank=True, verbose_name='Название сезона')

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'
        ordering = ['number']
        unique_together = ['anime', 'number']

    def __str__(self):
        return f'{self.anime.title_ru} - Сезон {self.number}'


class VoiceActor(SlugMixin):
    """Озвучка"""
    name = models.CharField(max_length=200, verbose_name='Название озвучки')
    description = models.TextField(blank=True, verbose_name='Описание')
    website = models.URLField(blank=True, verbose_name='Сайт')

    class Meta:
        verbose_name = 'Озвучка'
        verbose_name_plural = 'Озвучки'
        ordering = ['name']

    def __str__(self):
        return self.name


class Episode(models.Model):
    """Эпизод аниме"""
    QUALITY_CHOICES = [
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('4K', '4K'),
    ]

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes', verbose_name='Сезон')
    number = models.PositiveIntegerField(verbose_name='Номер эпизода')
    title = models.CharField(max_length=300, blank=True, verbose_name='Название эпизода')
    description = models.TextField(blank=True, verbose_name='Описание')
    duration = models.PositiveIntegerField(default=0, help_text='Длительность в минутах', verbose_name='Длительность')

    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='720p', verbose_name='Качество')
    voice_actors = models.ManyToManyField(VoiceActor, related_name='episodes', blank=True, verbose_name='Озвучки')

    released_at = models.DateField(null=True, blank=True, verbose_name='Дата выхода')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Эпизод'
        verbose_name_plural = 'Эпизоды'
        ordering = ['season', 'number']
        unique_together = ['season', 'number']
        indexes = [
            models.Index(fields=['season', 'number']),
            models.Index(fields=['-released_at']),
        ]

    def __str__(self):
        season_num = self.season.number
        return f'{self.season.anime.title_ru} - S{season_num}E{self.number}'

    def get_anime(self):
        return self.season.anime


class PlayerSource(models.Model):
    """Источник плеера (Anitype, Kodik, прямое видео)"""
    PLAYER_TYPE_CHOICES = [
        ('anitype', 'Anitype'),
        ('kodik', 'Kodik'),
        ('alloha', 'Alloha'),
        ('video', 'Прямое видео (Plyr)'),
        ('custom', 'Custom iframe'),
    ]

    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='player_sources', verbose_name='Эпизод')
    player_type = models.CharField(max_length=20, choices=PLAYER_TYPE_CHOICES, verbose_name='Тип плеера')
    
    # Для iframe источников
    url = models.URLField(blank=True, verbose_name='URL источника')
    iframe_url = models.URLField(blank=True, verbose_name='URL iframe')
    
    # Для прямого видео
    video_file = models.FileField(upload_to='videos/episodes/', blank=True, null=True, verbose_name='Видеофайл')
    video_url = models.URLField(blank=True, verbose_name='URL видеофайла')
    
    quality = models.CharField(max_length=10, choices=Episode.QUALITY_CHOICES, default='720p', verbose_name='Качество')
    is_default = models.BooleanField(default=False, verbose_name='По умолчанию')

    class Meta:
        verbose_name = 'Источник плеера'
        verbose_name_plural = 'Источники плеера'
        ordering = ['-is_default', 'player_type']

    def __str__(self):
        return f'{self.get_player_type_display()} - {self.episode}'
    
    def get_video_url(self):
        """Получить URL видео для Plyr"""
        if self.player_type == 'video':
            if self.video_file:
                return self.video_file.url
            return self.video_url
        return self.iframe_url or self.url
