from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from anime.models import Anime
from .models import UserBookmark


def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('anime:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return redirect('users:register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('anime:index')
    
    return render(request, 'users/register.html')


def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('anime:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('anime:index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'users/login.html')


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    return redirect('anime:index')


@login_required
def profile(request):
    """Профиль пользователя"""
    # Получаем закладки пользователя
    bookmarks = UserBookmark.objects.filter(user=request.user).select_related('anime')

    # Группируем по статусам
    watching = [b for b in bookmarks if b.status == 'watching']
    completed = [b for b in bookmarks if b.status == 'completed']
    planned = [b for b in bookmarks if b.status == 'planned']
    dropped = [b for b in bookmarks if b.status == 'dropped']
    on_hold = [b for b in bookmarks if b.status == 'on_hold']

    context = {
        'user': request.user,
        'bookmarks': bookmarks,
        'watching': watching,
        'completed': completed,
        'planned': planned,
        'dropped': dropped,
        'on_hold': on_hold,
        'total_bookmarks': bookmarks.count(),
    }
    return render(request, 'users/profile.html', context)


@login_required
@require_POST
def toggle_bookmark(request):
    """Добавить/удалить аниме из закладок"""
    anime_id = request.POST.get('anime_id')
    status = request.POST.get('status', 'planned')

    if not anime_id:
        return JsonResponse({'success': False, 'error': 'Anime ID required'})

    anime = get_object_or_404(Anime, id=anime_id)

    # Проверяем, есть ли уже закладка
    bookmark = UserBookmark.objects.filter(user=request.user, anime=anime).first()

    if bookmark:
        # Если закладка есть - удаляем
        bookmark.delete()
        return JsonResponse({
            'success': True,
            'action': 'removed',
            'message': 'Удалено из закладок'
        })
    else:
        # Если закладки нет - создаём
        UserBookmark.objects.create(user=request.user, anime=anime, status=status)
        return JsonResponse({
            'success': True,
            'action': 'added',
            'message': 'Добавлено в закладки'
        })


@login_required
@require_POST
def update_bookmark_status(request):
    """Обновить статус закладки"""
    anime_id = request.POST.get('anime_id')
    status = request.POST.get('status')

    if not anime_id or not status:
        return JsonResponse({'success': False, 'error': 'Anime ID and status required'})

    bookmark = UserBookmark.objects.filter(user=request.user, anime_id=anime_id).first()

    if not bookmark:
        return JsonResponse({'success': False, 'error': 'Bookmark not found'})

    bookmark.status = status
    bookmark.save()

    return JsonResponse({
        'success': True,
        'message': 'Статус обновлён'
    })
