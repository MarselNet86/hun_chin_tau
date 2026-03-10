from django.shortcuts import render, get_object_or_404, redirect
from episodes.models import Episode, PlayerSource


def player(request, episode_id):
    """Страница плеера"""
    episode = get_object_or_404(Episode, id=episode_id)
    anime = episode.season.anime
    season = episode.season
    
    # Получаем все эпизоды сезона
    season_episodes = Episode.objects.filter(season=season).order_by('number')
    
    # Получаем источник плеера
    player_source = episode.player_sources.filter(is_default=True).first()
    if not player_source:
        player_source = episode.player_sources.first()
    
    # Получаем прогресс просмотра (если пользователь авторизован)
    progress = 0
    current_time = "00:00"
    if request.user.is_authenticated:
        from player.models import WatchProgress
        try:
            watch_progress = WatchProgress.objects.get(user=request.user, episode=episode)
            progress = watch_progress.percentage
            current_time = format_time(watch_progress.current_time)
        except WatchProgress.DoesNotExist:
            pass
    
    context = {
        'episode': episode,
        'anime': anime,
        'season': season,
        'season_episodes': season_episodes,
        'player_source': player_source,
        'progress': progress,
        'current_time': current_time,
        'voice_actor': episode.voice_actors.first().name if episode.voice_actors.exists() else None,
    }
    
    return render(request, 'player/player.html', context)


def format_time(seconds):
    """Форматирование времени в MM:SS"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def next_episode(request, episode_id):
    """Переход к следующему эпизоду"""
    episode = get_object_or_404(Episode, id=episode_id)
    next_ep = Episode.objects.filter(
        season=episode.season,
        number__gt=episode.number
    ).order_by('number').first()
    
    if next_ep:
        return redirect('player:player', episode_id=next_ep.id)
    return redirect('anime:detail', slug=episode.season.anime.slug)


def prev_episode(request, episode_id):
    """Переход к предыдущему эпизоду"""
    episode = get_object_or_404(Episode, id=episode_id)
    prev_ep = Episode.objects.filter(
        season=episode.season,
        number__lt=episode.number
    ).order_by('-number').first()
    
    if prev_ep:
        return redirect('player:player', episode_id=prev_ep.id)
    return redirect('player:player', episode_id=episode_id)
