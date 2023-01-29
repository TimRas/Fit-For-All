from django.contrib import admin
from .models import Category, Challenge


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'excerpt',
        'image',
    )


class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'content',
        'image',
    )

    ordering = ('category',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Challenge, ChallengeAdmin)

