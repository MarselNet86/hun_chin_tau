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

    context = {
        'episode': episode,
        'anime': anime,
        'season': season,
        'season_episodes': season_episodes,
        'player_source': player_source,
        'voice_actor': episode.voice_actors.first().name if episode.voice_actors.exists() else None,
    }

    return render(request, 'player/player.html', context)


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
