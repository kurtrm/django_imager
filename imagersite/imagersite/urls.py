"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from imagersite.views import home_view
from imager_profile.views import profile_view, public_profile
from imager_images.views import (
    library,
    albums_view,
    photos_view,
    single_album_view,
    single_photo_view
)

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(
        template_name='imagersite/home.html'), name='logout'),
    url(r'^profile/$', profile_view, name='profile'),
    url(r'^profile/(?P<request_username>\w+)/$', public_profile,
        name='public_profile'),
    url(r'^images/library/$', library, name='library'),
    url(r'^images/photos/(?P<photo_id>\d+)/$', single_photo_view,
        name='single_photo'),
    url(r'^images/photos/$', photos_view, name='photos'),
    url(r'^images/albums/(?P<album_id>\d+)/$', single_album_view,
        name='single_album'),
    url(r'^images/albums/$', albums_view, name='albums'),
    # url(r'^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
