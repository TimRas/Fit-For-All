from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(max_length=200, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class Challenge(models.Model):

    class Meta:
        verbose_name_plural = 'Challenges'

    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image1 = models.ImageField(blank=True)
    image2 = models.ImageField(blank=True)
    image3 = models.ImageField(blank=True)
    image4 = models.ImageField(blank=True)
    intro = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    outro = models.TextField(blank=True)
    tips = models.TextField(blank=True)
    
    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes_challenge.count()
