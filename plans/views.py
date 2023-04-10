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



