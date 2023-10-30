from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Represents a category for challenges.

    Categories are used to organize challenges into different groups.
    """

    class Meta:
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(max_length=200, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        """ Returns the string representation of the category. """

        return self.title


class Challenge(models.Model):
    """
    Challenges are specific tasks or

    goals that users can participate in.
    """
    class Meta:
        verbose_name_plural = 'Challenges'

    category = models.ForeignKey('Category', blank=True,
                                 null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(max_length=200, blank=True)
    image1 = models.ImageField(blank=True)
    image2 = models.ImageField(blank=True)
    image3 = models.ImageField(blank=True)
    image4 = models.ImageField(blank=True)
    intro = models.TextField(max_length=200, blank=True)
    steps = models.TextField(max_length=200, blank=True)
    outro = models.TextField(max_length=200, blank=True)
    tips = models.TextField(max_length=200, blank=True)

    def __str__(self):
        """ Returns the string representation of the challenge. """

        return self.title

    def number_of_likes(self):
        """
        Returns the number of likes received by this challenge.

        This method is currently not fully applied in the application yet.
        """
        return self.likes_challenge.count()
