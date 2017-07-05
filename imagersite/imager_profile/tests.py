"""Tests for Imager Profile app."""

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.urls import reverse
from bs4 import BeautifulSoup


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
class PrivateProfileView(TestCase):
    """ImagerProfile tests."""

    def setUp(self):
        """."""
        user = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user.save()
        self.user = user
        self.client = Client()

    def test_logged_out_user_redirects(self):
        """Logged out user redirects to login."""
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_logged_in_user_gets_200_status(self):
        """Logged in user gets 200 status on profile get."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertTrue(response.status_code == 200)

    def test_username_appears(self):
        """Test username displays."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        html = BeautifulSoup(response.content, 'html.parser')
        username = html.find_all('p', 'username')
        self.assertIn(self.user.username, username[0])

    def test_link_checks_out(self):
        """Logged in user goes to their image library."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('library'))
        self.assertTrue(response.status_code == 200)


class PublicProfileView(TestCase):
    """ImagerProfile tests."""

    def setUp(self):
        """."""
        users = [UserFactory.create() for i in range(20)]

        for user in users:
            user.set_password('cake')
            user.save()

        self.users = users


# public
# logged in and logged out users see same content on public profile
# public profile displays public albums and photos
# get request for nonexistent user returns 'user doesn't exist'
