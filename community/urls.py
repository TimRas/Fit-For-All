from django.urls import path
from . import views
from .models import PostCategory, Post

urlpatterns = [
    path('gain_muscle', views.muscle_posts, name='muscle_posts'),
    path('lose_weight', views.weight_posts, name='weight_posts'),
    path('create_post', views.create_post, name='create_post'),
    path('<post_id>', views.post_detail, name='post_detail'),
    path('<post_id>/edit', views.edit_post, name='post_edit'),
    
]