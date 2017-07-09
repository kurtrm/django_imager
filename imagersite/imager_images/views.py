"""."""
from .models import Photo, Album
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView


class LibraryView(TemplateView):
    """List view for both albums and phots."""
    
    template_name = 'imager_images/library.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.all()
        context['albums'] = Album.objects.all()
        return {'photos': context['photos'], 'albums': context['albums']}


class PhotoListView(ListView):
    """Generic view for photo lists."""

    template_name = 'imager_images/photos.html'

    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {'photos': context['photo_list']}


class PhotoDetailView(DetailView):
    """Generic django view for single photos."""

    template_name = 'imager_images/photo.html'

    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {'photo': context['photo']}


class AlbumListView(ListView):
    """Generic view for photo lists."""

    template_name = 'imager_images/albums.html'

    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {'albums': context['album_list'].filter(published='PB')}


class AlbumDetailView(DetailView):
    """Generic django view for single photos."""

    template_name = 'imager_images/album.html'

    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_photos = context['album'].photos.filter(published='PB')
        return {'album': context['album'], 'album_photos': album_photos}
