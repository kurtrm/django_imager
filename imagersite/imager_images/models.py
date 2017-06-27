"""."""
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


class Photo(models.Model):
    """Create a photo model."""

    PUBLISHED_STATUS = (
        ('PB', 'public'),
        ('PV', 'private'),
        ('SH', 'shared'),
    )

    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=255, default='')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True)
    published = models.CharField(
        max_length=2,
        choices=PUBLISHED_STATUS,
        default='PV')
    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='user_images',
        null=True
    )

    def __repr__(self):
        """Represent."""
        return "<Photo: {}>".format(self.title)


class Album(models.Model):
    """Create an album model."""

    PUBLISHED_STATUS = (
        ('PB', 'public'),
        ('PV', 'private'),
        ('SH', 'shared'),
    )

    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=255, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True)
    published = models.CharField(
        max_length=2,
        choices=PUBLISHED_STATUS,
        default='PV')
    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE)
    photos = models.ManyToManyField(
        Photo,
        default='',
        related_name='albums')
    cover = models.ForeignKey(
        Photo,
        null=True,
        related_name='+')

    def __repr__(self):
        """Represent."""
        return "<Album: {}>".format(self.title)