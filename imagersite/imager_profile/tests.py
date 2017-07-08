"""Tests for Imager Profile app."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from bs4 import BeautifulSoup
import faker
import datetime
import factory
import os


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
        #  This may be redundant from a test in the 
        self.client.force_login(self.user)
        response = self.client.get(reverse('library'))
        self.assertTrue(response.status_code == 200)


fake = faker.Faker()


HERE = os.path.dirname(__file__)


class PhotoFactory(factory.django.DjangoModelFactory):
    """Factory for creating photos."""

    class Meta:
        """."""

        model = Photo

    title = factory.Sequence(
        lambda n: 'Photo{}'.format(n)
    )
    description = fake.text(254)
    date_modified = datetime.datetime.now()
    photo = SimpleUploadedFile(
        name='example.jpg',
        content=open(os.path.join(
            HERE,
            'static',
            'jerry-kiesewetter-192478.jpg'), 'rb').read(),
        content_type='image/jpeg')


class AlbumFactory(factory.django.DjangoModelFactory):
    """Factory for creating albums."""

    class Meta:
        """."""

        model = Album

    title = factory.Sequence(
        lambda n: 'Album{}'.format(n)
    )
    description = fake.text(254)
    date_modified = datetime.datetime.now()


class PublicProfileView(TestCase):
    """ImagerProfile tests."""

    def setUp(self):
        """."""
        user_1 = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user_1.save()
        self.user_1 = user_1
        self.client = Client()

        user_2 = User(
            username='mcgee',
            email='mcgee@mcgee.com'
        )
        user_2.save()
        self.user_2 = user_2
        self.client = Client()

        user_3 = User(
            username='mcgeeman',
            email='mcgeeman@mcgeeman.com'
        )
        user_3.save()
        self.user_3 = user_3
        self.client = Client()

        photos_1 = PhotoFactory.build()
        photos_1.user = self.user_2
        photos_1.title = 'Private Image'
        photos_1.save()
        photos_2 = PhotoFactory.build()
        photos_2.user = self.user_2
        photos_2.title = 'Public Image'
        photos_2.published = 'PB'
        photos_2.save()

        album_1 = AlbumFactory.build()
        album_1.user = self.user_2
        album_1.title = 'Private Album'
        album_1.save()
        album_2 = AlbumFactory.build()
        album_2.user = self.user_2
        album_2.title = 'Public Album'
        album_2.published = 'PB'
        album_2.save()

        self.photos_1 = photos_1
        self.photos_2 = photos_2
        self.album_1 = album_1
        self.album_2 = album_2

    def test_logged_logged_out_in_users_see_same_stuff(self):
        """."""
        response_logged_out = self.client.get(reverse('public_profile',
                                              kwargs={'request_username': 'mcgeeman'}))
        self.client.force_login(self.user_1)
        response_logged_in = self.client.get(reverse('public_profile',
                                             kwargs={'request_username': 'mcgeeman'}))
        self.assertEqual(response_logged_out.content, response_logged_in.content)

    def test_public_profiles_display_public_albums(self):
        """."""
        response = self.client.get(reverse('public_profile',
                                   kwargs={'request_username': 'mcgee'}))
        html = BeautifulSoup(response.content, 'html.parser')
        albums = html.find_all('li', 'album-title')
        self.assertIn(self.album_2.title, albums[0])

    def test_public_profiles_display_public_photos(self):
        """."""
        response = self.client.get(reverse('public_profile',
                                   kwargs={'request_username': 'mcgee'}))
        html = BeautifulSoup(response.content, 'html.parser')
        photos = html.find_all('li', 'photo-title')
        self.assertIn(self.photos_2.title, photos[0])

    def test_public_profiles_display_no_private_albums(self):
        """."""
        response = self.client.get(reverse('public_profile',
                                   kwargs={'request_username': 'mcgee'}))
        html = BeautifulSoup(response.content, 'html.parser')
        albums = html.find_all('li', 'album-title')
        self.assertNotIn(self.album_1.title, albums[0])

    def test_public_profiles_display__private_photos(self):
        """."""
        response = self.client.get(reverse('public_profile',
                                   kwargs={'request_username': 'mcgee'}))
        html = BeautifulSoup(response.content, 'html.parser')
        photos = html.find_all('li', 'photo-title')
        self.assertNotIn(self.photos_1.title, photos[0])

    def test_request_for_nonexistent_user_returns_correct(self):
        """Expect 'user' doesn't exist."""
        response = self.client.get(reverse('public_profile',
                                   kwargs={'request_username': 'wheatie'}))
        html = BeautifulSoup(response.content, 'html.parser')
        p_tag = html.find_all('p')
        self.assertIn('user doesn\'t exist', p_tag[0])
