"""."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible


class ProfileManager(models.Manager):
    """."""

    def get_queryset(self):
        """."""
        return (super(ProfileManager, self)
                .get_queryset()
                .filter(user__is_active=True))


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """Create imager-specific user profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, default='Seattle')
    age = models.IntegerField(null=True)
    job = models.CharField(max_length=50, default='')
    website = models.URLField(null=True)
    objects = models.Manager()
    active = ProfileManager()

    @property
    def is_active(self):
        """."""
        return self.user.is_active

    def __str__(self):
        """."""
        return """
        username: {}
        location: {}
        age: {}
        website: {}
        """.format(self.user.username, self.location, self.age, self.website)


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    """."""
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance'])
        new_profile.save()
