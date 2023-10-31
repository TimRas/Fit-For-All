from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostCategory, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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


def check_post_id(post, comment):
    return str(comment.post) == str(post.title)


def post_detail_create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.email = request.user.email
            comment.author = request.user
            comment.save()
            return redirect("post_detail", post_id=post.id)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'community/blog_details.html', context)


@login_required
def auth_check_create_post(request, category_title):
    """
    Redirects to signup page if not logged in,
    or to the create post page if logged in.
    """

    if request.user.is_authenticated:
        return redirect(reverse('create_post',
                        kwargs={'category_title': category_title}))
    else:
        messages.error(request, 'You need to be logged in create a post')
        return redirect('account_signup')


@login_required
def create_post(request, category_title):
    """ Create a new blog post in the specified category. """

    post_category = get_object_or_404(PostCategory, title=category_title)

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.post_category = post_category
            post.save()

            return redirect("post_detail", post_id=post.id)
    else:
        post_form = PostForm(initial={"category": post_category.title})

    return render(
        request,
        "community/blogs_create.html",
        {
            "post_form": post_form,
        },
    )


@login_required
def edit_post(request, post_id):
    """ Edit a existing blog post. """

    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save(commit=True)
            return redirect("post_detail", post_id=post_id)
    else:
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
    """ Delete a existing blog post and redirects to a specific category. """

    post = get_object_or_404(Post, pk=post_id)
    category_title = post.post_category.title
    post.delete()

    if category_title == 'Lose Weight':
        category_url = reverse('blogs_category', args=['Lose Weight'])
    elif category_title == 'Gain Muscle':
        category_url = reverse('blogs_category', args=['Gain Muscle'])
    else:
        return redirect('home')

    return redirect(category_url)


@login_required
def edit_comment(request, comment_id):
    """ Edit a existing comment. """

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
    """ Edit a existing comment and redirects to a specific blog post. """

    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    post_id = comment.post.id

    return redirect("post_detail", post_id=post_id)
