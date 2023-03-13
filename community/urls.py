from django.urls import path
from . import views
from .models import PostCategory, Post

urlpatterns = [
    path('', views.all_posts, name='posts'),
    path('<post_id>', views.post_detail, name='post_detail'),
    
]