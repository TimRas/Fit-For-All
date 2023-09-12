from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostCategory, Comment
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import PostForm, CommentForm


def blogs_main(request): 
    """ Renders a page to show all blog categories """

    all_categories = PostCategory.objects.all()

    all_blogs = []
    for category in all_categories:
        blogs_in_category = Post.objects.filter(post_category=category)
        all_blogs.extend(blogs_in_category)
    
    context = {
        'all_categories': all_categories,
        'all_blogs': all_blogs,
    }

    return render(request, 'community/blogs_main.html', context)


def show_blogs_category(request, category_title):
    """ Renders a page to show blogs of a specific category """

    category = PostCategory.objects.get(title=category_title)
    posts = Post.objects.filter(post_category=category)  

    context = {
        'category': category,
        'posts': posts,
    }

    return render(request, 'community/blogs_category.html', context)


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

  
def post_detail_create_comment(request, post_id):
        
    """ Renders a page to show all community posts and categories """

    post = get_object_or_404(Post, pk=post_id)
    comments = [x for x in Comment.objects.all() if check_post_id(post, x)]
    
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        comment_form.instance.email = request.user.email
        comment_form.instance.name = request.user.username
        comment = comment_form.save(commit=True)
        return redirect("post_detail", post_id=post.id)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        "comment_form": comment_form,
    }

    return render(request, 'community/blog_details.html', context)


@login_required
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


@login_required
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


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    category_title = post.post_category.title

    # Delete the post
    post.delete()

    # Determine the URL for the appropriate category
    if category_title == 'Lose Weight':
        category_url = reverse('blogs_category', args=['lose_weight'])
    elif category_title == 'Gain Muscle':
        category_url = reverse('blogs_category', args=['gain_muscle'])
    else:
        # If the category is not recognized, you can redirect to the home page
        return redirect('home')

    # Redirect to the appropriate category page
    return redirect(category_url)



@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save(commit=True)
            post_id = comment.post.id
            return redirect("post_detail", post_id=post_id)
    comment_form = CommentForm(instance=comment)

    return render(
        request,
        "community/comment_edit.html",
        {
            "comment_form": comment_form,
        },
    )


@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    post_id = comment.post.id

    return redirect("post_detail", post_id=post_id)   
