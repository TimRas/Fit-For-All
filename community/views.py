from django.shortcuts import render
# from django.views import generic
from .models import Post, PostCategory


# class PostCategories(generic.ListView):
#     model = PostCategory
#     queryset = Post.objects.order_by('-likes_post')
#     template_name = 'community/blogs.html'


# class PostList(generic.ListView):
    
#     model = Post
#     queryset = Post.objects.order_by('-created_on')
#     template_name = 'community/blogs.html'
#     paginate_by = 4


def all_posts(request):
        
    """ Renders a page to show all community posts and categories """

    post_categories = PostCategory.objects.all()
    posts = Post.objects.all()

    context = {
        'postcategories': post_categories,
        'posts': posts,
    }

    return render(request, 'community/blogs.html', context)
