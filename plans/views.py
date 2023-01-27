

def all_challenges(request):
    """ Renders a page to show all workout plans """

    return render(request, 'plans/challenges.html')