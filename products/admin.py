from django.contrib import admin
from .models import Product, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'has_sizes',
        'price',
    )

    ordering = ('category',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

