"""."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible


PUBLISHED_STATUS = (
    ('PB', 'public'),
    ('PV', 'private'),
    ('SH', 'shared')
)


class Photo(models.Model):
    """Create a photo model."""

    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=255, default='')
    date_uploaded = models.DateTime(auto_now=True)
    date_modified = models.DateTime(auto_now=True)
    date_published = models.DateTime(auto_now=True)
    published = models.CharField(
        max_length=2,
        choices=PUBLISHED_STATUS,
        default='PV'),
    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE)


class Album(models.Model):
    """Create an album model."""

    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=255, default='')
    date_created = models.DateTime(auto_now=True)
    date_modified = models.DateTime(auto_now=True)
    date_published = models.DateTime(auto_now=True)
    published = models.CharField(
        max_length=2,
        choices=PUBLISHED_STATUS,
        default='PV'),
    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE)
