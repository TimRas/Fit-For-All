from django.urls import path
from . import views
from .models import PostCategory, Post

urlpatterns = [
    path('blogs_main', views.blogs_main, name='blogs_main'),
    path('blogs_category/<str:category_title>/',
         views.show_blogs_category, name='blogs_category'),
    path('check_post', views.auth_check_create_post,
         name='check_post'),
    path('create_post', views.create_post, name='create_post'),
    path('<post_id>', views.post_detail_create_comment, name='post_detail'),
    path('<post_id>/edit', views.edit_post, name='post_edit'),
    path('<post_id>/delete', views.post_delete, name='post_delete'),
    path('<comment_id>/change', views.edit_comment, name='comment_edit'),
    path('<comment_id>/remove', views.delete_comment, name='comment_delete'),
    
]