from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostCategory, Comment
from .forms import PostForm, CommentForm


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

    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        comment_form.instance.email = request.user.email
        comment_form.instance.name = request.user.username
        comment = post_form.save(commit=True)
        return redirect("post_detail", post_id=post.id)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        "comment_form": comment_form,
    }

    return render(request, 'community/blog_details.html', context)


# def create_comment(request):

#     comment_form = CommentForm(data=request.POST)
#     if comment_form.is_valid():
#         comment_form.instance.email = request.user.email
#         comment_form.instance.name = request.user.username
#         pcomment = post_form.save(commit=True)
#         return redirect("post_detail", post_id=post.id)
#     else:
#         comment_form = PostForm()

#     return render(
#         request,
#         "community/blogs_create.html",
#         {
#             "comment_form": comment_form,
#         },
#     )


def create_post(request):

    post_form = PostForm(data=request.POST)
    if post_form.is_valid():
        post_form.instance.email = request.user.email
        post_form.instance.name = request.user.username
        post = post_form.save(commit=True)
        return redirect("post_detail", post_id=post.id)
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


def delete_post(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    post.delete()   
    if post.post_category.name == 'Lose Weight':
        return redirect("weight_posts")

    elif post.post_category.name == 'Gain Muscle':
        return redirect("muscle_posts")
    else:
        return redirect('home')