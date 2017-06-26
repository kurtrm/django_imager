"""."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imager_images.models import Photo, Album


@login_required
def profile_view(request):
    """View for the profile page."""
    photos = Photo.objects.filter(user=request.user).all().count()
    albums = Album.objects.filter(user=request.user).all().count()
    return render(
        request,
        'imager_profile/profile.html',
        context={'photos': photos, 'albums': albums}
    )
