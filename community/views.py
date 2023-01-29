from django.shortcuts import render



def all_posts(request):
    """ Renders a page to show all community posts """

    return render(request, 'community/blogs.html')