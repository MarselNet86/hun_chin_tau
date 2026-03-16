from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('bookmark/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmark/update/', views.update_bookmark_status, name='update_bookmark'),
]
