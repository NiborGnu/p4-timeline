from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('profiles/', views.profiles, name='profiles'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('like/<int:pk>', views.TimePost_like, name='like'),
    path('dislike/<int:pk>', views.TimePost_dislike, name='dislike'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
]