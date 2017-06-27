"""."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imager_images.models import Photo, Album
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


def public_profile(request, username):
    """Display the public profile for a given username."""
    # user_profile = ImagerProfile.objects.filter(user=username).all()
    # return render(
    #     request,
    #     'imager_profile/public_profile.html',
    #     context={'user': user_profile}
    # )
    pass
