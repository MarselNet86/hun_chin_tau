from django.urls import path
from . import views

app_name = 'player'

urlpatterns = [
    path('<int:episode_id>/', views.player, name='player'),
    path('<int:episode_id>/next/', views.next_episode, name='next'),
    path('<int:episode_id>/prev/', views.prev_episode, name='prev'),
]
