"""."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile


@login_required
def profile_view(request):
    """View for the profile page."""
    photos = Photo.objects.filter(user=request.user).count()
    albums = Album.objects.filter(user=request.user).count()
    return render(
        request,
        'imager_profile/profile.html',
        context={'photos': photos, 'albums': albums}
    )


def public_profile(request, request_username):
    """Display the public profile for a given username."""
    request_user = User.objects.filter(username=request_username)
    imager_profile = ImagerProfile.objects.filter(user=request_user)
    return render(
        request,
        'imager_profile/public_profile.html',
        context={'imager_user': imager_profile, 'username': request_username}
    )
