from django.urls import path
from . import views


urlpatterns = [
    path('profiles/', views.profiles, name='profiles'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
]
