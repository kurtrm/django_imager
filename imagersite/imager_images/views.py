"""."""
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Photo, Album


class LibraryView(LoginRequiredMixin, TemplateView):
    """List view for both albums and phots."""

    template_name = 'imager_images/library.html'

    def get_context_data(self, **kwargs):
        """Build context to create view."""
        context = super(LibraryView, self).get_context_data(**kwargs)
        username = context['view'].request.user
        context['photos'] = Photo.objects.filter(user=username)
        context['albums'] = Album.objects.filter(user=username)
        context['tags'] = set([tag for photo in context['photos'] for tag in photo.tags.names()])
        return context


class PhotoListView(ListView):
    """Generic view for photo lists."""

    template_name = 'imager_images/photos.html'
    model = Photo

    def get_context_data(self, **kwargs):
        """Build context to create view."""
        context = super(PhotoListView, self).get_context_data(**kwargs)
        context['photo_list'] = context['photo_list'].filter(published='PB')
        return context


class PhotoDetailView(DetailView):
    """Generic django view for single photos."""

    template_name = 'imager_images/photo.html'
    model = Photo


class AlbumListView(ListView):
    """Generic view for photo lists."""

    template_name = 'imager_images/albums.html'
    model = Album

    def get_context_data(self, **kwargs):
        """Filter albums by published."""
        context = super(AlbumListView, self).get_context_data(**kwargs)
        context['album_list'] = context['album_list'].filter(published='PB')
        return context


class AlbumDetailView(DetailView):
    """Generic django view for single photos."""

    template_name = 'imager_images/album.html'
    model = Album

    def get_context_data(self, **kwargs):
        """Build context to create view."""
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        context['album_photos'] = context['album'].photos.filter(published='PB')
        context['tags'] = set([tag for photo in context['album_photos'] for tag in photo.tags.names()])
        return context


class PhotoCreate(LoginRequiredMixin, CreateView):
    """Class-based view to create new photos."""

    model = Photo
    fields = ['title', 'description', 'published', 'photo', 'tags']
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """Identify form data with user and save in db."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateView, self).form_valid(form)


class PhotoEdit(LoginRequiredMixin, UpdateView):
    """Class-based view to edit photos."""

    model = Photo
    fields = ['title', 'description', 'published', 'photo', 'tags']
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """Identify form data with user and save in db."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(UpdateView, self).form_valid(form)


class AlbumCreate(LoginRequiredMixin, CreateView):
    """Class-based view to create new albums."""

    model = Album
    fields = ['title', 'description', 'photos', 'cover', 'published']
    success_url = reverse_lazy('library')

    def get_form(self):
        """Update form fields with photos belonging to user."""
        form = super(AlbumCreate, self).get_form()
        user_photos = Photo.objects.filter(user=self.request.user)
        form.fields['photos'].queryset = user_photos
        form.fields['cover'].queryset = user_photos
        return form

    def form_valid(self, form):
        """Identify form data with user and save in db."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateView, self).form_valid(form)


class AlbumEdit(LoginRequiredMixin, UpdateView):
    """Class-based view to create new albums."""

    model = Album
    fields = ['title', 'description', 'photos', 'cover', 'published']
    success_url = reverse_lazy('library')

    def get_form(self):
        """Update form fields with photos belonging to user."""
        form = super(AlbumEdit, self).get_form()
        user_photos = Photo.objects.filter(user=self.request.user)
        form.fields['photos'].queryset = user_photos
        form.fields['cover'].queryset = user_photos
        return form

    def form_valid(self, form):
        """Identify form data with user and save in db."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(UpdateView, self).form_valid(form)


class TagListView(ListView):
    """The listing for tagged books."""

    template_name = "imager_images/photos.html"

    def get_queryset(self):
        """Filter queryset by slug."""
        # import pdb; pdb.set_trace()
        return (Photo.objects.filter(tags__slug=self.kwargs.get("slug"))
                             .filter(published='PB')
                             .all())

    def get_context_data(self, **kwargs):
        """Return the context with the given tags."""
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        return context
