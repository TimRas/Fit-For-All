from .models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("post_category", "title", "slug", "author", "content", "excerpt", "updated_on", "likes_post")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("post", "name", "body", "likes_comment")