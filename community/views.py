from django.shortcuts import render, get_object_or_404
# from django.views import generic
from .models import Post, PostCategory, Comment


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


def check_post_id(post, comment):
    return str(comment.post) == str(post.title)

  
def post_detail(request, post_id):
        
    """ Renders a page to show all community posts and categories """

    post = get_object_or_404(Post, pk=post_id)
    comments = [x for x in Comment.objects.all() if check_post_id(post, x)]

    context = {
        'post': post,
        'comments': comments,
    }

    return render(request, 'community/blog_details.html', context)