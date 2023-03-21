from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("post_category", "title", "slug", "author", "content", "excerpt", "updated_on", "likes_post")