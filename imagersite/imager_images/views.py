"""."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Photo, Album


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


def photos_view(request):
    """View for multiple photos only."""
    photos_pub = Photo.objects.filter(published='PB')
    return render(
        request,
        'imager_images/photos.html',
        context={'photos': photos_pub}
    )


def single_photo_view(request, photo_id):
    """View for a single photo."""
    #  Template for checking if public or private
    photo = Photo.objects.get(id=photo_id)
    return render(
        request,
        'imager_images/photo.html',
        context={'photo': photo}
    )


def albums_view(request):
    """View for multiple albums only."""
    albums_pub = Album.objects.filter(published='PB')
    return render(
        request,
        'imager_images/albums.html',
        context={'albums': albums_pub}
    )


def single_album_view(request, album_id):
    """View for a single album."""
    album = Album.objects.get(id=album_id)
    album_photos = [album.photos[i] for i in range(album.photos)]
    return render(
        request,
        'imager_images/album.html',
        context={'album': album_photos}
    )
