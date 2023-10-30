from django.shortcuts import render, get_object_or_404, redirect, reverse
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
    """ Renders a page to show a specific challenge """

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
            challenge = form.save()
            messages.success(request, 'Successfully added a challenge!')
            return redirect(reverse('challenges', args=[challenge.id]))
        else:
            messages.error(request,
                           'Failed to add challenge.'
                           'Please ensure the form is valid.')
    else:
        form = ChallengeForm()

    template = 'plans/add_challenge.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_challenge(request, challenge_id):
    """ Edit a challenge that is on the plans page """

    challenge = get_object_or_404(Challenge, pk=challenge_id)
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated challenge!')
            return redirect(reverse('challenges', args=[challenge.id]))
        else:
            messages.error(request, 'Failed to update challenge.'
                           'Please ensure the form is valid.')
    else:
        form = ChallengeForm(instance=challenge)
        messages.info(request, f'You are editing {challenge.title}')

    template = 'plans/edit_challenge.html'
    context = {
        'form': form,
        'challenge': challenge,
    }

    return render(request, template, context)


@login_required
def delete_challenge(request, challenge_id):
    """ Delete a product from the store """

    challenge = get_object_or_404(Challenge, pk=challenge_id)
    challenge.delete()
    messages.success(request, 'Challenge deleted!')
    return redirect(reverse('plans_main'))
