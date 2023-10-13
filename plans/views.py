from django.shortcuts import render, get_object_or_404
from .models import Category, Challenge
from .forms import ChallengeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def plans_main(request):
    """ Renders a page to show all plan categories """

    all_categories = Category.objects.all()
 
    all_plans = []
    for category in all_categories:
        challenges_in_category = Challenge.objects.filter(category=category)
        all_plans.extend(challenges_in_category)

    context = {
        'all_categories': all_categories,
        'all_plans': all_plans,
    }

    return render(request, 'plans/plans_main.html', context)


def show_plans_category(request, category_title):
    """ Renders a page to show plans of a specific category """

    category = Category.objects.get(title=category_title)
    challenges = Challenge.objects.filter(category=category)

    context = {
            'category': category,
            'challenges': challenges,
        }

    return render(request, 'plans/plans_category.html', context)
    

def view_challenge(request, challenge_id):

    challenge = get_object_or_404(Challenge, pk=challenge_id)
    context = {
            'challenge': challenge,
        }
    return render(request, 'plans/plans_details.html', context)


@login_required
def add_challenge(request):
    """ Add a challenge to the plans page """
    
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added a challenge!')
            return redirect(reverse('challenges', args=[challenge.id]))
        else:
            messages.error(request, 'Failed to add challenge. Please ensure the form is valid.')
    else:
        form = ChallengeForm()

    template = 'plans/add_challenge.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


