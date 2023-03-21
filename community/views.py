from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostCategory, Comment
from .forms import PostForm


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


def create_post(request):

    post_form = PostForm(data=request.POST)
    if post_form.is_valid():
        post_form.instance.email = request.user.email
        post_form.instance.name = request.user.username
        post = post_form.save(commit=True)
        return redirect("post_detail", post_id=post_id)
    else:
        post_form = PostForm()

    return render(
        request,
        "community/blogs_create.html",
        {
            "post_form": post_form,
        },
    )


def edit_post(request, post_id):

    post = get_object_or_404(Post, pk=post_id)      
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save(commit=True)
            return redirect("post_detail", post_id=post_id)
    post_form = PostForm(instance=post)

    return render(
        request,
        "community/blogs_edit.html",
        {
            "post_form": post_form,
        },
    )
