from django.contrib import admin
from imager_images.models import Photo, Album


class PhotoAdmin(admin.ModelAdmin):

    list_display = ('title')


class AlbumAdmin(admin.ModelAdmin):

    list_display = ('title')

# Register your models here.
admin.site.register(Photo)
admin.site.register(Album)
