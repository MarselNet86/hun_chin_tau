import json
import random
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Anime
from episodes.models import Episode


def search_anime(request):
    """API для поиска аниме"""
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'results': [], 'query': query})

    # Поиск по названиям
    results = Anime.objects.filter(
        Q(title_ru__icontains=query) |
        Q(title_en__icontains=query) |
        Q(title_original__icontains=query)
    ).select_related().prefetch_related('genres')[:10]

    def anime_to_dict(anime):
        return {
            'id': anime.id,
            'title': anime.title_ru,
            'slug': anime.slug,
            'score': str(anime.score) if anime.score > 0 else 'N/A',
            'year': str(anime.year) if anime.year else '—',
            'poster': anime.poster.url if anime.poster else 'https://i.imgur.com/tCF58S3.jpg',
            'description': (anime.description[:150] + '...') if anime.description and len(anime.description) > 150 else (anime.description or 'Описание отсутствует...'),
        }

    return JsonResponse({
        'results': [anime_to_dict(anime) for anime in results],
        'query': query
    })


def index(request):
    """Главная страница"""
    # Получаем аниме для отображения
    now_watching = Anime.objects.filter(status='ongoing').order_by('-score', '-views_count')[:6]
    popular = Anime.objects.order_by('-views_count', '-score')[:6]
    
    # Выбираем случайное аниме для Hero секции
    all_anime = list(Anime.objects.all())
    hero_anime = random.choice(all_anime) if all_anime else None
    
    # Получаем первый эпизод для Hero аниме
    hero_first_episode = None
    if hero_anime:
        hero_first_episode = Episode.objects.filter(season__anime=hero_anime).order_by('season__number', 'number').first()
    
    # Формируем данные для шаблона в формате JSON для JavaScript
    def anime_to_dict(anime):
        return {
            'id': anime.id,
            'title': anime.title_ru,
            'slug': anime.slug,
            'rating': str(anime.score) if anime.score > 0 else 'N/A',
            'year': str(anime.year) if anime.year else 'N/A',
            'is_4k': False,
            'genres': [g.name for g in anime.genres.all()[:3]],
            'desc': anime.description[:200] if anime.description else 'Описание отсутствует...',
            'img': anime.poster.url if anime.poster else 'https://i.imgur.com/tCF58S3.jpg',
            'first_episode_id': Episode.objects.filter(season__anime=anime).order_by('season__number', 'number').first().id if Episode.objects.filter(season__anime=anime).exists() else None
        }
    
    now_watching_data = [anime_to_dict(a) for a in now_watching]
    popular_data = [anime_to_dict(a) for a in popular]
    all_anime_data = now_watching_data + popular_data
    
    # Данные для Hero аниме
    hero_data = None
    if hero_anime:
        hero_data = anime_to_dict(hero_anime)
    
    context = {
        'hero_anime': hero_anime,
        'hero_data': hero_data,
        'hero_first_episode': hero_first_episode,
        'now_watching': now_watching_data,
        'popular': popular_data,
        'anime_data': json.dumps(all_anime_data),
    }
    
    return render(request, 'anime/index.html', context)


def anime_detail(request, slug):
    """Страница аниме"""
    anime = get_object_or_404(Anime, slug=slug)
    
    # Получаем первый эпизод для кнопки "Смотреть"
    first_episode = Episode.objects.filter(season__anime=anime).order_by('season__number', 'number').first()
    
    # Получаем все сезоны с эпизодами
    seasons = anime.seasons.prefetch_related('episodes').all()
    
    context = {
        'anime': anime,
        'first_episode': first_episode,
        'seasons': seasons,
    }
    
    return render(request, 'anime/detail.html', context)
