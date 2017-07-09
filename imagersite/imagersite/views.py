"""Project-level views."""
from django.shortcuts import render
from django.views.generic.base import TemplateView
from imager_images.models import Photo


class HomeView(TemplateView):
    """View for the home page."""
    template_name = 'imagersite/home.html'

    def get_context_data(self, **kwargs):
        photos = Photo.objects.all()
        context = super().get_context_data(**kwargs)
        context['image'] = [photos[i].photo.url for i in range(len(photos))]

        return context


def account_view(request):
    """View for the registration page."""
    return render(request, 'registration/account.html')
