"""Project-level views."""
from django.shortcuts import render


def home_view(request):
    """View for the home page."""
    return render(
        request,
        'imagersite/home.html',
        context={'content': 'cake'}
    )
