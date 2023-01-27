from django.db import models
from django.contrib.auth.models import User


class Post (models.Model):

    class Meta:
        ordering = ['-created_on']

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_on = models.DateTimeField(auto_now=0)
    content = models.TextField()
    excerp = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):

    class Meta:
        ordering = ['-created_on']

    post = models.ForeignKey(Post, on_delete=CASCADE,)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(max_length=888)
    created_on = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
            return f"Comment {self.name} by {self.name}" 

