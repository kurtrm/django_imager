"""Urls for image related views."""
from django.conf.urls import url
from .views import (
    LibraryView,
    AlbumDetailView,
    AlbumListView,
    PhotoDetailView,
    PhotoListView,
    PhotoCreate,
    PhotoEdit,
    AlbumCreate,
    AlbumEdit,
    TagListView
)

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^photos/(?P<pk>\d+)/$', PhotoDetailView.as_view(),
        name='single_photo'),
    url(r'^photos/add/$', PhotoCreate.as_view(), name='photo_add'),
    url(r'^photos/$', PhotoListView.as_view(), name='photos'),
    url(r'^photos/(?P<pk>\w+)/edit/$', PhotoEdit.as_view(), name='photo_edit'),
    url(r'^photos/tag/(?P<slug>[-\w]+)/$', TagListView.as_view(), name="tagged_images"),
    url(r'^albums/(?P<pk>\d+)/$', AlbumDetailView.as_view(),
        name='single_album'),
    url(r'^albums/$', AlbumListView.as_view(), name='albums'),
    url(r'^albums/add/$', AlbumCreate.as_view(), name='album_add'),
    url(r'^albums/(?P<pk>\w+)/edit/$', AlbumEdit.as_view(), name='album_edit')
]
