from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('profiles/', views.profiles, name='profiles'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('like/<int:pk>', views.TimePost_like, name='like'),
    path('dislike/<int:pk>', views.TimePost_dislike, name='dislike'),
]