from django.shortcuts import render
from anime.models import Anime, Genre


def catalog(request):
    """Страница каталога с фильтрами"""
    animes = Anime.objects.all()
    genres = Genre.objects.all()
    
    # Простая фильтрация по GET параметрам
    genre_id = request.GET.get('genre')
    if genre_id:
        animes = animes.filter(genres__id=genre_id)
    
    status = request.GET.get('status')
    if status:
        animes = animes.filter(status=status)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-year')
    if sort_by in ['year', '-year', 'title_ru', '-title_ru', 'score', '-score', 'views_count', '-views_count']:
        animes = animes.order_by(sort_by)
    
    context = {
        'animes': animes,
        'genres': genres,
        'sort': sort_by,
        'status': status,
    }
    return render(request, 'catalog/catalog.html', context)
