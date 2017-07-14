"""Urls for profile related views."""
from django.conf.urls import url
from imager_profile.views import (
    ProfileView,
    PublicProfileView,
    ProfileEdit
)

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'^edit/$', ProfileEdit.as_view(), name='profile_edit'),
    url(r'^(?P<request_username>\w+)/$', PublicProfileView.as_view(),
        name='public_profile'),
]
