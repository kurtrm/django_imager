"""."""
from imager_images.models import Photo
from imager_profile.models import ImagerProfile
# from imager_api.permissions import IsOwnerOrReadOnly
# from django.contrib.auth.models import User
from rest_framework import renderers
from rest_framework import (
    generics,
    permissions
)
from imager_api.serializers import (
    PhotoSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import detail_route


class PhotoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    # import pdb; pdb.set_trace()
    # queryset = Photo.objects.filter(published='PB')
    serializer_class = PhotoSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

    def get_queryset(self):
        """Filter queryset by slug."""
        return Photo.objects.filter(user='pk').filter(published='PB')

    # def get_context_data(self, **kwargs):
    #     """Return the context with the given tags."""
    #     context = super(TagListView, self).get_context_data(**kwargs)
    #     context["tag"] = self.kwargs.get("slug")
    #     return context