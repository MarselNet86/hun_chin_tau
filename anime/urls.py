from django.urls import path
from . import views

app_name = 'anime'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_anime, name='search'),
    path('anime/<slug:slug>/', views.anime_detail, name='detail'),
]
