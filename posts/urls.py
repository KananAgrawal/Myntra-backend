from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from posts import views

urlpatterns = [
    path('add-blog/',BlogCreateView.as_view(),name='add-blog'),
    path('add-post/',PostCreateView.as_view(), name='add-post'),
    path('add-comment/', CommentCreateView.as_view(),name='add-comment'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('blogs/<int:pk>/like/', views.like_blog, name='like-blog'),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('home/', views.home_view, name='home-view'),
    
]


