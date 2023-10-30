from .models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
    """ A form for creating or updating a blog post. """

    class Meta:
        model = Post
        fields = ('title', 'content', 'excerpt',)


class CommentForm(forms.ModelForm):
    """ A form for creating or updating a blog comment. """

    class Meta:
        model = Comment
        fields = ('body',)
