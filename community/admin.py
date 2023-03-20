from django.contrib import admin
from .models import Post, Comment, PostCategory


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'created_on',
        'updated_on',
    )

    ordering = ('likes_post',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'name',
        'created_on',
    )

    ordering = ('likes_comment',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)




