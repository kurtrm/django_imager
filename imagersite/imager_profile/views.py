"""."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile


@login_required
def profile_view(request):
    """View for the profile page."""
    photos_priv = (Photo.objects
                   .filter(user=request.user)
                   .filter(published='PV')
                   .count())
    photos_pub = (Photo.objects
                  .filter(user=request.user)
                  .filter(published='PB')
                  .count())
    albums_priv = (Album.objects
                   .filter(user=request.user)
                   .filter(published='PV')
                   .count())
    albums_pub = (Album.objects
                  .filter(user=request.user)
                  .filter(published='PB')
                  .count())
    return render(
        request,
        'imager_profile/profile.html',
        context={
            'photos_pub': photos_pub,
            'photos_priv': photos_priv,
            'albums_pub': albums_pub,
            'albums_priv': albums_priv}
    )


def public_profile(request, request_username):
    """Display the public profile for a given username."""
    request_username = request_username.lower()
    request_user = User.objects.filter(username=request_username)
    imager_profile = ImagerProfile.objects.filter(user=request_user)
    photos_pub = (Photo.objects
                  .filter(user=request_user)
                  .filter(published='PB')
                  )
    albums_pub = (Album.objects
                  .filter(user=request_user)
                  .filter(published='PB')
                  )
    return render(
        request,
        'imager_profile/public_profile.html',
        context={
            'imager_user': imager_profile,
            'username': request_username,
            'photos_pub': photos_pub,
            'albums_pub': albums_pub,
        }
    )
