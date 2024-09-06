from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('like/<int:pk>', views.TimePost_like, name='like'),
    path('dislike/<int:pk>', views.TimePost_dislike, name='dislike'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
]