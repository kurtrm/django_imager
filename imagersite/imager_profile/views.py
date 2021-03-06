"""."""
from imager_images.models import Photo, Album
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import UserForm


class ProfileView(LoginRequiredMixin, TemplateView):
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

    def post(self, request, *args, **kwargs):
        """Form post method."""
        self.object = self.get_object()
        user = request.user
        data = request.POST
        if data['username'] and data['email']:
            user.username = data['username']
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.imagerprofile.age = data['age']
            user.imagerprofile.job = data['job']
            user.imagerprofile.website = data['website']
            user.save()
            user.imagerprofile.save()

            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(**kwargs))


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
