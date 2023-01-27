from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Challenge(models.Model):

    class Meta:
        verbose_name_plural = 'Challenges'

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    
    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
