from django.shortcuts import render
from .models import Category, Challenge


def all_plans(request):
    """ Renders a page to show all workout plans """

    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'plans/workout_plans.html', context)

