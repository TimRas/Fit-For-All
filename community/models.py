from django.db import models
from django.contrib.auth.models import User


class Post (models.Model):

    class Meta:
        ordering = ['-created_on']

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=400, blank=False)
    excerpt = models.TextField(blank=True) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=0)
    likes_post = models.ManyToManyField(User, blank=True, related_name='post_likes')

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes_post.count()


class Comment (models.Model):

    class Meta:
        ordering = ['-created_on']

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    body = models.TextField(max_length=888, blank=False)
    created_on = models.DateTimeField(auto_now=True)
    likes_comment = models.ManyToManyField(User, blank=True, related_name='comment_likes')

    def __str__(self):
      return f"Comment on {self.post} by {self.name}" 

