import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Anime


def index(request):
    """Главная страница"""
    # Получаем аниме для отображения
    now_watching = Anime.objects.filter(status='ongoing').order_by('-score', '-views_count')[:6]
    popular = Anime.objects.order_by('-views_count', '-score')[:6]
    
    # Формируем данные для шаблона в формате JSON для JavaScript
    def anime_to_dict(anime):
        return {
            'id': anime.id,
            'title': anime.title_ru,
            'rating': str(anime.score) if anime.score > 0 else 'N/A',
            'year': str(anime.year) if anime.year else 'N/A',
            'is_4k': False,  # Можно добавить поле в модель
            'genres': [g.name for g in anime.genres.all()[:3]],
            'desc': anime.description[:200] if anime.description else 'Описание отсутствует...',
            'img': anime.poster.url if anime.poster else 'https://i.imgur.com/tCF58S3.jpg'
        }
    
    now_watching_data = [anime_to_dict(a) for a in now_watching]
    popular_data = [anime_to_dict(a) for a in popular]
    all_anime_data = now_watching_data + popular_data
    
    context = {
        'now_watching': now_watching_data,
        'popular': popular_data,
        'anime_data': json.dumps(all_anime_data),
    }
    
    return render(request, 'anime/index.html', context)


def anime_detail(request, slug):
    """Страница аниме"""
    anime = get_object_or_404(Anime, slug=slug)
    return render(request, 'anime/detail.html', {'anime': anime})
