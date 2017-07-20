"""Serialize Photo data."""

from rest_framework import serializers
from imager_images.models import Photo
from imager_profile.models import ImagerProfile


class PhotoSerializer(serializers.ModelSerializer):
    """Serialize photo data."""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        """Define model and fields."""

        model = Photo
        fields = (
            'user',
            'title',
            'description',
            'date_uploaded',
            'date_modified',
            'date_published',
            'published',
            'photo')
