"""."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Photo, Album
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile


@login_required
def library(request):
    """View for the profile page."""
    photos = Photo.objects.filter(user=request.user)
    albums = Album.objects.filter(user=request.user)
    return render(
        request,
        'imager_images/library.html',
        context={'photos': photos, 'albums': albums}
    )
