"""."""
from django.db import models
from django.contrib.auth.models import User


class ProfileManager(models.Manager):
    """."""

    def get_queryset(self):
        """."""
        return super(ProfileManager, self).get_queryset().filter(user__is_active=True)


class ImagerProfile(models.Model):
    """Create imager-specific user profile."""

    user = models.OneToOneField(User)
    location = models.CharField(max_length=50)
    age = models.IntegerField()
    job = models.CharField(max_length=50)
    website = models.URLField()
    objects = models.Manager()
    active = ProfileManager()

    @property
    def is_active(self):
        """."""
        return self.user.is_active
