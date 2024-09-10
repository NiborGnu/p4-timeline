from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('like/<int:pk>', views.timepost_like, name='like'),
    path('dislike/<int:pk>', views.timepost_dislike, name='dislike'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('delete_timepost/<int:pk>', views.delete_timepost, name='delete_timepost'),
    path('edit_timepost/<int:pk>', views.edit_timepost, name='edit_timepost'),
    path('search/', views.search, name='search'),
    path('timepost/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]