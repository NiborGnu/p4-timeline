from django.urls import path
from . import views


urlpatterns = [
    path(
        'users/',
        views.users,
        name='users'
        ),
    path(
        'profile/<int:pk>',
        views.profile,
        name='profile'
        ),
    path(
        'profile/followers/<int:pk>',
        views.followers,
        name='followers'
        ),
    path(
        'profile/follows/<int:pk>',
        views.follows,
        name='follows'
        ),
    path(
        'profile/<int:profile_id>/delete/',
        views.delete_profile,
        name='delete_profile'
        ),
]
