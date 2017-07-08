"""Project-level views."""
from django.shortcuts import render
from imager_images.models import Photo


def home_view(request):
    """View for the home page."""
    photos = Photo.objects.all()
    images = [photos[i].photo.url for i, _ in enumerate(photos)]

    return render(
        request,
        'imagersite/home.html',
        context={'content': 'cake',
                 'image': images}
    )


def account_view(request):
    """View for the registration page."""
    return render(request, 'registration/account.html')
