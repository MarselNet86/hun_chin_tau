from django.shortcuts import render
from anime.models import Anime, Genre
from episodes.models import VoiceActor
from django.db.models import Min, Max


def catalog(request):
    """Страница каталога с фильтрами"""
    animes = Anime.objects.all()
    genres = Genre.objects.all()

    # Получаем озвучки, которые есть в эпизодах
    voice_actors = VoiceActor.objects.filter(episodes__isnull=False).distinct()

    # Получаем доступные годы из базы
    years_data = Anime.objects.aggregate(min_year=Min('year'), max_year=Max('year'))
    min_year = years_data['min_year'] or 2000
    max_year = years_data['max_year'] or 2024
    years = list(range(max_year, min_year - 1, -1))

    # Сохраняем исходные параметры для отображения активных фильтров
    original_params = request.GET.copy()

    # Фильтрация по жанрам (множественный выбор)
    genre_ids = request.GET.getlist('genre')
    if genre_ids:
        animes = animes.filter(genres__id__in=genre_ids).distinct()

    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        animes = animes.filter(status=status)

    # Фильтрация по озвучке
    voice_id = request.GET.get('voice')
    if voice_id:
        animes = animes.filter(seasons__episodes__voice_actors__id=voice_id).distinct()

    # Фильтрация по году
    year = request.GET.get('year')
    if year:
        animes = animes.filter(year=year)

    # Фильтрация по рейтингу (score)
    min_score = request.GET.get('min_score')
    if min_score:
        try:
            animes = animes.filter(score__gte=float(min_score))
        except (ValueError, TypeError):
            min_score = None

    # Сортировка
    sort_by = request.GET.get('sort', '-year')
    if sort_by in ['year', '-year', 'title_ru', '-title_ru', 'score', '-score', 'views_count', '-views_count']:
        animes = animes.order_by(sort_by)

    context = {
        'animes': animes,
        'genres': genres,
        'voice_actors': voice_actors,
        'years': years,
        'sort': sort_by,
        'status': status,
        'selected_genres': genre_ids,
        'selected_voice': voice_id,
        'selected_year': year,
        'min_score': min_score,
        'original_params': original_params,
    }
    return render(request, 'catalog/catalog.html', context)
