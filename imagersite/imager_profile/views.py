"""."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic.base import TemplateView


class ProfileView(TemplateView):
    """Classed based view for private profiles."""

    template_name = 'imager_profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos_priv'] = (Photo.objects
                                  .filter(published='PV')
                                  .count())
        context['photos_pub'] = (Photo.objects
                                 .filter(published='PB')
                                 .count())
        context['albums_priv'] = (Album.objects
                                  .filter(published='PV')
                                  .count())
        context['albums_pub'] = (Album.objects
                                 .filter(published='PB')
                                 .count())

        return context


class PublicProfileView(TemplateView):
    """Classed based public profile view."""
    template_name = 'imager_profile/public_profile.html'

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
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
