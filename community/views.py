from django.shortcuts import render, get_object_or_404
from .models import Post, PostCategory, Comment


def muscle_posts(request):
        
    """ Renders a page to show all gain muscle posts """

    category_muscle = PostCategory.objects.get(name='Gain Muscle')
    posts_muscle = Post.objects.filter(post_category=category_muscle).values()

    context = {
        'posts_muscle': posts_muscle,

    }

    return render(request, 'community/blogs_gain_muscle.html', context)


def weight_posts(request):
        
    """ Renders a page to show all lose weight posts """

    category_weight = PostCategory.objects.get(name='Lose Weight')
    posts_weight = Post.objects.filter(post_category=category_weight).values()

    context = {
        'posts_weight': posts_weight,

    }

    return render(request, 'community/blogs_lose_weight.html', context)


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