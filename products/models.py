from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=120)
    friendly_name = models.CharField(max_length=120)

    def __str__(self):
        return self.name
        
    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField()

    def __str__(self):
        return self.name
