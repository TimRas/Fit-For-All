from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class PostCategory(models.Model):

    class Meta:
        verbose_name_plural = 'Post categories'

    title = models.CharField(max_length=200, default='Default Title')
    slug = models.SlugField(max_length=200, unique=True, default='default-slug')
    excerpt = models.TextField(max_length=200, blank=True)
    image = models.ImageField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post (models.Model):

    class Meta:
        ordering = ['-created_on']

    post_category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='post_categories')
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000, blank=False)
    excerpt = models.TextField(max_length=140, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
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

