"""Urls for image related views."""
from django.conf.urls import url
from imager_api.views import PhotoViewSet

photo_list = PhotoViewSet.as_view({
    'get': 'list'
})
photo_detail = PhotoViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = [
    url(r'^photos/(?P<pk>\w+)$', photo_list, name='photo_list_all'),
]
