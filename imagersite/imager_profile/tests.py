"""Tests for Imager Profile app."""

from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile

import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating users."""

    class Meta:
        """."""

        model = User
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))


class ImagerProfileTestCase(TestCase):
    """ImagerProfile tests."""

    def setUp(self):
        """."""
        users = [UserFactory.create() for i in range(20)]

        for user in users:
            user.set_password('cake')
            user.save()

        self.users = users

    def test_imager_profiles_have_user(self):
        """."""
        with self.assertRaises(Exception):
            imager_user = ImagerProfile()
            imager_user.save()

    def test_imager_profile_prints_username(self):
        """."""
        imager_profile = ImagerProfile.objects.first()
        self.assertTrue(str(imager_profile), imager_profile.user.username)

    def test_new_user_has_imager_profile(self):
        """."""
        user = UserFactory.create()
        profile = ImagerProfile.objects.last()
        self.assertTrue(profile.user == user)

    def test_user_imager_profiles_count_matches(self):
        """."""
        self.assertEquals(len(User.objects.all()), len(ImagerProfile.objects.all()))

    def test_make_one_inactive_user(self):
        """Make one inactive user."""
        user = UserFactory.create()
        user.is_active = False
        user.save()
        self.assertEquals(User.objects.count(), ImagerProfile.active.count() + 1)


#  profile related tests

# private
# logged out user redirects to login when trying to access profile
# logged out user gets 304 when trying to visit profile
# logged in user gets 200 status when visiting profile
# logged in user sees accurate info from their account
# logged in user profile library link is valid

# public
# logged in and logged out users see same content on public profile
# public profile displays public albums and photos
# get request for nonexistent user returns 'user doesn't exist'
