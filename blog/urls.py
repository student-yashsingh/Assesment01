from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('tag/<slug:slug>/', views.tag_filter, name='tag_filter'),
    path('register/', views.register, name='register'),
]
