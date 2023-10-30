from django.db import models


class Category(models.Model):
    """
    Represents a product category. It is used to define product categories

    so that organizing products is able.
    """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=120)
    friendly_name = models.CharField(max_length=120)

    def __str__(self):
        """ Returns the string representation of the category. """
        return self.name

    def get_friendly_name(self):
        """ Returns the friendly name of the category. """
        return self.friendly_name


class Product(models.Model):
    """ Represents a product in the store. """
    category = models.ForeignKey('Category', blank=True,
                                 null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        """ Returns the string representation of the product. """
        return self.name
