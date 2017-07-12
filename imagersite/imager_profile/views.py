"""."""
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import UserForm


class ProfileView(TemplateView):
    """Class based view for private profiles."""

    template_name = 'imager_profile/profile.html'

    def get_context_data(self, **kwargs):
        """Build context for view."""
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['photos_priv'] = (Photo.objects
                                  .filter(published='PV')
                                  .filter(user=self.request.user)
                                  .count())
        context['photos_pub'] = (Photo.objects
                                 .filter(published='PB')
                                 .filter(user=self.request.user)
                                 .count())
        context['albums_priv'] = (Album.objects
                                  .filter(published='PV')
                                  .filter(user=self.request.user)
                                  .count())
        context['albums_pub'] = (Album.objects
                                 .filter(published='PB')
                                 .filter(user=self.request.user)
                                 .count())

        return context


class ProfileEdit(UpdateView):
    """Class based profile edit view."""

    model = User
    fields = []
    template_name = 'imager_profile/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Get user."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Assign form."""
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context['form'] = UserForm()
        return context


class PublicProfileView(TemplateView):
    """Class based public profile view."""

    template_name = 'imager_profile/public_profile.html'

    def get_context_data(self, **kwargs):
        """Build context for view."""
        context = super(PublicProfileView, self).get_context_data(**kwargs)
        request_user = User.objects.filter(username=self.kwargs['request_username'])
        imager_profile = ImagerProfile.objects.filter(user=request_user)
        context['photos_pub'] = (Photo.objects
                                 .filter(user=request_user)
                                 .filter(published='PB'))
        context['albums_pub'] = (Album.objects
                                 .filter(user=request_user)
                                 .filter(published='PB'))
        context['imager_user'] = imager_profile

        return context
