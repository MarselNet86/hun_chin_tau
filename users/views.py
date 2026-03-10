from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


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
    return render(request, 'users/profile.html', {'user': request.user})
