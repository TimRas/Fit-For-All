from django.shortcuts import render, get_object_or_404
from .models import Category, Challenge


def workout_plans(request):
    """ Renders a page to show all workout plans """

    category_workout = Category.objects.get(title='Workouts')
    challenges = Challenge.objects.filter(category=category_workout)

    context = {
        'challenges': challenges,
    }

    return render(request, 'plans/workout_plans.html', context)


def diet_plans(request):
    """ Renders a page to show all diet plans """

    category_diet = Category.objects.get(title='Diet')
    challenges = Challenge.objects.filter(category=category_diet)

    context = {
        'challenges': challenges,
    }

    return render(request, 'plans/diet_plans.html', context)


def view_challenge(request, challenge_id):

    challenge = get_object_or_404(Challenge, pk=challenge_id)
    context = {'challenge': challenge}
    return render(request, 'plans/plans_details.html', context)


# def edit_post(request, post_id):

#     post = get_object_or_404(Post, pk=post_id)      
#     if request.method == "POST":
#         post_form = PostForm(request.POST, instance=post)
#         if post_form.is_valid():
#             post_form.save(commit=True)
#             return redirect("post_detail", post_id=post_id)
#     post_form = PostForm(instance=post)

#     return render(
#         request,
#         "community/blogs_edit.html",
#         {
#             "post_form": post_form,
#         },
#     )
