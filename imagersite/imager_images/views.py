"""."""
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Photo, Album


class LibraryView(TemplateView):
    """List view for both albums and phots."""

    template_name = 'imager_images/library.html'

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
        username = context['view'].request.user
        context['photos'] = Photo.objects.filter(user=username)
        context['albums'] = Album.objects.filter(user=username)
        return context


class PhotoListView(ListView):
    """Generic view for photo lists."""

    template_name = 'imager_images/photos.html'

    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_list'] = context['photo_list'].filter(published='PB')
        return context


class PhotoDetailView(DetailView):
    """Generic django view for single photos."""

    template_name = 'imager_images/photo.html'

    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AlbumListView(ListView):
    """Generic view for photo lists."""

    template_name = 'imager_images/albums.html'

    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album_list'] = context['album_list'].filter(published='PB')
        return context


class AlbumDetailView(DetailView):
    """Generic django view for single photos."""

    template_name = 'imager_images/album.html'

    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album_photos'] = context['album'].photos.filter(published='PB')
        return context
